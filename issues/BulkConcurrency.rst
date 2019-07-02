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

Sample Output
-------------

Sample run::

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

