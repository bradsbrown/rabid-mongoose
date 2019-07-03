Feature: Hash endpoint GET and POST basic tests

  Scenario: basic POST is accepted
    When the endpoint processes a request to post a password
    Then the response is successful
    And a Job ID is returned

  Scenario: password is hashed as expected
    When the endpoint processes a request to post a password
    And the hash for that password is requested
    Then the hash returned matches a hash of the password

  Scenario: Long strings are successful
    Given a password that is a long string
    When the endpoint processes a request to post a password
    And the hash for that password is requested
    Then the hash returned matches a hash of the password

  Scenario: Unicode is successful
    Given a password containing non-ASCII unicode characters
    When the endpoint processes a request to post a password
    And the hash for that password is requested
    Then the hash returned matches a hash of the password

  Scenario: Retrieve invalid Job ID fails
    When the endpoint processes a request to retrieve an invalid Job ID
    Then the response is a client error
