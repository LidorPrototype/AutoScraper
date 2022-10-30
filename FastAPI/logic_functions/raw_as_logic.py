import pandas as pd

from logic_functions.auto_scraping.auto_scraping import Auto_Scraper

# Author: Lidor Eliyahu Shelef

def scrape_similarities(raw_elements, _url, duplications_status, re_headers = None):
    scraper = Auto_Scraper()
    wanted_elements = []
    result_data = pd.DataFrame()
    for key, value in raw_elements.items():
        wanted_elements.append({key: value})
    print("wanted_elements: ", wanted_elements)
    for item in wanted_elements:
        item_results = scraper.build_model(url=_url, wanted_dict=item, remove_duplicates=duplications_status)
        print("item_results: ", item_results)
        if not result_data.empty:
            if len(item_results) < len(result_data):
                item_results = item_results[:len(result_data)]
            elif len(item_results) > len(result_data):
                item_results = item_results[:len(result_data)]
        try:
            result_data[list(item.keys())[0]] = item_results
        except:
            result_data = result_data.head(len(item_results))
            result_data[list(item.keys())[0]] = item_results
    if duplications_status:
        result_data = result_data.drop_duplicates()
    print(result_data)
    print(type(result_data))
    return result_data
