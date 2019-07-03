"""Test `/hash` endpoint under concurrent calls."""
import pytest

pytestmark = pytest.mark.usefixtures("server")


def _do_bulk_upload(client, bulk_call, passwords):
    pw_to_id_map = bulk_call(client.post_password, passwords)
    id_to_hash_map = bulk_call(
        client.get_hash, list(pw_to_id_map.values()), data_extract=lambda x: x.text
    )
    return [(k, v, id_to_hash_map[v]) for k, v in pw_to_id_map.items()]



@pytest.mark.parametrize("count", [5, 15, 50, 100])
def test_bulk_uploads(bulk_call, client, random_string, hash_from, count):
    """Validate that bulk concurrent calls all return hashes that match the given password."""
    passwords = [random_string() for _ in range(count)]
    collected_data = _do_bulk_upload(client, bulk_call, passwords)
    failed_matches = list(filter(lambda x: hash_from(x[0]) != x[2], collected_data))
    msg = (
        f"There were {len(failed_matches)} hashes that didn't match their password, "
        f"out of {count} entries."
    )
    assert not failed_matches, msg


def test_unique_values(bulk_call, client, random_string):
    """Validate that no duplicate hashes are returned."""
    count = 20
    passwords = [random_string() for _ in range(count)]
    collected_data = _do_bulk_upload(client, bulk_call, passwords)
    job_id_count = len({x[1] for x in collected_data})
    hash_count = len({x[2] for x in collected_data})
    msg = (
        f"There were {job_id_count} unique job ids and {hash_count} unique hashes "
        f"for {count} records."
    )
    assert job_id_count == hash_count == count, msg


def test_retry_failed(bulk_call, client, hash_from, random_string):
    """Test retrying mismatched values by calling the given job IDs again sequentially."""
    passwords = [random_string() for _ in range(20)]
    collected_data = _do_bulk_upload(client, bulk_call, passwords)
    failed_matches = list(filter(lambda x: hash_from(x[0]) != x[2], collected_data))
    for idx, entry_tuple in enumerate(failed_matches):
        failed_matches[idx] = (
            entry_tuple[0], entry_tuple[1], client.get_hash(entry_tuple[1]).text
        )
    final_failures = list(filter(lambda x: hash_from(x[0]) != x[2], failed_matches))
    msg = f"Out of {len(failed_matches)} initial failures, {len(final_failures)} remained after retry."
    assert not final_failures, msg
