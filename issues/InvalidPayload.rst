Issue Report
============

Summary
-------
Hash endpoint accepts invalid payload.

Description
-----------
The endpoint documentation stipulates that
the expected payload format to post a password is::

    {"password": "mysamplepassword"}

In most cases, the endpoint will reject improperly formatted values,
returing a 400 response code and a "Malformed Input" message.

However, if the payload is a JSON dictionary,
the response seems to be unconditionally accepted.
If a "password" key is present in the dict,
that value will be used to generate the hash.
However, if no "password" key is present,
the value of first key in the dict will be used instead.

Note::

    In testing, it appears that subsequent key/value pairs
    have no impact on the hashed value,
    and the "password" key will always take precedence.
    The "password" key is also prioritized case-insensitive --
    "PaSSwoRd" is the same as "PASSWORD" is the same as "password".

How to reproduce
----------------
Submit a payload in JSON dict format as a POST to the /hash endpoint,
with key/value pairs in which no key is any capitalization variant of "password".
Note that the POST is accepted,
and that the Job ID provided will return a valid hash
which pairs to the first key in the dict.

Given the same first value (regardless of key),
you can vary the first key
as well as any subsequent key/value pairs,
with repeated posts,
and as long as the first value is the same,
and no "password" key is present,
all Job IDs will return the same hash.

Sample Output
-------------

Sample from test case::


    request = <FixtureRequest for <Function test_invalid_formats_are_rejected>>

    >   ???

    test/steps/test_basics.py:65:
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    ../../.virtualenvs/hs/lib/python3.6/site-packages/pytest_bdd/scenario.py:195: in _execute_scenario
        _execute_step_function(request, scenario, step, step_func)
    ../../.virtualenvs/hs/lib/python3.6/site-packages/pytest_bdd/scenario.py:136: in _execute_step_function
        step_func(**kwargs)
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    result = namespace(response=<Response [200]>)

        @then("the response is a client error")
        def response_is_client_error(result):
    >       assert 400 <= result.response.status_code <= 499
    E       assert 400 <= 200
    E        +  where 200 = <Response [200]>.status_code
    E        +    where <Response [200]> = namespace(response=<Response [200]>).response

    test/steps/conftest.py:175: AssertionError

