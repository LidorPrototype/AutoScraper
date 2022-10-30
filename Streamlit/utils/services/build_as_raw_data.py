import streamlit as st
import pandas as pd
import time
import sys

sys.path.append('./utils')
import general_utils as g_utils
sys.path.append('./utils/auto_scraping')
from auto_scraping import Auto_Scraper


#  <<<<<<<<<<<<<<<<<<<<<<<<<<<<< Scrape data from a given website based on user wishes >>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def scraping_raw_data():
    """
        Goal:
            Creating a screen for the user to scrape the web automatically, without the need to
            know too much about the web scraping process so much
    """
    # Global Variables
    field_names = []
    field_values = []
    field_duplicates = True
    _data = ""
    _data = pd.DataFrame()
    if 'rendered' not in st.session_state:
        st.session_state['rendered'] = False
    if 'data_itself' not in st.session_state:
        st.session_state['data_itself'] = pd.DataFrame()
    if 'failed_flag' not in st.session_state:
        st.session_state['failed_flag'] = False
    #  ----------------------------------------------------------------------------------------------------------    
    # Disclouser
    st.caption("You can change the theme form the hamburger menu (on the right) \U0001F603")
    #  ----------------------------------------------------------------------------------------------------------    
    first_inputs = st.columns([4, 0.2, 1])
    # URL provider
    with first_inputs[0]:
        url = st.text_input("Enter website url", key='url_input')
    # Developer Checker
    if st.session_state['failed_flag']:
        with first_inputs[2]:
            st.write("")
            st.write("")
            developer_check = st.checkbox("Developer?")
        if developer_check:
            g_utils.put_line_break()
            developer_cols = st.columns(2)
            with developer_cols[0]:
                st.subheader("Please enter custom headers")
            with developer_cols[1]:
                st.write("")
                st.caption(" in the right format for the python language")
            custom_headers = st.text_area("Format should be: 'field_name:field_value:type_of_value', each field should be in a new line (no line indicator needed)")
            if custom_headers != "":
                new_headers, correct_format = g_utils.parse_headers(custom_headers)
                if correct_format:
                    st.write(new_headers)
                elif not correct_format:
                    st.write("Please follow the format given above...")
            st.caption("Value types: String, int, double, float, char, boolean")
    g_utils.put_line_break()
    #  ----------------------------------------------------------------------------------------------------------    
    # Get number of fields
    fields_question = 'How many fields would you like to query?'
    init_cols = st.columns(2)
    with init_cols[0]:
        numbers = int(st.number_input(fields_question, min_value=0, step=1))
    with init_cols[1]:
        dup = st.selectbox('Remove Duplicates', ('Yes', 'No'), key='duplication_status')
        if dup == 'Yes':
            field_duplicates = True
        elif dup == 'No':
            field_duplicates = False
    fields_instructions = 'For each field value it is reccomended to give more than one example, split them with a comma between them and with no spaces as such: "value1,value2", Keep in mind, the more example you give the more accurate the result shall be \U0001f604'
    st.caption(fields_instructions)
    #  ----------------------------------------------------------------------------------------------------------    
    # Create number of requested fields
    col1, col2 = st.columns(2)
    if numbers > 0:
        for i in range(1, numbers + 1):
            with col1:
                field_names.append(st.text_input(f"Field {i}", key=i))
            with col2:
                field_values.append(st.text_input(f"Value {i}", key=i))
    #  ----------------------------------------------------------------------------------------------------------    
    # Submit request + Show result
    submit_cb = st.checkbox("Scrape My Request!", key="submit_cb")
    if not st.session_state['rendered']:
        if submit_cb:
            _data = pd.DataFrame()
            if numbers <= 0:
                st.write("Please give us some filed examples sir/ma'am")
            else:
                all_elements = {}
                for idx in range(len(field_names)):
                    all_elements[field_names[idx]] = field_values[idx].split(",")
                if "" in all_elements:
                    st.write("Please fill all the empty cells sir/ma'am")
                else:
                    if not _data.empty:
                        data_frame = st.dataframe(_data)
                    elif _data.empty:
                        loading_gif = st.image('utils/media/gifs/loading_with_rocket2.gif')
                        _url = str(url).strip()
                        
                        _data = activate_raw_logic(all_elements, url, field_duplicates)
                        
                        time.sleep(0.5)
                        loading_gif.empty()
                        if not _data.empty:
                            data_frame = st.dataframe(_data)
                        else:
                            st.write("It seems we are having truble processing your request \U0001f604")
                            failure_cols = st.columns(2)
                            with failure_cols[0]:
                                st.write("If this process is important to you, you can submit a request for it via: ")
                            with failure_cols[1]:
                                fail_request_btn = st.checkbox("Submit Request", key="fail_request_request_reprocess")
                                if fail_request_btn == True:
                                    company_name = "GOD DAMN IT!" # Down not work, rerender everything!!!!
                                    st.write("Request Sent...")
                            g_utils.put_line_break()
                            custom_headers_cols = st.columns([4,1])
                            with custom_headers_cols[0]:
                                st.write("Or if you know how to, you may submit custom headers for the request library by marking the option next to the url that will apear aftet you click the button to the right.")
                            st.session_state['failed_flag'] = True
                            with custom_headers_cols[1]:
                                developer_ok = st.button("I will")
                                if developer_ok:
                                    submit_cb = False
                        st.session_state['rendered'] = True
                        st.session_state['data_itself'] = _data
    else:
        _data = st.session_state['data_itself']
        if not _data.empty:
            data_frame = st.dataframe(_data)
    if not submit_cb:
        st.session_state['rendered'] = False
    #  ----------------------------------------------------------------------------------------------------------     
    # Download file
    if not _data.empty and submit_cb:
        g_utils.let_the_user_download_it(_data)
    # Create / Request The Process
    if not _data.empty and submit_cb:
        g_utils.create_process()
#  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


def activate_raw_logic(elements, _url, duplications_status, re_headers = None):
    """
        Goal:
            Scrape the web with the auto scraper, based on similarities and get the user everything 
            that is similar (via tag body) to the user examples
        Parameters:
            :param elements: Dictionary of all the elements, {"element_name": "element_example"}
            :param _url: A url link to scrape on
            :param duplications_status: Boolean flag to show me how to handle the duplications data
            :param re_headers: New headers to apply the logic with
        Returns:
            :return result_data: Resulting dataframe with the scraped data
            
        ToDo:
            Apply the :re_headers: param
    """
    scraper = Auto_Scraper()
    wanted_elements = []
    result_data = pd.DataFrame()
    for key, value in elements.items():
        wanted_elements.append({key: value})
    for item in wanted_elements:
        item_results = scraper.build_model(url=_url, wanted_dict=item, remove_duplicates=duplications_status)
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
    return result_data
