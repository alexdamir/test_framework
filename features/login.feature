Feature: User Login
  As a user
  I want to be able to log in to the application
  So that I can access my account

  Background:
    Given I am on the login page

  Scenario: Successful login with valid credentials
    When I enter username "testuser" and password "testpass"
    And I click the login button
    Then I should be successfully logged in

  Scenario: Login with invalid credentials
    When I enter username "invalid" and password "invalid"
    And I click the login button
    Then I should see an error message "Invalid username or password"

  Scenario Outline: Login with various invalid credentials
    When I enter username "<username>" and password "<password>"
    And I click the login button
    Then I should see an error message "<error_message>"

    Examples:
      | username | password | error_message              |
      | ""       | "pass"   | Username is required       |
      | "user"   | ""       | Password is required       |
      | ""       | ""       | Username and password required |
