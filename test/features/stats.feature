Feature: Stats endpoint basic tests

  Scenario: Stats start empty
    When the endpoint processes a request for stats
    Then the "TotalRequests" value is 0
    And the "AverageTime" value is 0

  Scenario: Stats after posting are accurate
    When the endpoint processes multiple password posts and hash retrievals
    And the endpoint processes a request for stats
    Then the request count matches the posted count
    And the average time value in ms is less than average password cycle time
