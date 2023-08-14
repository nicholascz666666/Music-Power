import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send a GET request to the website
    response = requests.get(url)

    # If the GET request is successful, the status code will be 200
    if response.status_code != 200:
        print(f'Failed to get content of URL: {url}, status code: {response.status_code}')
        return None

    # Get the content of the response
    webpage_content = response.content

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(webpage_content, 'html.parser')

    # Now you can navigate the HTML tree, for example to get all the headers:
    headers = [header.text for header in soup.find_all('h1')]

    return headers

# Use the function
url = 'https://soundraw.io/create_music'
headers = scrape_website(url)
print(headers)
