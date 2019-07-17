import json

from pytest_bdd import scenarios, when, then

scenarios("../features/format.feature")


@when("the endpoint processes a request to <description>")
def endpoint_processes_request(client, result, random_string, description):
    call = {
        "post a password": lambda: client.post_password(random_string()),
        "retrieve a hash": lambda: client.get_hash(client.post_password(random_string()).json()),
        "retrieve stats": lambda: client.get_stats(),
    }[description]
    result.response = call()


@then("the response is a JSON Content Type")
def response_is_json_type(result):
    content_type = result.response.headers["Content-Type"]
    assert "application/json" in content_type, f"Content Type was '{content_type}'"


@then("the content is json-parseable")
def response_is_json_parseable(result):
    try:
        result.response.json()
    except json.decoder.JSONDecodeError as e:
        raise AssertionError("Response was not JSON-parseable") from e
