from behave import given, when, then
from features.support.page_objects.base_page import BasePage


@given('I navigate to "{url}"')
def step_navigate_to_url(context, url):
    """Navigate to a specific URL"""
    base_page = BasePage(context.page)
    full_url = url if url.startswith('http') else f"{context.config.base_url}{url}"
    base_page.navigate_to(full_url)
    base_page.wait_for_load_state()


@when('I go back in browser history')
def step_go_back(context):
    """Navigate back in browser history"""
    context.page.go_back()


@when('I go forward in browser history')
def step_go_forward(context):
    """Navigate forward in browser history"""
    context.page.go_forward()


@when('I refresh the page')
def step_refresh_page(context):
    """Refresh the current page"""
    context.page.reload()


@when('I click the link "{link_text}"')
def step_click_link(context, link_text):
    """Click a link by its text"""
    context.page.click(f"a:has-text('{link_text}')")


@when('I click the button "{button_text}"')
def step_click_button(context, button_text):
    """Click a button by its text"""
    context.page.click(f"button:has-text('{button_text}')")


@when('I click the element with id "{element_id}"')
def step_click_by_id(context, element_id):
    """Click an element by its ID"""
    context.page.click(f"#{element_id}")


@when('I click the element with class "{class_name}"')
def step_click_by_class(context, class_name):
    """Click an element by its class"""
    context.page.click(f".{class_name}")


@when('I hover over "{element_text}"')
def step_hover_element(context, element_text):
    """Hover over an element"""
    context.page.hover(f"text={element_text}")


@when('I scroll to "{element_text}"')
def step_scroll_to_element(context, element_text):
    """Scroll to an element"""
    element = context.page.locator(f"text={element_text}")
    element.scroll_into_view_if_needed()


@when('I wait for "{seconds}" seconds')
def step_wait_seconds(context, seconds):
    """Wait for a specified number of seconds"""
    context.page.wait_for_timeout(int(seconds) * 1000)


@when('I wait for the element "{selector}" to appear')
def step_wait_for_element(context, selector):
    """Wait for an element to appear"""
    context.page.wait_for_selector(selector, timeout=30000)


@when('I wait for the element "{selector}" to disappear')
def step_wait_for_element_hidden(context, selector):
    """Wait for an element to disappear"""
    context.page.wait_for_selector(selector, state="hidden", timeout=30000)


@then('I should be on the "{expected_page}" page')
def step_verify_current_page(context, expected_page):
    """Verify current page by URL pattern"""
    url_patterns = {
        "home": "",
        "login": "/login",
        "dashboard": "/dashboard",
        "profile": "/profile",
        "settings": "/settings"
    }

    expected_pattern = url_patterns.get(expected_page.lower(), f"/{expected_page}")
    current_url = context.page.url
    assert expected_pattern in current_url, \
        f"Expected to be on '{expected_page}' page (URL containing '{expected_pattern}'), but current URL is '{current_url}'"


@then('the page title should be "{expected_title}"')
def step_verify_page_title(context, expected_title):
    """Verify page title"""
    actual_title = context.page.title()
    assert expected_title in actual_title, \
        f"Expected title to contain '{expected_title}', but actual title is '{actual_title}'"


@then('the element "{selector}" should be visible')
def step_verify_element_visible(context, selector):
    """Verify an element is visible"""
    assert context.page.is_visible(selector), f"Element '{selector}' is not visible"


@then('the element "{selector}" should not be visible')
def step_verify_element_not_visible(context, selector):
    """Verify an element is not visible"""
    assert not context.page.is_visible(selector), f"Element '{selector}' is visible but shouldn't be"


@then('the element "{selector}" should contain text "{expected_text}"')
def step_verify_element_text(context, selector, expected_text):
    """Verify element contains specific text"""
    actual_text = context.page.text_content(selector) or ""
    assert expected_text in actual_text, \
        f"Expected element '{selector}' to contain '{expected_text}', but actual text is '{actual_text}'"


@then('the current URL should contain "{url_fragment}"')
def step_verify_url_contains(context, url_fragment):
    """Verify current URL contains a specific fragment"""
    current_url = context.page.url
    assert url_fragment in current_url, \
        f"Expected URL to contain '{url_fragment}', but current URL is '{current_url}'"


@then('I should see a link to "{link_text}"')
def step_verify_link_exists(context, link_text):
    """Verify a link with specific text exists"""
    link_selector = f"a:has-text('{link_text}')"
    assert context.page.is_visible(link_selector), f"Link with text '{link_text}' not found"


@then('I should see a button labeled "{button_text}"')
def step_verify_button_exists(context, button_text):
    """Verify a button with specific text exists"""
    button_selector = f"button:has-text('{button_text}')"
    assert context.page.is_visible(button_selector), f"Button with text '{button_text}' not found"