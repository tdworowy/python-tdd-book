Feature: My lists
  As a logged-in user I want to be able to see all my lists in one page, so then i can find then all after i've written them

  Scenario: Create two lists and see them on My lists page
    Given I am a logged-in user
    When I create a list with first item "Reticulate Splines"
    And I add an item "Immanetize Eschaton"
    And I create a list with first item "Buy milk"
    Then I will see a link to "My lists"
    When I click the link to "My lists"
    Then I will see a link to "Reticulate Splines"
    And  I will see a link to "Buy milk"
    When I click the link to "Reticulate Splines"
    Then I will be on the "Reticulate Splines" list page