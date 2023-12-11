from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from keywords import indian_legal_keywords
import nltk
from urllib.parse import urlparse
# nltk.download('punkt')
from nltk.tokenize import word_tokenize,sent_tokenize

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

# Set to store visited domains
visited_domains = set()

# Loop through the first three search result links
for result_index in range(2):
    try:
        # Wait for up to 10 seconds for the element to be present
        result_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'.tF2Cxc a:nth-child({result_index + 1})'))
        )
        # Get the href attribute of the link
        link_href = result_link.get_attribute('href')
        
        # Parse the URL to extract the domain
        domain = urlparse(link_href).netloc
        
        # Skip links leading to Wikipedia if already visited
        if 'wikipedia.org' in domain and domain in visited_domains:
            continue

        # Add the domain to the set of visited domains
        visited_domains.add(domain)

        # Click on the link
        result_link.click()
    except Exception as e:
        print(f"Error: {e}")

    # Pause for a moment to let the page load
    time.sleep(2)

    # Get the HTML source code of the page
    html_source = driver.page_source

    # Parse the HTML source code
    soup = BeautifulSoup(html_source, 'html.parser')

    result_paragraph = ""
    count = 0
    # Extract paragraphs containing any of the tokens
    for p_tag in soup.find_all('p'):
        paragraph_text = p_tag.get_text()
        count += 1
        if any(token.lower() in paragraph_text.lower() for token in tokens):
            print(paragraph_text)
            result_paragraph += paragraph_text + "\n"
        if count == 10:
            break 

        # Go back to the search results page for the next iteration
    driver.back()
    time.sleep(2)  # Pause for a moment before moving to the next result
		
# Quit the WebDriver
driver.quit()

######################SPACY & NLTK#########################

from collections import Counter
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.tokenize import sent_tokenize,word_tokenize

def extract_important_keywords(query):
    # Load spaCy model for English
    nlp = spacy.load("en_core_web_sm")

    # Tokenize the query
    doc = nlp(query)

    # Identify important keywords (non-stopwords) related to Indian legal domain
    important_keywords = [token.text for token in doc if token.text.lower() not in STOP_WORDS]

    # Further filter important keywords based on legal domain knowledge
    query_tokens = word_tokenize(search_query)
    legal_keywords = query_tokens # Add more as needed
    important_legal_keywords = [kw for kw in important_keywords if kw.lower() in legal_keywords]

    return important_legal_keywords


def rank_sentences_by_keyword_match(query, sentences):
    important_keywords = extract_important_keywords(query)
    sentence_scores = []

    for sentence in sentences:
        sentence_tokens = re.findall(r'\b\w+\b', sentence.lower())
        keyword_matches = Counter(token for token in sentence_tokens if token in important_keywords)
        sentence_score = sum(keyword_matches.values())
        sentence_scores.append((sentence, sentence_score))

    # Sort sentences by the number of matched keywords in descending order
    ranked_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
    return ranked_sentences

# Example usage
query = search_query
# Define a custom rule to split sentences
custom_sentence_splitter = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')

# Use the custom rule to split sentences
result_sentences = custom_sentence_splitter.split(result_paragraph)
# result_sentences = sent_tokenize(result_paragraph)
print(result_sentences)
# Rank sentences based on keyword matching
ranked_sentences = rank_sentences_by_keyword_match(query, result_sentences)

# Print the ranked sentences
final_result = ""
for sentence, score in ranked_sentences:
    print(f"Score: {score}, Sentence: {sentence}")
    if score > 0:
        final_result += sentence

print('FINAL RESULT : ')
print(final_result)


