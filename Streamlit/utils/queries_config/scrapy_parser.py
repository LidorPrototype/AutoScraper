import streamlit as st
import pandas as pd
import sys
import time

sys.path.append('./utils')
import general_utils as g_utils
sys.path.append('./utils/queries_config/auto_use_scrapy')
from auto_use_scrapy import generic_scrapy_builder as gsb


# Parsing the user queries using Scrapy library in a generic autu way
def build_xpath_tree():
    """
        Goal:
            building the screen for the xpath part of the queries based service 
            and letting the user activate the generic scrapy file after filling 
            all the needed information
    """
    st.caption("You can leave the prefix and metadata empty if you do not wish to add them")
    
    _urls = []
    _prefixes = []
    _metadata_names = []
    _metadata_values = []
    _metadata = {"names": [], "values": []}
    _queries_names = []
    _queries_xpathes = []
    _queries = {"names": [], "xpaths": []}
    
    project_name = st.text_input("Enter project name")
    st.caption("Keep in mind, spaces or special characters will be removed")
    project_name = ''.join(c for c in project_name if c.isalnum() or c == '_')
    if project_name != "":
        st.caption(f"Project name will be: {project_name}")
    g_utils.put_line_break()
    # Ask the user for urls
    num_of_urls = int(st.number_input('Number of urls', min_value=0, step=1))
    if num_of_urls > 0:
        for idx in range(1, num_of_urls + 1):
            _urls.append(st.text_input(f"Url {idx}:", key=str(idx) + " url"))
    g_utils.put_line_break()
    # Ask the user for prefixes
    num_of_prefixes = int(st.number_input('Number of prefixes', min_value=0, max_value=1, step=1))
    if num_of_prefixes > 0:
        for idx in range(1, num_of_prefixes + 1):
            _prefixes.append(st.text_input(f"Prefix {idx}:", key=str(idx) + " prefix"))
    g_utils.put_line_break()
    # Ask the user for metadata
    num_of_metadata = int(st.number_input('Number of metadata', min_value=0, step=1))
    if num_of_metadata > 0:
        metadata_cols = st.columns([1, 2])
        for idx in range(1, num_of_metadata + 1):
            with metadata_cols[0]:
                _metadata_names.append(st.text_input(f"Meta Name {idx}", key=idx))
            with metadata_cols[1]:
                _metadata_values.append(st.text_input(f"Metadata {idx}:", key=idx))
        for idx in range(len(_metadata_names)):
            _metadata["names"].append(_metadata_names[idx])
            _metadata["values"].append(_metadata_values[idx])
    g_utils.put_line_break()
    # Ask the user for queries
    num_of_queries = int(st.number_input('Number of queries', min_value=0, step=1))
    if num_of_queries > 0:
        queries_cols = st.columns([1, 2])
        for idx in range(1, num_of_queries + 1):
            with queries_cols[0]:
                _queries_names.append(st.text_input(f"Query {idx}", key=idx))
            with queries_cols[1]:
                _queries_xpathes.append(st.text_input(f"xPath {idx}:", key=idx))
        for idx in range(len(_queries_names)):
            _queries["names"].append(_queries_names[idx])
            _queries["xpaths"].append(_queries_xpathes[idx])
    g_utils.put_line_break()
        
    out_file = st.text_input("Output file name")
    st.caption("Keep in mind, it will be a csv file")
    
    if st.button("Run"):
        st.caption("If you don't get the desired output, try giving us more data to work with \U0001F603")
        _data = {
            'urls' : _urls,
            'prefixes' : _prefixes,
            'metadata' : _metadata,
            'queries' : _queries,
            'project': project_name,
            'out': (out_file or "request_data") + ".csv"
        }
        
        loading_gif = st.image('utils/media/gifs/web_surfing2.gif')
        time.sleep(0.5)        
        scrape_status, scrape_data_df = validate_activate_scrapy_logic(_data, False)
        if scrape_status == "Success":
            st.dataframe(scrape_data_df)
            g_utils.let_the_user_download_it(scrape_data_df, _data['out'][:-4])
        else:
            st.write("--> Status:  " + status)
        loading_gif.empty()

        
def validate_activate_scrapy_logic(data, _ = False):
    """
        Goal:
             a little validation (the rest is getting checked at the utils file), and
             activatin the generic scrapy and afterwards let the user download the results
        Parameters:
            :param data: dictionary holding all the wanted data from the user
             - data keys:
                - urls: list of urls the user want to scrape through
                - prefixes: list of prefixes the user would like to add (usually there is only 1)
                - metadata: dictionary holding the metadata, keys:
                    - names: list of names for the metadata values
                    - values: list of values to be put as the metadata
                - queries: dictionary holding the queries, keys:
                    - names: list of names for each query data
                    - xpaths: list of xpaths commands to be run
        Returns:
            :return status: Status of the scraping
            :return result_df or pd.DataFrame(): Result dataframe or an empty one in case of any problems
    """
    result_df = pd.DataFrame()
    output = (result_df)
    (result_df, status) = gsb.gs_builder(project=data['project'], out=data['out'],urls=data['urls'], prefixes=data['prefixes'], metadata=data['metadata'],queries=data['queries'])
    if not result_df.empty:
        return status, result_df
    else:
        return status, pd.DataFrame()
