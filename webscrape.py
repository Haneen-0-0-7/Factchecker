from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import nltk
# nltk.download('punkt')
from nltk.tokenize import word_tokenize

# Define the website to perform a Google search
google_search_url = 'https://www.google.com/search?q='

# Take user input for the search query
search_query = input("Enter your search query: ")

# Concatenate the search query with the Google search URL
google_search_url += search_query

# Tokenize the search query
tokens = word_tokenize(search_query)

# Path to the ChromeDriver executable
path = r'D:\chrome driver\chromedriver-win64\chromedriver.exe'

chrome_options = Options()

# Specify the path to the ChromeDriver executable
chrome_options.add_argument(f'--webdriver-path={path}')

# Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)

# Open Google Chrome with the Google search URL
driver.get(google_search_url)

# Pause for a moment to let the search results load
time.sleep(2)

# Locate and click on the first search result link
try:
    # Wait for up to 10 seconds for the element to be present
    first_result_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.tF2Cxc a'))
    )
    first_result_link.click()
except Exception as e:
    print(f"Error: {e}")

# Pause for a moment to let the page load
time.sleep(2)

html_source = driver.page_source
# Parse the HTML source code
soup = BeautifulSoup(html_source, 'html.parser')

result_paragraph = ""

# Extract paragraphs containing any of the tokens
for p_tag in soup.find_all('p'):
    paragraph_text = p_tag.get_text()
    if any(token.lower() in paragraph_text.lower() for token in tokens):
        print(paragraph_text)
        result_paragraph += paragraph_text + "\n"
		
# Quit the WebDriver
driver.quit()

# if word_count + len(paragraph_text.split()) > 500:
#         break

#     # Add the paragraph to the result
#     result_paragraph += paragraph_text + "\n"
#     word_count += len(paragraph_text.split())