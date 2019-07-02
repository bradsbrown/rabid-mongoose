"""Test `/hash` endpoint under concurrent calls."""
import concurrent.futures

import pytest

pytestmark = pytest.mark.usefixtures("server")


def _bulk_post(post_call, passwords):
    result_dict = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_data = {
            executor.submit(post_call, p): p
            for p in passwords
        }
        for future in concurrent.futures.as_completed(future_to_data):
            p = future_to_data[future]
            job_id = future.result().json()
            result_dict[p] = job_id
    return result_dict


def _bulk_retrieve(get_call, job_ids):
    result_dict = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_data = {
            executor.submit(get_call, j): j
            for j in job_ids
        }
        for future in concurrent.futures.as_completed(future_to_data):
            j = future_to_data[future]
            pw_hash = future.result().text
            result_dict[j] = pw_hash
    return result_dict



@pytest.mark.parametrize("count", [5, 15, 50, 100])
def test_bulk_uploads(client, random_string, hash_from, count):
    """Validate that bulk concurrent calls all return expected results."""
    passwords = [random_string() for _ in range(count)]
    pw_to_id_map = _bulk_post(client.post_password, passwords)
    id_to_hash_map = _bulk_retrieve(client.get_hash, list(pw_to_id_map.values()))
    collected_data = [(k, v, id_to_hash_map[v]) for k, v in pw_to_id_map.items()]
    failed_matches = list(filter(lambda x: hash_from(x[0]) != x[2], collected_data))
    assert not failed_matches, f"There were {len(failed_matches)} failures from {count} entries."
