import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def login_website(url):
    # # Prepare login data
    # login_data = {
    #     'username': "1209794350cz666@gmail.com",
    #     'password': "Xy@7E9M6#u7x6!y",
    # }

    # # Initialize a Session
    # with requests.Session() as s:
    #     try:
    #         # Send a POST request to the login url with your credentials
    #         response = s.post(url, data=login_data)

    #         # Check if login was successful by examining the response or the content of response
    #         if response.status_code == 200:  # HTTP Status Code for "OK"
    #             print('Login successful!')
    #             return s  # Return session if needed for further requests as a logged-in user
    #         else:
    #             print('Login failed, check your credentials and the url')
    #             return None

    #     except RequestException as e:
    #         # Handle request errors
    #         print(f'Request failed: {str(e)}')
    #         return None
    driver = webdriver.Firefox()  # Substitute with your preferred browser

    driver.get(url)

    # Replace 'username-field' and 'password-field' with the correct IDs or use other Selenium methods to locate the fields
    username_field = driver.find_element_by_id('email-sign-in')
    password_field = driver.find_element_by_id('password-sign-in')

    username_field.send_keys("1209794350cz666@gmail.com")
    password_field.send_keys("Xy@7E9M6#u7x6!y")

    # Replace 'login-button' with the correct ID or use other Selenium methods to locate the button
    login_button = driver.find_element_by_xpath('//input[@value="Log in"]')
    login_button.click()

    # Wait for the page to load after login, adjust the condition according to your case
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'element_after_login')))

    return driver



def scrape_website(url):
    # # Use the session to send a GET request to the page url
    # page = session.get(url)

    # # Parse the page with BeautifulSoup
    # soup = BeautifulSoup(page.content, 'html.parser')


    # for link in soup.find_all('a'):
    #     print(link.get('href'))

    # Configure Firefox options
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", "web_craw\\download\\")
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")  # Change this to match the MIME type of your files
    
    driver = webdriver.Firefox(options=options)  # Substitute with your preferred browser

    driver.get(url)

    # Replace 'username-field' and 'password-field' with the correct IDs or use other Selenium methods to locate the fields
    username_field = driver.find_element_by_id('email-sign-in')
    password_field = driver.find_element_by_id('password-sign-in')

    username_field.send_keys("1209794350cz666@gmail.com")
    password_field.send_keys("Xy@7E9M6#u7x6!y")

    # Replace 'login-button' with the correct ID or use other Selenium methods to locate the button
    login_button = driver.find_element_by_xpath('//input[@value="Log in"]')
    login_button.click()

    # Wait for the page to load after login, adjust the condition according to your case
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'element_after_login')))
    
    # Find the download buttons
    download_icons = driver.find_elements_by_css_selector('.btn-pool.clickable.has-tooltip')[:15]
    # Now download_icons is a list, and you can interact with each button. For example:
    for icon in download_icons:
        icon.click()

    driver.quit()
# print(login_website('https://soundraw.io/users/sign_in'))
scrape_website("https://soundraw.io/edit_music?length=180&tempo=low,normal,high&mood=Happy")