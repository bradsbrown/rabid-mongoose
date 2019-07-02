"""Tests around the shutdown call."""
import time

import pytest
import requests


@pytest.mark.usefixtures("running_server")
def test_shutdown_response(client):
    response = client.shutdown()
    assert response.status_code == 200
    assert not response.content


@pytest.mark.usefixtures("running_server")
def test_shutdown_disallows_posts(client, random_string):
    # First load up some jobs to be run
    for _ in range(10):
        client.post_password(random_string())
    client.shutdown()
    with pytest.raises(requests.exceptions.ConnectionError):
        client.post_password(random_string())
