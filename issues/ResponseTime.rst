Issue Report
============

Summary
-------
Response to POSTing a password is delayed.

Description
-----------
The server specifications state that
upon posting a password the repsonse should be immediate,
after which the server will wait 5 seconds
then hash the posted password.

What is happening instead is that the response is delayed
for 5 seconds, at which point the hash is immediately available.

The desired fix is for the server to return a Job ID
as soon as password is submitted.

How to reproduce
----------------
Make any valid password POST call,
and record the response time from the server.
It will consistently be approximately 5 seconds.

Sample Output
-------------

From the relevant scenario output:

    ================================================================================= FAILURES ==================================================================================
    _______________________________________________________________ test_password_post_returns_immediate_response _______________________________________________________________

    request = <FixtureRequest for <Function test_password_post_returns_immediate_response>>

        response_secs = result.response.elapsed.total_seconds()
    >   msg = f"The response took {response_secs:0.2f} seconds to return!"

    test/steps/test_basics.py:49:
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    ../../.virtualenvs/hs/lib/python3.6/site-packages/pytest_bdd/scenario.py:195: in _execute_scenario
        _execute_step_function(request, scenario, step, step_func)
    ../../.virtualenvs/hs/lib/python3.6/site-packages/pytest_bdd/scenario.py:136: in _execute_step_function
        step_func(**kwargs)
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    result = namespace(password='rFJ|*zN|>|', response=<Response [200]>)

        @then("the Job ID is returned immediately")
        def job_id_is_immediate(result):
            response_secs = result.response.elapsed.total_seconds()
            msg = f"The response took {response_secs:0.2f} seconds to return!"
    >       assert response_secs < 1, msg
    E       AssertionError: The response took 5.00 seconds to return!
    E       assert 5.00261 < 1

    test/steps/test_basics.py:50: AssertionError
    ==================================================================== 1 failed, 5 passed in 27.17 seconds ====================================================================
