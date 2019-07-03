import base64
import concurrent.futures
import hashlib
import os
import random
import string
import subprocess
import time
import types

import requests
import pytest
from pytest_bdd import given, then


class HashClient(requests.Session):
    """Custom client for easy calls against the hash server."""

    def __init__(self, *args, hash_port=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.hash_port = hash_port

    def request(self, method, url, *args, **kwargs):
        """Build a full url from the provided path, then place the call."""
        full_url = f"http://localhost:{self.hash_port}{url}"
        return super().request(method, full_url, *args, **kwargs)

    def post_password(self, password):
        return self.post("/hash", json={"password": password})

    def get_hash(self, job_id):
        return self.get(f"/hash/{job_id}")

    def get_stats(self):
        return self.get("/stats")

    def shutdown(self):
        return self.post("/hash", data="shutdown")


###################
# Static Fixtures #
###################


@pytest.fixture(scope="session", autouse=True)
def port():
    """Ensure a port is set and shared for server and client."""
    port = os.getenv("PORT")
    if not port:
        port = os.environ["PORT"] = "8000"
    return port


@pytest.fixture(scope="session")
def client(port):
    """Create requests client with base url built-in."""
    client = HashClient(hash_port=port)
    adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
    client.mount("http://", adapter)
    return client


@pytest.fixture(scope="module")
def start_server():
    def _start_server():
        subprocess.Popen(["./bin/broken-hashserve_darwin"])
        # allow an arbitrary few seconds for the server to start up
        time.sleep(2)

    return _start_server


@pytest.fixture(scope="module")
def server(start_server, client):
    """Run server for life of testing."""
    start_server()
    yield
    client.shutdown()


@pytest.fixture
def result():
    return types.SimpleNamespace()


#####################
# Fixture Functions #
#####################


@pytest.fixture
def hash_from():
    """Accept a password and return the expected hash value."""

    def _hash_from(password):
        return base64.b64encode(
            hashlib.sha512(password.encode("utf-8")).digest()
        ).decode("utf-8")

    return _hash_from


def random_unicode_char():
    """Return any random printable unicode character."""
    while True:
        i = random.randint(32, 0x110000)
        char = chr(i)
        if char.isprintable():
            break
    return char


@pytest.fixture
def random_string():
    """Generate a random string of printable ascii characters."""

    def _random_string(length=10):
        return "".join(random.choice(string.printable) for _ in range(length))

    return _random_string


@pytest.fixture
def random_unicode():
    """Generate a random string of printable unicode characters."""

    def _random_unicode(length=10):
        return "".join(random_unicode_char() for _ in range(length))

    return _random_unicode


def _get_json(response):
    return response.json()


@pytest.fixture
def bulk_call():
    def _bulk_call(call_fn, values, data_extract=_get_json):
        result_dict = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_data = {executor.submit(call_fn, v): v for v in values}
            for future in concurrent.futures.as_completed(future_to_data):
                v = future_to_data[future]
                result = data_extract(future.result())
                result_dict[v] = result
        return result_dict

    return _bulk_call


######################
# common Given steps #
######################


@given("a running server")
def running_server(start_server):
    start_server()


#####################
# common Then steps #
#####################


@then("the response is successful")
def response_is_successful(result):
    assert 200 <= result.response.status_code <= 299


@then("the response is a client error")
def response_is_client_error(result):
    assert 400 <= result.response.status_code <= 499


@then("the response content is empty")
def response_content_is_empty(result):
    assert not result.response.content


@then("the hash returned matches a hash of the password")
def hashes_match(hash_from, result):
    assert result.hash == hash_from(result.password)
