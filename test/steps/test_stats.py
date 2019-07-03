"""Basic test for `/stats` endpoints."""
import time

import pytest
from pytest_bdd import parsers, scenarios, given, when, then

pytestmark = pytest.mark.usefixtures("server")

scenarios("../features/stats.feature")


@when("the endpoint processes a request for stats")
def request_stats(client, result):
    result.response = client.get_stats()


@when("the endpoint processes multiple password posts and hash retrievals")
def multiple_password_posts(client, random_string, result):
    result.post_count = 10

    time_stats = []
    for _ in range(result.post_count):
        start_time = time.time()
        job_id = client.post_password(random_string()).json()
        client.get_hash(job_id)
        time_stats.append(time.time() - start_time)

    result.average_cycle_ms = (sum(time_stats) / len(time_stats)) * 1000



@then(parsers.parse('the "{key}" value is {value}'))
def key_value_matches(result, key, value):
    response = result.response.json()
    assert key in response
    assert float(response[key]) == float(value)


@then("the request count matches the posted count")
def request_count_matches(result):
    assert result.response.json()["TotalRequests"] == result.post_count


@then("the average time value in ms is less than average password cycle time")
def average_time_matches(result):
    assert result.response.json()["AverageTime"] <= result.average_cycle_ms
