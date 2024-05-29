Feature: try to login into webportal

  Scenario Outline: Login to webportal
    Given open webportal url
    When user input <username> and <password>
    Then user click on login button
    Then wait

  Examples: Login account
    | username                   | password |
    | phuong24feb1@gigacover.com | Test1234 |

