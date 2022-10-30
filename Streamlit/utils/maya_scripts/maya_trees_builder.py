import sys
import shutil
import streamlit as st
import pandas as pd
from maya_downloader import activate_maya_logic

# All place using it are commented for now, it uses the process creation method
# sys.path.append('./utils')
# import general_utils as g_utils


def build_html_tree(from_pad, to_pad):
    """
        Goal:
            Building the screen for the html download from the maya website,
            allowing the user to download the report form maya in various formats
        Parameters:
            :param from_pad: Padding 'for' the from date
            :param to_pad: Padding for the 'to' text
        Return:
            :return unwanted_path: path to the files that are meant to be deleted
    """
    fetched = False
    html_cols = st.columns(3)
    with html_cols[0]:
        en_report_name = st.text_input("Enter report name in English")
        from_date = (st.text_input("From Date") + from_pad)
    with html_cols[1]:
        he_report_name = st.text_input("Enter report name in Hebrew")
        to_date = (st.text_input("To Date") + to_pad)
    with html_cols[2]:
        html_type = st.selectbox('Select Format',('HTML', 'JSON', 'CSV'))
    get_html_reports = st.button("Render my request")
    if get_html_reports:
        if he_report_name != '' and en_report_name != '' and from_date != '' and to_date != '':
            if html_type == "HTML":
                loading_gif = st.image('utils/media/gifs/loading_with_rocket1.gif')
                file_name = f"Results/HTML/{en_report_name}_html_format.zip"
                activate_maya_logic(file_name[:-4], he_report_name, from_date, to_date, "HTML")
                _label = "Download Reports - HTML"
                shutil.make_archive(file_name[:-4], file_name[-3:], file_name[:-4])
                loading_gif.empty()
                with open(file_name, 'rb') as zippy:
                    download_btn = st.download_button(label=_label, data=zippy, file_name=file_name, mime="application/zip")
                unwanted_path = (file_name[:-4], '')
                fetched = True
            elif html_type == "JSON":
                loading_gif = st.image('utils/media/gifs/loading_with_rocket1.gif')
                file_name = f"Results/HTML/{en_report_name}_json_format.zip"
                activate_maya_logic(file_name[:-4], he_report_name, from_date, to_date, "JSON")
                _label = "Download Reports - JSON"
                shutil.make_archive(file_name[:-4], file_name[-3:], file_name[:-4])
                loading_gif.empty()
                with open(file_name, 'rb') as zippy:
                    download_btn = st.download_button(label=_label, data=zippy, file_name=file_name, mime="application/zip")
                unwanted_path = (file_name[:-4], '')
                fetched = True
            elif html_type == "CSV":
                gifs_cols = st.columns(3)
                with gifs_cols[0]:
                    loading_gif0 = st.image('utils/media/gifs/loading_with_rocket1.gif')
                file_name = f"Results/HTML/{en_report_name}_csv_format"
                _label = "Download Reports - CSV"
                csv_name_round1 = activate_maya_logic(file_name, he_report_name, from_date, to_date, "CSV", 1)
                with gifs_cols[1]:
                    loading_gif1 = st.image('utils/media/gifs/greek_loading.gif')
                csv_name_round2 = activate_maya_logic(file_name, he_report_name, from_date, to_date, "CSV", 2)
                df = pd.read_csv(csv_name_round2)
                csv_file = df.to_csv().encode('utf-8')
                download_btn = st.download_button(label=_label, data=csv_file, file_name=csv_name_round2)
                loading_gif0.empty()
                loading_gif1.empty()
                unwanted_path = (file_name, csv_name_round2)
                fetched = True
#             if fetched:
#                 g_utils.create_process()
        else:
            st.caption("Please fill all the empty cells")
            print(unwanted_path)
        return unwanted_path
#  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
def build_pdf_tree(from_pad, to_pad):
    """
        Goal:
            Building the screen for the pdf download from the maya website,
            allowing the user to download the report form maya in pdf format
        Parameters:
            :param from_pad: Padding 'for' the from date
            :param to_pad: Padding for the 'to' text
        Return:
            :return unwanted_path: path to the files that are meant to be deleted
    """
    pdf_cols = st.columns(2)
    with pdf_cols[0]:
        en_report_name = st.text_input("Enter report name in English")
        from_date = (st.text_input("From Date") + from_pad)
    with pdf_cols[1]:
        he_report_name = st.text_input("Enter report name in Hebrew")
        to_date = (st.text_input("To Date") + to_pad)
    get_pdf_reports = st.button("Render my request")
    if get_pdf_reports:
        if he_report_name != '' and en_report_name != '' and from_date != '' and to_date != '':
            center_with_cols = st.columns(3)
            with center_with_cols[1]:
                loading_gif = st.image('utils/media/gifs/turning_from_digital_doc.gif')
            file_name = f"Results/PDF/{en_report_name}_pdf_format.zip"
            activate_maya_logic(file_name[:-4], he_report_name, from_date, to_date, "PDF")
            _label = "Download Reports - PDF"
            shutil.make_archive(file_name[:-4], file_name[-3:], file_name[:-4])
            loading_gif.empty()
            with open(file_name, 'rb') as zippy:
                download_btn = st.download_button(label=_label, data=zippy, file_name=file_name, mime="application/zip")
            unwanted_path = (file_name[:-4], '')
#             g_utils.create_process()
        return unwanted_path
#  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


def maya_tree_builder(type_of_tree):
    """
        Goal:
            Controller function to decide whether building an html hadnler screen or a 
            pdf handler screen
        Parameters:
            :param type_of_tree: str flag indicates if we should build an html tree or pdf tree
    """
    from_pad = "T22:00:00.000Z"
    to_pad = "T21:00:00.000Z"
    path_to_delete = ""
    if type_of_tree == "PDF":
        path_to_delete = build_pdf_tree(from_pad, to_pad)
    elif type_of_tree == "HTML":
        path_to_delete = build_html_tree(from_pad, to_pad)
    return path_to_delete
