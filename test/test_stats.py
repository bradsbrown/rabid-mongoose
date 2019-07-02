"""Basic test for `/stats` endpoints."""
import time

import pytest

pytestmark = pytest.mark.usefixtures("server")


def test_stats_call(client, random_string):
    """Validate Returned stats match expected values."""
    time_stats = []
    post_count = 10
    for _ in range(post_count):
        start_time = time.time()
        job_id = client.post_password(random_string()).json()
        client.get_hash(job_id)
        time_stats.append(time.time() - start_time)
    response = client.get_stats()
    assert response.json()
    stats = response.json()
    assert stats["TotalRequests"] == post_count
    average_call_cycle = (sum(time_stats) / len(time_stats)) * 1000
    assert stats["AverageTime"] < average_call_cycle
