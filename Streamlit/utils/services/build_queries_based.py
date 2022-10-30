import streamlit as st
import sys

sys.path.append('./utils')
import general_utils as g_utils
sys.path.append('./utils/queries_config')
from scrapy_parser import build_xpath_tree
from bs4_parser import build_bs4_tree


#  <<<<<<<<<<<<<<<<<<<<<<<<<<<<< Run user based quesries and download data >>>>>>>>>>>>>>>>>>>>>>>>>>>>
def queries_based():
    """
        Goal:
            Creating a screen for the user to download data from a desired url, using queries.
            This is a screen for more advanced users, it allows the user to provide us 
            with BeautifulSoup queries and command, and also an xpath to be used with 
            the Scrapy library.
    """
    # Let the user choose the sub-service        
    chosen_service = st.radio(label = 'Choose Service', options = ['XPATH','BS4'], key='radio-scrapy-bs4')    
    g_utils.put_line_break()
    if chosen_service == 'XPATH':
        build_xpath_tree()
    elif chosen_service == 'BS4':
        build_bs4_tree()
#  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

