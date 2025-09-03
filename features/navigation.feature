Feature: Website Navigation
  As a user
  I want to navigate through the website
  So that I can access different pages and features

  Background:
    Given I am on the "home" page

  Scenario: Navigate to different pages using navigation menu
    When I click the link "Login"
    Then I should be on the "login" page
    And the page title should be "Login"

  Scenario: Navigate using browser controls
    Given I navigate to "/dashboard"
    When I go back in browser history
    Then I should be on the "home" page
    When I go forward in browser history
    Then I should be on the "dashboard" page

  Scenario: Page refresh functionality
    Given I am on the "dashboard" page
    When I refresh the page
    Then I should be on the "dashboard" page
    And the element "#main-content" should be visible

  Scenario: Wait for dynamic content
    Given I am on the "dashboard" page
    When I click the button "Load Data"
    And I wait for the element ".loading-spinner" to disappear
    Then the element ".data-table" should be visible
    And the element ".data-table" should contain text "Data loaded successfully"

  Scenario: Navigation with hover effects
    When I hover over "User Menu"
    Then the element ".dropdown-menu" should be visible
    When I click the link "Profile"
    Then I should be on the "profile" page

  Scenario Outline: Navigate to various pages
    When I click the link "<link_text>"
    Then I should be on the "<expected_page>" page
    And the current URL should contain "<url_fragment>"

    Examples:
      | link_text | expected_page | url_fragment |
      | About     | about        | /about       |
      | Contact   | contact      | /contact     |
      | Services  | services     | /services    |
      | Blog      | blog         | /blog        |