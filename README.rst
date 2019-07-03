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
All you need to do it call ``./run_tests.sh``!
The test suite will automatically spin up the API server,
run the tests,
and report results,
then spin down the server when finished.


Very cool! But did you find any bugs?
-------------------------------------

Of course!
You'll see some failures as you run the tests,
and you can also view details of the failures
in the ``issues`` directory of this repository.

Why did you test what you did?
------------------------------

The goal was to start with the most basic checks --
can I actually post something and retrieve the hash, etc. --
then to build around that looking for potential failure points.
It seemed to me that,
given a service using some sort of shared data store,
and supporting concurrent calls in and out,
that the most likely point of potential failure was in that intersection.

What is the structure here?
---------------------------
You'll find 3 main directories:

- ``bin`` - contains the compiled server executable as well as its version file.
- ``issues`` - contains documentation of issues found, as well as a template for future issue reports.
- ``test`` - contains the test suite. There are 2 subdirectories to note:

  - ``features`` - contains the Gherkin descriptions of the endpoint specifications being tested
  - ``steps`` - contains the python code to run the tests as defined in the Gherkin

How do I modify/add tests?
--------------------------

To contribute, there are a few things you'll need to do,
and a few you'll need to know.

All the details:

- Install the development requirements (``pip install -r dev-requirements.txt``)
- Before committing, run ``./self_check.sh`` to autoformat and lint your code
- It might be helpful to review the workings of pytest-bdd_ and pytest_
- Currently, all shared steps are stored in ``tests/steps/conftest.py``,
  with feature-specific step defs in the individual ``test_{feature}.py`` files.
- If you want to test against specific features or scenarios,
  the args in the `pytest specifications`_ can be passed into `./run_tests.sh`

.. _pytest: https://pytest.org
.. _pytest-bdd: https://pytest-bdd.readthedocs.io/en/latest/
.. _`pytest specifications`: https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests
