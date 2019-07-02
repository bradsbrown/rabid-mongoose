"""Tests around the shutdown call."""
import random
import time

import pytest
import requests


@pytest.mark.usefixtures("running_server")
def test_shutdown_response(client):
    """Validate that shutdown response matches expected."""
    response = client.shutdown()
    assert response.status_code == 200
    assert not response.content


@pytest.mark.usefixtures("running_server")
def test_shutdown_disallows_posts(client, random_string):
    """Validate that shutdown disallows new posts."""
    # First load up some jobs to be run
    for _ in range(10):
        client.post_password(random_string())
    client.shutdown()
    with pytest.raises(requests.exceptions.ConnectionError):
        client.post_password(random_string())


@pytest.mark.usefixtures("running_server")
def test_shutdown_disallows_get_jobs(client, random_string):
    """Validate that shutdown disallows getting job data."""
    # First load up some jobs to be run
    job_ids = [client.post_password(random_string()).json() for _ in range(10)]
    client.shutdown()
    with pytest.raises(requests.exceptions.ConnectionError):
        client.get_hash(random.choice(job_ids))
