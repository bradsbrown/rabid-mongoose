"""Tests for repeated values."""


def test_repeats(client, random_string, hash_from):
    """Test that repeat values are each treated as independent entitites."""
    password = random_string()
    count = 20

    job_ids = []
    for _ in range(count):
        job_ids.append(client.post("/hash", json={"password": password}).json())

    hashes = []
    for job_id in job_ids:
        hashes.append(client.get(f"/hash/{job_id}").text)

    assert len(set(job_ids)) == count, "Fewer job ids than submissions!"
    assert len(set(hashes)) == 1, "More than one hash was found for the same password!"
    assert hash_from(password) == hashes[0], "Password did not match hash!"
