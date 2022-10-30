import streamlit as st
import sys

sys.path.append('./utils')
import general_utils as g_utils
sys.path.append('./utils/maya_scripts')
from maya_trees_builder import maya_tree_builder


#  <<<<<<<<<<<<<<<<<<<< Download reports from the Maya website in different formats >>>>>>>>>>>>>>>>>>>
def maya_downloader():
    """
        Goal:
            Creating a screen for the user to download data from the maya website (the israeli 
            stock exchange website - https://maya.tase.co.il/), the data is the reports the website
            provides, in different versions and formats
    """
    unwanted_path = ''
    reports_type = st.selectbox('Which report type would you like to download?',('', 'HTML', 'PDF'))
    if reports_type != '':
        g_utils.put_line_break()
#   PDF OPTION!
    if reports_type == 'PDF':
        unwanted_path = maya_tree_builder("PDF")
#   HTML OPTION!
    elif reports_type == 'HTML':
        unwanted_path = maya_tree_builder("HTML")
    elif reports_type == '':
        st.write(reports_type + "\U0001F923 \U0001F603 Please Choose a Format \U0001F603 \U0001F923")
#  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
