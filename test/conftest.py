import base64
import hashlib
import os
import random
import string
import subprocess

import requests
import pytest


class HashClient(requests.Session):
    """Custom client for easy calls against the hash server."""

    def __init__(self, *args, hash_port=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.hash_port = hash_port

    def request(self, method, url, *args, **kwargs):
        """Build a full url from the provided path, then place the call."""
        full_url = f"http://localhost:{self.hash_port}{url}"
        return super().request(method, full_url, *args, **kwargs)


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
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=100, pool_maxsize=100
    )
    client.mount('http://', adapter)
    return client


@pytest.fixture(scope="module", autouse=True)
def server(client):
    """Run server for life of testing."""
    pid = subprocess.Popen(["./bin/broken-hashserve_darwin"]).pid
    yield
    client.post("/hash", data="shutdown")


@pytest.fixture
def hash_from():
    """Accept a password and return the expected hash value."""

    def _hash_from(password):
        return base64.b64encode(
            hashlib.sha512(password.encode('utf-8')).digest()
        ).decode('utf-8')

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
        return ''.join(random.choice(string.printable) for _ in range(length))

    return _random_string


@pytest.fixture
def random_unicode():
    """Generate a random string of printable unicode characters."""

    def _random_unicode(length=10):
        return ''.join(random_unicode_char() for _ in range(length))

    return _random_unicode
