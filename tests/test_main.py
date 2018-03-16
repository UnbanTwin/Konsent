"""
Intergration tests for Konsent
the tests must run in order, they are NOT independent from each other.

NOTE: In order for the tests to run firefox and geckodriver must be on $PATH.
"""

import pytest
from selenium.webdriver import Firefox


URL = 'http://127.0.0.1:5000/'

# CSS selectors
HOME_LOGIN_BUTTON = 'a.btn:nth-child(6)'
HOME_NEW_ACCOUNT_BUTTON = 'a.btn:nth-child(7)'
LOGIN_USER_FIELD = 'div.form-group:nth-child(1) > input:nth-child(2)'
LOGIN_PASS_FIELD = 'div.form-group:nth-child(2) > input:nth-child(2)'
LOGIN_CONFIG_BUTTON = '.btn'
ALERT = '.alert'
TOP_NEW_ACCOUNT = 'li.nav-item:nth-child(1) > a:nth-child(1)'
TOP_LOGIN = 'li.nav-item:nth-child(2) > a:nth-child(1)'
REGISTER_SUBMIT_BUTTON = 'input.btn'
REGISTER_CREATE_NEW_UNION_BUTTON = 'a.btn'
REGISTER_DISPLAY_NAME = '#name'
REGISTER_USERNAME = '#username'
REGISTER_PASSWORD = '#password'
REGISTER_CONFIRM_PASSWORD = '#confirm'
REGISTER_UNION = '#users_union'
REGISTER_UNION_PASSWORD = '#union_password'
UNION_REGISTER_NAME ='#union_name' 
UNION_REGISTER_PASSWORD = '#password' 
UNION_REGISTER_PASSWORD_CONFIRM = '#confirm'
UNION_REGISTER_SUBMIT_BUTTON ='.btn' 


@pytest.fixture(scope='module')
def browser():
    firefox = Firefox()
    yield firefox
    # firefox.quit()


def test_user_story_account(browser):
    # user enters the url on the browser
    browser.get(URL)
    find = browser.find_element_by_css_selector

    assert 'Konsent' in browser.title

    # she clicks the login button
    home_login_button = find(HOME_LOGIN_BUTTON)
    home_login_button.click()

    # she is redirected to the login page
    assert browser.current_url.endswith('/login')

    # she tries to login with wrong credentials
    find(LOGIN_USER_FIELD).send_keys("WRONG_USER")
    find(LOGIN_PASS_FIELD).send_keys("SOME_PASSWORD")
    find(LOGIN_CONFIG_BUTTON).click()

    # an alert popups with an error message
    alert = find(ALERT)
    assert 'This user doesnt exist' in alert.text

    # she clicks a button for creating a new account on top bar
    find(TOP_NEW_ACCOUNT).click()

    # she is redirected to the register page
    assert browser.current_url.endswith('/register')

    # she clicks create account without entering any information
    find(REGISTER_SUBMIT_BUTTON).click()

    # error text appears under the missing fields
    assert browser.current_url.endswith('/register')
    assert 'This field is required' in browser.page_source

    # she creates a new union
    find(REGISTER_CREATE_NEW_UNION_BUTTON).click()
    assert browser.current_url.endswith('/register-union')

    # she fills the required field and sumbits
    find(UNION_REGISTER_NAME).send_keys('test_union')
    find(UNION_REGISTER_PASSWORD).send_keys('test_union_password')
    find(UNION_REGISTER_PASSWORD_CONFIRM).send_keys('test_union_password')
    find(UNION_REGISTER_SUBMIT_BUTTON).click()

    # she goes back to register a new account
    find(TOP_NEW_ACCOUNT).click()
    # she fills the required fields
    find(REGISTER_DISPLAY_NAME).send_keys('test_display_name')
    find(REGISTER_USERNAME).send_keys('test_username')
    find(REGISTER_PASSWORD).send_keys('test_password')
    find(REGISTER_CONFIRM_PASSWORD).send_keys('test_password')
    # she selects her new union
    options = find(REGISTER_UNION).find_elements_by_tag_name('option')
    test_union_option = next(opt for opt in options if opt.get_property('value') == 'test_union')
    test_union_option.click()
    find(REGISTER_UNION_PASSWORD).send_keys('test_union_password')
    # she sumbits the information
    find(REGISTER_SUBMIT_BUTTON).click()

    # she logins with the correct credentials
    find(TOP_LOGIN).click()
    find(LOGIN_USER_FIELD).send_keys("test_username")
    find(LOGIN_PASS_FIELD).send_keys("test_password")
    find(LOGIN_CONFIG_BUTTON).click()
    assert 'Youve been logged in' in find(ALERT).text
