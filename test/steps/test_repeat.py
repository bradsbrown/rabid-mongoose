"""Tests for repeated values."""
import pytest
from pytest_bdd import scenarios, when, then

pytestmark = pytest.mark.usefixtures("server")

scenarios("../features/repeats.feature")


@when("the endpoint processes multiple requests to post the same password")
def repeated_password_posts(client, random_string, result):
    result.password = random_string()
    result.job_ids = [client.post_password(result.password).json() for _ in range(20)]


@when("the hash values for each are retrieved")
def retrieve_hash_values(client, result):
    result.hashes = [client.get_hash(j).text for j in result.job_ids]


@then("there is a unique Job ID returned for each post")
def check_unique_job_ids(result):
    msg = "Fewer job ids than submissions!"
    assert len(set(result.job_ids)) == len(result.job_ids), msg


@then("all hash values match")
def check_hash_values_match(result):
    msg = "More than one hash was found for the same password!"
    assert len(set(result.hashes)) == 1, msg
    result.hash = result.hashes[0]
