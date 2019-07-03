Feature: Shutdown call tests

  Scenario: Shutdown response matches expected
    Given a running server
    When the endpoint processes a call to shutdown
    Then the response is successful
    And the response content is empty

  Scenario Outline: Shutdown denies subsequent requests
    Given a running server
    And some jobs posted
    When the endpoint processes a call to shutdown
    Then a call to <action> is not accepted

    Examples:
      | action          |
      | post a password |
      | get a hash      |
