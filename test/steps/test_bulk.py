"""Test `/hash` endpoint under concurrent calls."""
import pytest
from pytest_bdd import parsers, scenarios, given, when, then

pytestmark = pytest.mark.usefixtures("server")

scenarios("../features/concurrency.feature")


def _do_bulk_upload(client, bulk_call, passwords):
    pw_to_id_map = bulk_call(client.post_password, passwords)
    id_to_hash_map = bulk_call(
        client.get_hash, list(pw_to_id_map.values()), data_extract=lambda x: x.text
    )
    return [(k, v, id_to_hash_map[v]) for k, v in pw_to_id_map.items()]


def _filter_to_mismatches(hash_from, result_list):
    return list(filter(lambda x: hash_from(x[0]) != x[2], result_list))


@given("<count> randomly generated passwords to upload")
@given(parsers.parse("{count:d} randomly generated passwords to upload"))
def randomly_generated_passwords(random_string, result, count):
    result.passwords = [random_string() for _ in range(int(count))]


@when(
    "the endpoint processes concurrent requests to post the passwords and retrieve the hashes"
)
def post_and_retrieve_concurrently(client, bulk_call, result):
    result.collected_data = _do_bulk_upload(client, bulk_call, result.passwords)


@when(
    "the endpoint processes sequential requests to retrieve any initially mismatched hashes"
)
def find_mismatches_and_reattempt(client, hash_from, result):
    result.failed_matches = _filter_to_mismatches(hash_from, result.collected_data)
    for idx, entry_tuple in enumerate(result.failed_matches):
        result.failed_matches[idx] = (
            entry_tuple[0],
            entry_tuple[1],
            client.get_hash(entry_tuple[1]).text,
        )


@then("all hashes match their given passwords")
def check_all_hashes_match(hash_from, result):
    failed_matches = _filter_to_mismatches(hash_from, result.collected_data)
    msg = (
        f"There were {len(failed_matches)} hashes that didn't match their password, "
        f"out of {len(result.collected_data)} entries."
    )
    assert not failed_matches, msg


@then("both the counts of unique Job IDs and hashes match the password count")
def validate_unique_jobid_and_hash_counts(result):
    password_count = len(result.passwords)
    job_id_count = len({x[1] for x in result.collected_data})
    hash_count = len({x[2] for x in result.collected_data})
    msg = (
        f"There were {job_id_count} unique job ids and {hash_count} unique hashes "
        f"for {password_count} records."
    )
    assert job_id_count == hash_count == password_count, msg


@then("no mismatches between password and hash remain")
def check_remaining_failures_after_retry(hash_from, result):
    final_failures = list(
        filter(lambda x: hash_from(x[0]) != x[2], result.failed_matches)
    )
    msg = (
        f"Out of {len(result.failed_matches)} initial failures, "
        f"{len(final_failures)} remained after retry."
    )
    assert not final_failures, msg
