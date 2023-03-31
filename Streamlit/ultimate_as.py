import streamlit as st
import sys

sys.path.append('./utils')
import general_utils as g_utils
sys.path.append('./utils/services')
from build_as_raw_data import scraping_raw_data
from build_api_calls import api_calls
from build_maya_handler import maya_downloader
from build_queries_based import queries_based

# ------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------> Problems & TODO Area <---------------------------------------------
# ------------------------------------------------------Start-------------------------------------------------------
#  - Program flow is at the bottom
#  TODO:
#     - bs4_parser: Only flags["del_tags"] tested, 
#                   Need to test the rest as well
#     - queries_based(): Need to make the table not disappear when the user click on the download
#                        option (like I did in the raw data scraping)
#     - Create a dag template on the api_calls service only for now, it should be a parent dag that takes 
#        argument from a configuration file and run every morning based on the configuration file for it's 
#        paths (what to take, form where, to where, etc...).
#  Problems:
#     - api_calls: asking a csv, it arrives as a json and is being converted to a one line csv auto by the
#                  tensorflow library, convert it back to json in order to convert it properly back to csv
#        - api_calls: there is a place that cuase a one in a life time index error, find it and fix it
# -------------------------------------------------------End--------------------------------------------------------
# ---------------------------------------------> Problems & TODO Area <---------------------------------------------
# ------------------------------------------------------------------------------------------------------------------


#  ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
#  ><-------------------------------------------> Program Flow <-------------------------------------------><
#  ><--------------------------------------> Controlled from Sidebar <-------------------------------------><
#  ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
company_name = 'Bank of Israel - AutoScraper'
g_utils.outside_page_configurations(company_name, 'utils/media/boi_logo.png')
# Sidebar Menu
buttons_Style = st.sidebar.markdown("""
<style>
div.stButton > button:first-child {filter: drop-shadow(0 0 0.2rem #000);text-shadow: none!important;border:3px; border-style:solid; border-color:#FF0000;font-style: italic;}
</style>""", unsafe_allow_html=True)
contact_us_btn = st.sidebar.button("For support please contact the amazing DSG team")
if contact_us_btn:
    g_utils.apply_notification(icon_path="\\utils\\media\\boi_logo_circle.ico")
# Services
services_names = ('Scraping raw data', 'API calls', 'Maya downloader', 'Queries Based')
services_flags = ('Raw', 'API', 'Maya', 'Queries')
service_chosen = st.sidebar.radio("Chose your service", services_names)
# Title + Logo
entrance_cols = st.columns([1,5])
with entrance_cols[0]:
    st.image('utils/media/boi_logo.png', width=85)
with entrance_cols[1]:
    st.title(company_name) 
    g_utils.put_line_break()
# Application Flow Handler
if service_chosen == services_names[0]:
    scraping_raw_data()
    g_utils.sidebar_examples("Raw")
elif service_chosen == services_names[1]:
    api_calls()
    g_utils.sidebar_examples("API")
elif service_chosen == services_names[2]:
    maya_downloader()
    g_utils.sidebar_examples("Maya")
elif service_chosen == services_names[3]:
    queries_based()
    g_utils.sidebar_examples("Queries")

