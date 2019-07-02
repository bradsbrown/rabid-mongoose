Issue Report
============

Summary
-------
``AverageTime`` calculation does not match expectations.

Description
-----------
The ``AverageTime`` key is described in the project specs as::

    the average time of a hash request in milliseconds.

In testing, it appears that the value returned is _much_ larger
than the measured round-trip time
(time to post a password then retrieved the hashed value),
almost by a factor of 10.

How to reproduce
----------------
Measure the round-trip time (as described above)
for multiple calls and compare to the ``/stats`` call ``AverageTime`` key.

Can be automatically tested via ``pytest test/test_stats.py``.

Sample Output
-------------


Sample run::

        def test_stats_call(client, random_string):
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
    >       assert stats["AverageTime"] < average_call_cycle
    E       assert 48700 < 5010.865831375122
