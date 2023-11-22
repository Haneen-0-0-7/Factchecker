import re
import requests
import pandas as pd
import cred

def clean_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)  # remove special characters
    return filename


def build_payload(query, start=1, num=10, date_restrict="ml", **params):
    """
    Function to build the payload for the Google Search API request.

    :param query: Search term

    :param start: The index of the first result to return

    :param link_site: Specifies that all search results should contain a link to a particular URL :param search_type: Type of search (default is undefined, 'IMAGE' for image search)

    :param date_restrict: Restricts results based on recency (default is one month '1')

    :param params: Additional parameters for the API request

    :return: Dictionary containing the API request parameters
    """
    payload = {
        "key": API_KEY,
        "q": query,
        "cx": SEARCH_ENGINE_ID,
        "start": start,
        "num": num,
        "dateRestrict": date_restrict,
    }

    payload.update(params)

    return payload



def make_request(payload):
    """
    Function to send a GET request to the Google Search API and handle potential errors.

    :param payload: Dictionary containing the API request parameters

    :return: JSON response from the API

    """

    response = requests.get(
        "https://www.googleapis.com/customsearch/v1", params=payload
    )

    if response.status_code != 200:
        raise Exception("Request failed")

    return response.json()


def main(query, result_total=10):
    """
    Main function to execute the script.
    """
    items = []

    reminder = result_total % 10

    if reminder > 0:
        pages = (result_total // 10) + 1

    else:
        pages = result_total // 10

    for i in range(pages):
        if pages == i + 1 and reminder > 0:
            payload = build_payload(query, start=(i + 1) * 10, num=reminder)

        else:
            payload = build_payload(query, start=(i + 1) * 10)

        response = make_request(payload)

        items.extend(response["items"])

    query_string_clean = clean_filename(query)

    df = pd.json_normalize(items)
    df.to_excel("Google Search Result_{0}.xlsx".format(query_string_clean), index=False)
    print("\nResults are succesfully added to an excel sheet in the parent folder")

if __name__ == "__main__":
    API_KEY = cred.google_search_api_key
    SEARCH_ENGINE_ID = cred.google_search_engine_id

    search_query=input("Enter the Search Query :")
    total_results=int(input("\nHow much pages from web is required :"))
    main(search_query, total_results)