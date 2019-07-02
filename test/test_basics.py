"""Basic tests around the `/hash` GET and POST calls."""
import pytest

pytestmark = pytest.mark.usefixtures("server")

def test_get_invalid(client):
    """Validate the expected client error from an invalid hash job id."""
    response = client.get_hash("asdf")
    assert response.status_code == 400


def test_basic_post(client):
    """Validate a simple job post to ensure it is accepted."""
    response = client.post_password("test_basic_post")
    job_id = response.json()
    assert job_id


def _post_and_assert_hash_value(client, hash_from, password):
    response = client.post_password(password)
    job_id = response.json()
    get_response = client.get_hash(job_id)
    assert get_response.status_code == 200
    assert get_response.text == hash_from(password)


def test_hash_value(client, hash_from):
    """Validate a posted password generates the expected hash value."""
    password = "test_hash_value"
    _post_and_assert_hash_value(client, hash_from, password)


@pytest.mark.parametrize("length", [10, 100, 10000])
def test_long_strings(client, hash_from, random_string, length):
    """Validate that any printable ascii string of any length succeeds."""
    _post_and_assert_hash_value(client, hash_from, random_string(length))


@pytest.mark.parametrize("length", [10, 100, 10000])
def test_long_unicode(client, hash_from, random_unicode, length):
    """Validate that any printable unicode string of any length succeeds."""
    _post_and_assert_hash_value(client, hash_from, random_unicode(length))
