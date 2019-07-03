"""Basic tests around the `/hash` GET and POST calls."""
import pytest
from pytest_bdd import scenarios, given, when, then

pytestmark = pytest.mark.usefixtures("server")

scenarios("../features/hash.feature")


@given("a password that is a long string")
def long_string_password(random_string, result):
    result.password = random_string(10000)


@given("a password containing non-ASCII unicode characters")
def unicode_password(random_unicode, result):
    result.password = random_unicode(50)


@when("the endpoint processes a request to post a password")
def basic_post_request(client, random_string, result):
    result.password = getattr(result, "password", random_string())
    result.response = client.post_password(result.password)


@when("the hash for that password is requested")
def retrieve_hash(client, result):
    result.job_id = result.response.json()
    result.hash = client.get_hash(result.job_id).text


@when("the endpoint processes a request to retrieve an invalid Job ID")
def retrieve_invalid_job_id(client, random_string, result):
    result.response = client.get_hash(random_string())


@then("a Job ID is returned")
def job_id_is_returned(result):
    job_id = result.response.json()
    # The ID should not be an empty result
    assert job_id
    # The ID should be a single value (not dict, list, etc.)
    assert isinstance(job_id, (str, int))
