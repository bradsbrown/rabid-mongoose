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
- ``test`` - contains the test suite. Each ``test_{something}`` file covers a particular feature of the server.
- ``issues`` - contains documentation of issues found, as well as a template for future issue reports.
