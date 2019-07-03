"""Tests around the shutdown call."""
import random
import time

import pytest
from pytest_bdd import parsers, scenarios, given, when, then
import requests.exceptions


scenarios("../features/shutdown.feature")


@given("some jobs posted")
def post_some_jobs(client, random_string, result):
    result.job_ids = [
        client.post_password(random_string()).json() for _ in range(10)
    ]


@when("the endpoint processes a call to shutdown")
def request_shutdown(client, result):
    result.response = client.shutdown()


@then("a call to <action> is not accepted")
def check_call_not_accepted(client, random_string, result, action):
    action_dict = {
        "post a password": lambda: client.post_password(random_string()),
        "get a hash": lambda: client.get_hash(random.choice(result.job_ids))
    }
    with pytest.raises(requests.exceptions.ConnectionError):
        action_dict[action]()
