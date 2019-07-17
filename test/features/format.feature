Feature: Return Format

  Scenario Outline: Return values are in JSON Format
    When the endpoint processes a request to <description>
    Then the response is a JSON Content Type
    And the content is json-parseable

    Examples:
      | description     |
      | post a password |
      | retrieve a hash |
      | retrieve stats  |
