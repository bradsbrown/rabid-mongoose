QA Assignment
=============

What is this?
-------------

This is a project to attempt to test a black-box API,
finding bugs and documenting them.

How do set it up?
-----------------

- First, you'll need to ensure you have Python 3.6 or later available on your system.
- Create a VirtualEnv with your tool of choice (one simple suggestion would be ``python3 -m venv VENV``)
- with that environment activated (``source VENV/bin/activate``), install the requirements (``pip install -r requirements.txt``)

Ok, but how do I run it?
------------------------

This is the fun part.
All you need to do it call ``pytest .``!
The test suite will automatically spin up the API server,
run the tests,
and report results,
then spin down the server when finished.

.. Note::

    If you want more information as it runs,
    you can call ``pytest -v .`` to get more details in the console.

Very cool! But did you find any bugs?
-------------------------------------

Of course!
You'll see some as you run the tests,
but you can also view descriptions of the failures
in the ``issues`` directory of this repository.
