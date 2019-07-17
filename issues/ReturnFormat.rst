Issue Report
============

Summary
-------
Return values are not provided in the expected JSON format.

Description
-----------
The specifications note that requests should provide JSON,
and that return values should be in JSON  as well.

All data returned is given with a ``Content-Type`` header of ``text/plain; charset=utf-8``
rather than the expected ``application/json``.
In some cases, such as a POST to ``/hash`` or a GET to ``/stats``,
the data is still parse-able as JSON,
since in the first case the return is an integer,
and in the second is a dictionary.

However, the string value returned from a GET call to ``/hash/{job_id}``
is a plain string that is not JSON-formatted.

How to reproduce
----------------
* Make any call to any endpoint, note the ``Content-Type`` header value.
* Attempt to parse (``json.loads()``) the response from a GET ``/hash/{job_id}`` call.
