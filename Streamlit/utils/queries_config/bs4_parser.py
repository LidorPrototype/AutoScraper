import streamlit as st
import sys
import pandas as pd
import requests
import re
import time
from bs4 import BeautifulSoup

sys.path.append('./utils')
import general_utils as g_utils


def build_bs4_tree():
    """
        Goal:
            building the screen for the bs4 (BeautifulSoup) part of the queries based 
            service and letting the user activate BeautifulSoup module after filling 
            all the needed information
    """
    # Variables
    queries_type = ""
    queries_names = []
    queries_values = []
    queries = []
    metadatas = []
    metadata_names = []
    metadata_values = []
    num_of_metadatas = 0
    num_of_queries = 0
    qu_wrong_format = False
    me_wrong_format = False
    url = st.text_input("Insert url to run on")
    # User question prompt + instructions
    st.subheader("Please provide us with a list of queries")
    # Queries
    num_of_queries = int(st.number_input('Number of queries', min_value=0, step=1))
    
    soup_str = """
        <p style='opacity: 0.55; font-size: 12px'>
        SOUP query should be: func_name(func parameters){br}
        SOUP example: find_all('p', class_='outer-text')
        </p>
    """.format(br="<br>")
    st.markdown(soup_str, unsafe_allow_html=True)
       
    if num_of_queries > 0:
        query_cols = st.columns([1, 2])
        for idx in range(1, num_of_queries + 1):
            with query_cols[0]:
                queries_names.append(st.text_input(f"Data Name {idx}", key=idx))
            with query_cols[1]:
                queries_values.append(st.text_input(f"Query {idx}:", key=idx))
        queries = {}
        for idx in range(len(queries_names)):
            queries[queries_names[idx]] = queries_values[idx]
        for item in queries:
            if queries[item] == "":
                continue
            if queries[item] != "":
                qu_wrong_format = True
                break
    g_utils.put_line_break()
    # Allow the user to prompt to unsert metadata as well
    _metadata_status = st.checkbox("Add metadata")
    if _metadata_status:
        # User question prompt + instructions
        st.subheader("Please provide us with a list of metadatas")
        num_of_metadatas = int(st.number_input('Number of metadatas', min_value=0, step=1))
        me_col1, me_col2 = st.columns(2)
        if num_of_metadatas > 0:
            for i in range(1, num_of_metadatas + 1):
                with me_col1:
                    metadata_names.append(st.text_input(f"Metadata {i}", key=i))
                with me_col2:
                    metadata_values.append(st.text_input(f"Value {i}", key=i))
            for idx in range(len(metadata_names)):
                if metadata_names[idx] == "" and metadata_values[idx] == "":
                    continue
                if metadata_names[idx] == "" or metadata_values[idx] == "":
                    me_wrong_format = True
                    break
                metadatas.append((metadata_names[idx], metadata_values[idx]))
    g_utils.put_line_break()
    if num_of_queries > 0 or num_of_metadatas > 0:
        if not qu_wrong_format or not me_wrong_format:
            flags_cols = st.columns([1, 1, 1, 1])
            with flags_cols[0]:
                remove_tags = st.checkbox("Remove html tags")
            with flags_cols[1]:
                remove_char = ""
                split_lines = st.checkbox("Split lines")
                remove_empty_cells = False
                if split_lines:
                    remove_empty_cells = st.checkbox("Remove empty cells")
                    with flags_cols[2]:
                        remove_chars_radio = st.radio("Remove cells with 1 char", ("Specific single char", "All single chars"))
                        if remove_chars_radio == "Specific single char":
                            remove_char = st.text_input("Char:")
                        elif remove_chars_radio == "All single chars":
                            remove_char = "ALL"
            if url != "":
                g_utils.put_line_break()
                run_queries_cb = st.checkbox("Run my credentials", key="query_metadata")
                if run_queries_cb:
                    fetched_already = False
                    fetch_func = activate_soup_logic
                    if "fetch_func" in locals() or "fetch_func" in globals():
                        try:      
                            flags = {
                                "del_tags": remove_tags, 
                                "split_lines": split_lines, 
                                "del_empty": remove_empty_cells, 
                                "del_char": remove_char
                            }
                            queries_result = fetch_func(url, queries, metadatas, flags)
                            st.write(queries_result)
                        except Exception as e:
                            exc = f"The credentials resulted with an {type(e).__name__}, that mean that you have a {e.args[0]}"
                            st.warning(exc)
                    if fetched_already:
                        create_process()
        else:
            st.caption("Please fill all the pairs")
            

def activate_soup_logic(URL, _queries, _metadatas, _flags):
    """
        Goal:
            Parsing the user queries and metadata using bs4 - BeautifulSoup
        Parameters:
            :param URL: url (str) to be scraped
            :param _queries: dictionary of the queries (name, value)
            :type _queries: dictionary
            :param _metadatas: list of the metadata (name, value)
            :type _metadatas: list of tuples
            :param _flags: list of flags representing extra steps to apply 
                            on the user result data
    """
    loading_gif = st.image('utils/media/gifs/soup1.gif')
    time.sleep(2.25)
    result_df = pd.DataFrame()
    try:
        page = requests.get(URL)
    except Exception:
        return "We couldn't reach the given url"
    soup = BeautifulSoup(page.content, 'html.parser')
    for item in _queries:
        query_res = eval("soup." + _queries[item])
        if _flags["del_tags"]:
            CLEANR = re.compile('<.*?>')
            def apply_sub(value):
                return re.sub('\n+', '\n', re.sub(' +', ' ', re.sub(CLEANR, '', str(value)).strip()))
            query_res = [apply_sub(item) for item in query_res]
        if _flags["split_lines"]:
            query_res = query_res.split('\n')
        if _flags["del_empty"]:
            query_res = [item for item in query_res if item.strip() != ""]
        if _flags["del_char"] != "":
            if len(_flags[3]) <= 1:
                query_res = [item for item in query_res if item.strip() != _flags[3]]
            elif _flags[3] == "ALL":
                query_res = [item for item in query_res if len(item.strip()) != 1]
        
        query_res = list(query_res)
        query_res = [str(item) for item in query_res]
        result_df[item] = query_res
        
    loading_gif.empty()
    return result_df




