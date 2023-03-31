import streamlit as st
import pandas as pd
import pathlib
import shutil
from win10toast_click import ToastNotifier as TN
from PIL import Image


def apply_notification(icon_path, website_url=None):
    """
        Goal:
            Generate a custom notification to the user
        Parameter:
            :param icon_path: path to the icon that will appear on the notification
            :type icon_path: str
        Temp Parameter:
            :param website_url: a link to the website to be opened when the user click on the notification
            :type website_url: str
    """
    
    def notification_action():
        import webbrowser
        try:
            url = website_url or "https://ibb.co/5hMkTS2"
            webbrowser.open_new(url)
            print('Opening URL...')  
        except: 
            print('Failed to open URL. Unsupported variable type.')
            
    cur_path = str(pathlib.Path().resolve()) + icon_path
    toaster = TN()
    toaster.show_toast(
        "Contact us at",
        "Lidor-eliyahu.shelef@boi.org.il\nCurrently opens our icon \U0001F61B", # Image name: DSG_BOI_2.png
        icon_path=cur_path,
        threaded=True,
        callback_on_click=notification_action
    )


def outside_page_configurations(page_title, image_path):
    """
        Goal:
            Set the default page configuration
        Parameters:
            :param page_title: title of the page, application
            :param image_path: path to the image that will appear on the top of the page (website tab)
            :type: str - for both of the parameters
    """
    image_logo = Image.open(image_path)
    st.set_page_config(page_title=page_title, page_icon=image_logo)


# Puts a line break, on main screen or sidebar based on :flag:
def put_line_break(flag=0):
    """
        Generate a linebreak on the main screen / sidebar based on the flag parameter
    """
    if flag == 0:
        st.markdown("___") # Line break between two sections
    else:
        st.sidebar.markdown("___") # Line break between two sections 
        

def create_process():
    """
        This method creating the ui for creating a process in the airflow
                         ( only the ui for now )
    """
    return True # In order to not get anything - Pilot #1
    create_request_cb = st.checkbox("Create My Process!", key="create_request_cb")
    if create_request_cb:
        date_container = st.columns(3)
        day_str = "Which day should the process occur?"
        hour_str = "At which time?"
        file_type_str = "Choose file type"
        with date_container[0]:
            day = st.text_input(day_str, key="day_input")
#         with date_container[1]:
#             hour = st.text_input(hour_str, key="hour_input")
        with date_container[2]:
            if st.selectbox(file_type_str,('', 'CSV', 'JSON', 'HTML', 'MD')):
                st.write("!!!NEED TO IMPLEMENT!!!")
        email = st.text_input("Please provide an email to send the report to")
        st.caption("(Leave empty if you don't want to recieve a report about it everytime)")
        put_line_break()
        
        
def let_the_user_download_it(df_to_download, output_file_name="request_data"):
    """
        Goal:
            Allow the user to download the data in 4 different formats,
            it handle ui as well as ux
        Parameters:
            :param df_to_download: Dataframe (usually) for the user to download
            :param output_name: name of the output file, defualts to request_data
    """
    # Download data in desired
    _data = pd.DataFrame(df_to_download)
    # Different File Types
    csv_file = _data.to_csv().encode('utf-8')
    json_file = _data.to_json()
    html_file = _data.to_html()
    md_file = _data.to_markdown()
    # Download Files
    formats = 4
    formats_col = st.columns(formats)
    with formats_col[0]:
        download_csv = st.download_button("CSV", csv_file, file_name=f'{output_file_name}.csv')
    with formats_col[1]:
        download_json = st.download_button("JSON", json_file, file_name=f'{output_file_name}.json')
    with formats_col[2]:
        download_html = st.download_button("HTML", html_file, file_name=f'{output_file_name}.html')
    with formats_col[3]:
        download_md = st.download_button("MD", md_file, file_name=f'{output_file_name}.md')
        
        
def delete_unwanted(del_path):
    """
        Goal:
            Deletes everything in the given path
        Parameters:
            :param del_path: path wanted to be deleted
            :type del_path: str
    """
    directory = del_path[0]
    try:
        shutil.rmtree(directory)
    except OSError as e:
        pass # print("Error: %s - %s." % (e.filename, e.strerror))
    

def parse_headers(headers, _=True):
    """
        Goal:
            Parse a header given to us by the user in an agreed format
        Parameters:
            :param headers: the headers we get from the user
            :type headers: str
            :param _: flag to indicates the correct way to split the headers
    """
    _headers = {}
    headers = headers.split("\n")
    correct_fmt = True
    for row in headers:
        try:
            row = row.split(":")
            if _:
                _headers[row[0]] = (row[1], row[2])
            elif not _:
                _headers[row[0]] = row[1]
        except IndexError:
            correct_fmt = False
    return (_headers, correct_fmt)

        
def sidebar_examples(_):
    """
        Goal:
            Builds the sidebar menu examples, for every mode of the application
        Parameters:
            :param _: type of service we want examples for
            :type _: str
    """
    if _ == "Raw":
        put_line_break(1)
        st.sidebar.title("Scraping Examples:")
        st.sidebar.text("Url: https://www.shufersal.co.il/online/he/קטגוריות/סופרמרקט/חלב-וביצים/מעדנים-וקינוחים/c/A0110")
        side_cols = st.sidebar.columns(3)
        with side_cols[0]:
            st.subheader("Fields:")
            st.text("Title")
            st.text("Price")
        with side_cols[1]:
            st.subheader("Values:")
            st.text("מילקי בטעם וניל")
            st.text("2.90")
        put_line_break(1)
        st.sidebar.text("Url: https://www.zara.com/il/he/man-knitwear-cardigans-l685.html?v1=1886300")
        side_cols = st.sidebar.columns(3)
        with side_cols[0]:
            st.subheader("Fields:")
            st.text("שם")
            st.text("מחיר")
        with side_cols[1]:
            st.subheader("Values:")
            st.text("קרדיגן עם כיסים")
            st.text("₪ 269.00")
    elif _ == "API":
        put_line_break(1)
        st.sidebar.title("API Example:")
        st.sidebar.text("Url: http://www.imageprocessingplace.com/downloads_V3/root_downloads/image_databases/standard_test_images.zip")
        st.sidebar.text("File name: standard_test_images")
        st.sidebar.text("File format: zip")
    elif _ == "Maya":
        put_line_break(1)
        st.sidebar.title("Maya Example:")
        side_cols = st.sidebar.columns(2)
        with side_cols[0]:
            st.subheader("En Report Name:")
            st.text("HTML - Tav049")
            st.text("JSON - Tav086")
        with side_cols[1]:
            st.subheader("He Report Name:")
            st.text("ת049")
            st.text("ת086")
        st.sidebar.text("From: 2021-08-11")
        st.sidebar.text("To: 2021-09-11")
        st.sidebar.caption("CSV Time stamp:")
        st.sidebar.text("From: 2021-08-28")
        st.sidebar.text("To: 2021-09-11")
    elif _ == "Queries":
        put_line_break(1)
        st.sidebar.title("Queries Example:")
        st.sidebar.subheader("XPATH:")
        _data_examples = {
            "urls" : ['https://www.ynet.co.il/news/category/185'],
            "prefixes" : ['https://www.ynet.co.il/news/article'],
            "metadata" : {'names': ['date', 'source'], 'values': ['02-11-2021', 'ynet']},
            "queries" : {'names': ['title'], 'xpaths': ['//h1[@class="mainTitle"]/text()']}
        }
        side_cols_xpath = st.sidebar.columns([1, 2])
        with side_cols_xpath[0]:
            st.text("Urls:")
            st.text("Prefixes:")
            st.text("")
            st.text("")
            st.text("Metadata:")
            st.text("")
            st.text("")
            st.text("Queries:")
        with side_cols_xpath[1]:
            st.text(f"{_data_examples['urls'][0]}")
            st.text(f"{_data_examples['prefixes'][0]}")
            st.text(f"{_data_examples['metadata']['names'][0]}, {_data_examples['metadata']['names'][1]}")
            st.text(f"{_data_examples['metadata']['values'][0]}, {_data_examples['metadata']['values'][1]}")
            st.text(f"{_data_examples['queries']['names'][0]}")
            st.text(f"{_data_examples['queries']['xpaths'][0]}")
        st.sidebar.subheader("BS4:")
        st.sidebar.text("Url: https://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
        side_cols_bs4 = st.sidebar.columns([1, 2])
        with side_cols_bs4[0]:
            st.text("Query")
        with side_cols_bs4[1]:
            st.text("find_all('p')")
        
