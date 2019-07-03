Feature: Test concurrent calls

  Scenario Outline: Concurrent uploads return matching hashes
    Given <count> randomly generated passwords to upload
    When the endpoint processes concurrent requests to post the passwords and retrieve the hashes
    Then all hashes match their given passwords

    Examples:
      | count |
      | 5     |
      | 15    |
      | 50    |
      | 100   |

  Scenario: Concurrent uploads return unique Job ID and hash values
    Given 20 randomly generated passwords to upload
    When the endpoint processes concurrent requests to post the passwords and retrieve the hashes
    Then both the counts of unique Job IDs and hashes match the password count

  Scenario: Re-retrival attempt for originally mismatched concurrent hashes succeeds
    Given 20 randomly generated passwords to upload
    When the endpoint processes concurrent requests to post the passwords and retrieve the hashes
    And the endpoint processes sequential requests to retrieve any initially mismatched hashes
    Then no mismatches between password and hash remain
