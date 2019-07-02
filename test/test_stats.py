"""Basic test for `/stats` endpoints."""
import time


def test_stats_call(client, random_string):
    """Validate Returned stats match expected values."""
    time_stats = []
    post_count = 10
    for _ in range(post_count):
        start_time = time.time()
        id = client.post("/hash", json={"password": random_string()}).json()
        client.get(f"/hash/{id}")
        time_stats.append(time.time() - start_time)
    response = client.get("/stats")
    assert response.json()
    stats = response.json()
    assert stats["TotalRequests"] == post_count
    average_call_cycle = (sum(time_stats) / len(time_stats)) * 1000
    assert stats["AverageTime"] < average_call_cycle
