from behave import given, when, then
from features.support.page_objects.login_page import LoginPage

@given('I am on the login page')
def step_navigate_to_login(context):
    login_page = LoginPage(context.page)
    login_page.navigate_to(f"{context.config.base_url}/login")
    context.login_page = login_page

@when('I enter username "{username}" and password "{password}"')
def step_enter_credentials(context, username, password):
    context.login_page.login(username, password)

@when('I click the login button')
def step_click_login(context):
    context.login_page.click(context.login_page.LOGIN_BUTTON)

@then('I should see an error message "{error_message}"')
def step_verify_error_message(context, error_message):
    actual_error = context.login_page.get_error_message()
    assert error_message in actual_error, f"Expected error '{error_message}' not found in '{actual_error}'"

@then('I should be successfully logged in')
def step_verify_successful_login(context):
    # Wait for redirect after login
    context.page.wait_for_url("**/dashboard", timeout=10000)
    assert "/dashboard" in context.page.url
