from behave import given, when, then
from features.support.page_objects.base_page import BasePage

@given('I am on the "{page_name}" page')
def step_navigate_to_page(context, page_name):
    url_map = {
        "login": f"{context.config.base_url}/login",
        "dashboard": f"{context.config.base_url}/dashboard",
        "home": context.config.base_url
    }
    
    base_page = BasePage(context.page)
    base_page.navigate_to(url_map.get(page_name.lower(), context.config.base_url))
    base_page.wait_for_load_state()

@when('I click on "{element_text}"')
def step_click_element(context, element_text):
    context.page.click(f"text={element_text}")

@then('I should see "{text}" on the page')
def step_verify_text_present(context, text):
    assert context.page.is_visible(f"text={text}"), f"Text '{text}' not found on page"

@then('I should be redirected to "{expected_url}"')
def step_verify_url(context, expected_url):
    current_url = context.page.url
    assert expected_url in current_url, f"Expected URL '{expected_url}' not in current URL '{current_url}'"
