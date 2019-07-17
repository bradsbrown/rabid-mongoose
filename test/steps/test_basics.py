"""Basic tests around the `/hash` GET and POST calls."""
import random

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


@when("the endpoint processes a password payload that <description>")
def post_payload_with_no_pw_key(client, result, random_string, description):
    payload = {
        "is a dict with no 'password' key": lambda: {random_string(): random_string()},
        "is an integer": lambda: random.randint(1, 999999),
        "is a string": random_string,
        "is a list": lambda: [random_string() for _ in range(5)],
        "is a non-JSON dict": lambda: {random_string(): random_string()},
    }[description]()
    kwargs = {"data" if "non-JSON" in description else "json": payload}
    result.response = client.post("/hash", **kwargs)


@then("a Job ID is returned")
def job_id_is_returned(result):
    job_id = result.response.json()
    # The ID should not be an empty result
    assert job_id
    # The ID should be a single value (not dict, list, etc.)
    assert isinstance(job_id, (str, int))


@then("the Job ID is returned immediately")
def job_id_is_immediate(result):
    response_secs = result.response.elapsed.total_seconds()
    msg = f"The response took {response_secs:0.2f} seconds to return!"
    assert response_secs < 1, msg
