import re
import requests
import pandas as pd
import cred

def clean_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)  # remove special characters
    return filename

def build_payload(query, start=1, num=10, **params):
    """
    Function to build the payload for the Google Search API request.

    :param query: Search term
    :param start: The index of the first result to return
    :param num: Number of results to return
    :param params: Additional parameters for the API request

    :return: Dictionary containing the API request parameters
    """
    payload = {
        "key": API_KEY,
        "q": query,
        "cx": SEARCH_ENGINE_ID,
        "start": start,
        "num": num,
    }

    payload.update(params)

    return payload

def make_request(payload):
    """
    Function to send a GET request to the Google Search API and handle potential errors.

    :param payload: Dictionary containing the API request parameters

    :return: JSON response from the API
    """
    response = requests.get("https://www.googleapis.com/customsearch/v1", params=payload)

    if response.status_code != 200:
        raise Exception("Request failed")

    return response.json()

def main(query, total_results=10):
    """
    Main function to execute the script.
    """
    items = []

    pages = total_results // 10
    reminder = total_results % 10

    for i in range(pages + (1 if reminder > 0 else 0)):
        if i == pages and reminder > 0:
            payload = build_payload(query, start=i * 10, num=reminder)
        else:
            payload = build_payload(query, start=i * 10)

        response = make_request(payload)
        items.extend(response["items"])

    query_string_clean = clean_filename(query)

    df = pd.json_normalize(items)
    df.to_excel(f"Google_Search_Result_{query_string_clean}.xlsx", index=False)
    print("\nResults are successfully added to an excel sheet in the parent folder")

if __name__ == "__main__":
    API_KEY = 'AIzaSyDshhGO26W2UpJWJtiAxRIb26OqInY0AAY'
    SEARCH_ENGINE_ID = '47a6ec826ff564164'

    search_query = input("Enter the Search Query: ")
    total_results = int(input("\nHow many results from the web are required: "))
    main(search_query, total_results)
