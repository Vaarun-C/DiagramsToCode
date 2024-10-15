from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up the Selenium WebDriver for Firefox
driver = webdriver.Firefox()  # Make sure geckodriver is in your PATH or specify the executable path

# Open the webpage
base_url = "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide"
url = base_url + "/aws-template-resource-type-ref.html"  # Replace with the actual URL
driver.get(url)

html_source = driver.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_source, 'html.parser')

# Close the browser after fetching the page source
driver.quit()
RESOURCES = {}
# Function to collect resource details using BeautifulSoup
def collectDetails(soup: BeautifulSoup):
    # Find the first element with class 'highlights'
    resources = soup.find(class_='highlights')
    
    # Find the 'ul' and iterate over its 'li' children
    list_items = resources.find('ul').find_all('li')
    
    obj = {}
    for item in list_items:
        # Find the first 'a' tag inside each list item
        link = item.find('a')
        href = link['href']  # Extract the link URL
        print(f"Link: {href}")
        obj[link.text] = base_url + href[1:]
    return obj

print(collectDetails(soup))