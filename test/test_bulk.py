"""Test `/hash` endpoint under concurrent calls."""
import pytest

pytestmark = pytest.mark.usefixtures("server")


@pytest.mark.parametrize("count", [5, 15, 50, 100])
def test_bulk_uploads(bulk_call, client, random_string, hash_from, count):
    """Validate that bulk concurrent calls all return expected results."""
    passwords = [random_string() for _ in range(count)]

    pw_to_id_map = bulk_call(client.post_password, passwords)
    id_to_hash_map = bulk_call(
        client.get_hash, list(pw_to_id_map.values()), data_extract=lambda x: x.text
    )

    collected_data = [(k, v, id_to_hash_map[v]) for k, v in pw_to_id_map.items()]
    failed_matches = list(filter(lambda x: hash_from(x[0]) != x[2], collected_data))
    assert not failed_matches, f"There were {len(failed_matches)} failures from {count} entries."
