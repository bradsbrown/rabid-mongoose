Issue Report
============

Summary
-------
Multiple concurrent connections result in inaccurate data.

Description
-----------
When placing a large amount of concurrent calls,
the server can mismatch responses
such that the posted password -> job id -> hash value
linkage does not match up.

How to reproduce
----------------
Run many concurrent calls to post passwords.

.. Note::

    the volume of calls seems to be less a factor
    than the simultaneous nature of the calls.

Once placed, call to retrieve all hashes by job id,
and compare the hashes returned
with a local hash of the original password.
You will likely find at least a few
that have failed to match up.

After further testing,
I believe I have isolated the issue to
concurrent password POSTs causing
one of the hashed values to be written to
the job ID of all concurrent calls.
Note the second and third outputs below.
In the second, we see that
each post always returns a unique job ID,
but the hash values returned for that set of job IDs
is not always unique.
In the third, we see that
the incorrect value is returned upon subsequent attempts
to retrieve the correct hash,
suggesting it is not a problem of concurrent retrieval,
but of concurrent POST.

Sample Output
-------------

Sample concurrent post run::

    ======================================================== FAILURES =========================================================
    __________________________________________________ test_bulk_uploads[5] ___________________________________________________

    client = <conftest.HashClient object at 0x10a305438>
    random_string = <function random_string.<locals>._random_string at 0x10a309d08>
    hash_from = <function hash_from.<locals>._hash_from at 0x10a309c80>, count = 5

        @pytest.mark.parametrize("count", [5, 15, 50, 100])
        def test_bulk_uploads(client, random_string, hash_from, count):
            passwords = [random_string() for _ in range(count)]
            pw_to_id_map = _bulk_post(client.post, passwords)
            id_to_hash_map = _bulk_retrieve(client.get, list(pw_to_id_map.values()))
            collected_data = [(k, v, id_to_hash_map[v]) for k, v in pw_to_id_map.items()]
            failed_matches = list(filter(lambda x: hash_from(x[0]) != x[2], collected_data))
    >       assert not failed_matches, f"There were {len(failed_matches)} failures from {count} entries."
    E       AssertionError: There were 4 failures from 5 entries.
    E       assert not [("hV'@7;_ko.", 1, '8xnDIwlbf8Qh6qmuw0GFsHgiwTN342Rx0wl8aCf3TOBUJJ93JNGKF1gEV6Fly1ZvVrXvhxu30wNLsedaRY/MJg=='), ('\x0b...MJg=='), ('iNRjk:pLan', 2, '8xnDIwlbf8Qh6qmuw0GFsHgiwTN342Rx0wl8aCf3TOBUJJ93JNGKF1gEV6Fly1ZvVrXvhxu30wNLsedaRY/MJg==')]

    test/test_bulk.py:42: AssertionError
    __________________________________________________ test_bulk_uploads[15] __________________________________________________

    client = <conftest.HashClient object at 0x10a305438>
    random_string = <function random_string.<locals>._random_string at 0x10a366620>
    hash_from = <function hash_from.<locals>._hash_from at 0x10a3661e0>, count = 15

        @pytest.mark.parametrize("count", [5, 15, 50, 100])
        def test_bulk_uploads(client, random_string, hash_from, count):
            passwords = [random_string() for _ in range(count)]
            pw_to_id_map = _bulk_post(client.post, passwords)
            id_to_hash_map = _bulk_retrieve(client.get, list(pw_to_id_map.values()))
            collected_data = [(k, v, id_to_hash_map[v]) for k, v in pw_to_id_map.items()]
            failed_matches = list(filter(lambda x: hash_from(x[0]) != x[2], collected_data))
    >       assert not failed_matches, f"There were {len(failed_matches)} failures from {count} entries."
    E       AssertionError: There were 2 failures from 15 entries.
    E       assert not [('9}Zt9BEX,x', 12, 'fXVlATZEUBYe8drnWv43SlUxEMjsrYxL/wrmJRgl4EHH6imf5HofP2vNVtw9DeSr7r+UMVwafZWj1iZT0wWI8g=='), ('bYL2Mw\rHty', 14, 'TK7UxF4xGnAJyYUeTkqtgUjQw4houTIq5denmQCnpR25GbauuirH1yrppGCbDJo2NnJZMzGJDrWPJDEacDtVGA==')]

    test/test_bulk.py:42: AssertionError
    __________________________________________________ test_bulk_uploads[50] __________________________________________________

    client = <conftest.HashClient object at 0x10a305438>
    random_string = <function random_string.<locals>._random_string at 0x10a366598>
    hash_from = <function hash_from.<locals>._hash_from at 0x10a366bf8>, count = 50

        @pytest.mark.parametrize("count", [5, 15, 50, 100])
        def test_bulk_uploads(client, random_string, hash_from, count):
            passwords = [random_string() for _ in range(count)]
            pw_to_id_map = _bulk_post(client.post, passwords)
            id_to_hash_map = _bulk_retrieve(client.get, list(pw_to_id_map.values()))
            collected_data = [(k, v, id_to_hash_map[v]) for k, v in pw_to_id_map.items()]
            failed_matches = list(filter(lambda x: hash_from(x[0]) != x[2], collected_data))
    >       assert not failed_matches, f"There were {len(failed_matches)} failures from {count} entries."
    E       AssertionError: There were 3 failures from 50 entries.
    E       assert not [('VR|kk9CW#\\', 32, 'MmLipl2521xQdpEKjRpRYNdBqlyOW1WMwu1ljSx3Kx0b6B+IP6pTjIA92wfl+oAVl+4hKWAXrfGCpyJiQt7smg=='), ('BS...0Q=='), ('$[]1~9dOb=', 63, 'OXrbTUuTdT4ku2Qu3NCNhY9CIUV9xXHuPg0biNpuuREHBHwfccGvXM7t6Q44JezWjDrU0XqgXc/W7bzmqUOOrg==')]

    test/test_bulk.py:42: AssertionError
    _________________________________________________ test_bulk_uploads[100] __________________________________________________

    client = <conftest.HashClient object at 0x10a305438>
    random_string = <function random_string.<locals>._random_string at 0x10a3667b8>
    hash_from = <function hash_from.<locals>._hash_from at 0x10a366d08>, count = 100

        @pytest.mark.parametrize("count", [5, 15, 50, 100])
        def test_bulk_uploads(client, random_string, hash_from, count):
            passwords = [random_string() for _ in range(count)]
            pw_to_id_map = _bulk_post(client.post, passwords)
            id_to_hash_map = _bulk_retrieve(client.get, list(pw_to_id_map.values()))
            collected_data = [(k, v, id_to_hash_map[v]) for k, v in pw_to_id_map.items()]
            failed_matches = list(filter(lambda x: hash_from(x[0]) != x[2], collected_data))
    >       assert not failed_matches, f"There were {len(failed_matches)} failures from {count} entries."
    E       AssertionError: There were 3 failures from 100 entries.
    E       assert not [("JlDu^z'8|x", 129, 'Ck41vwnv2Gnp1fDMsb1sXodcM3XmndSs2a7ewBCz3PCx6mVYykaUK/Ix9cWm+jz2/5KRpwiw4rq3OQhJxTcbCA=='), ('}@...A=='), ('dMt:2v).LZ', 154, 'A3Hx+oND3QmrB5t4Okr3HceW1Cse4EEAkt7nBZmtdB+Q6STlge1ViN/le2ldYJiC3XUYvDKhKzyVFj/p0JpIKA==')]


Output of uniqueness check::

    ____________________________________________________________ test_unique_values _____________________________________________________________

    bulk_call = <function bulk_call.<locals>._bulk_call at 0x10bdad510>, client = <conftest.HashClient object at 0x10bd915c0>
    random_string = <function random_string.<locals>._random_string at 0x10bdad1e0>

        def test_unique_values(bulk_call, client, random_string):
            """Validate that no duplicate hashes are returned."""
            count = 20
            passwords = [random_string() for _ in range(count)]
            collected_data = _do_bulk_upload(client, bulk_call, passwords)
            job_id_count = len({x[1] for x in collected_data})
            hash_count = len({x[2] for x in collected_data})
            msg = (
                f"There were {job_id_count} unique job ids and {hash_count} unique hashes "
                "for {count} records."
            )
    >       assert job_id_count == hash_count == count, msg
    E       AssertionError: There were 20 unique job ids and 19 unique hashes for 20 records.
    E       assert 20 == 19

    test/test_bulk.py:40: AssertionError

Output of retry check::


    bulk_call = <function bulk_call.<locals>._bulk_call at 0x10d603488>, client = <conftest.HashClient object at 0x10bd915c0>
    hash_from = <function hash_from.<locals>._hash_from at 0x10d603510>
    random_string = <function random_string.<locals>._random_string at 0x10d603730>

        def test_retry_failed(bulk_call, client, hash_from, random_string):
            """Test retrying mismatched values by calling the given job IDs again sequentially."""
            passwords = [random_string() for _ in range(20)]
            collected_data = _do_bulk_upload(client, bulk_call, passwords)
            failed_matches = list(filter(lambda x: hash_from(x[0]) != x[2], collected_data))
            for idx, entry_tuple in enumerate(failed_matches):
                failed_matches[idx] = (
                    entry_tuple[0], entry_tuple[1], client.get_hash(entry_tuple[1]).text
                )
            final_failures = list(filter(lambda x: hash_from(x[0]) != x[2], failed_matches))
            msg = f"Out of {len(failed_matches)} initial failures, {len(final_failures)} remained after retry."
    >       assert not final_failures, msg
    E       AssertionError: Out of 2 initial failures, 2 remained after retry.
    E       assert not [('Na4^8^/l@.', 192, 'j+HAh9y3iiWu4RCvs+1qeH0XsIWk1a7AN2jFWW+XZlKYb8Zjxx59yhHppt/DXkGK5prpkePqyf6GteuEM8F4Tw=='), ('#{j6?f>0@n', 203, '+SMTV53Kdh0eMzmROMmyPYZA0Y+RRDdWiljXeOdgd1ISPKc+Lhd2JukA4pbJrdAKlAYxFjNZApAvhKiJYIRgiQ==')]

    test/test_bulk.py:54: AssertionError
