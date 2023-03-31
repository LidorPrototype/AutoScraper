# Start of file.
# Author: Lidor Eliyahu Shelef
# import json
import json
import os
import pandas as pd


# Constant Keys 
ACCESS_KEY = "@-@-Prototype-@-@"
DSG_KEY = "@@DSG@@"
BS_KEY = "@RT5&rM^MFs^_@"
MAYA_HTML_KEY = "HTML"
MAYA_JSON_KEY = "JSON"
MAYA_CSV_KEY = "CSV"
MAYA_PDF_KEY = "PDF"
PDF_ALL_KEY = "all"
PDF_TEXT_KEY = "text"
PDF_TABLES_KEY = "tables"
# Constant Flags
AUTOSCRAPER_FLAG = "AUTOSCRAPER"
GET_FILE_FLAG = "GET_FILE"
POST_FILE_FLAG = "POST_FILE"
MAYA_FLAG = "MAYA"
QUERIES_XPATH_FLAG = "QUERIES_XPATH"
PDF_PARSER_FLAG = "PDF_PARSER"
AZURE_DATALAKE_FLAG = "AZURE_DATALAKE"
# Azure Datalake Functionalities
AZURE_FUNCTIONS = [
    'list_all',
    'create_request',
    'update_request',
    'delete_request',
    'approve_request',
    'disable_request',
    'delete@all',
    'restart_default'
]


def ensure_dir(folder):
    """
        If the directory :folder: does not exists, create it
    """
    # _folder = f"download_files/{folder}"
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
    except OSError as e:
        raise


def check_data_validity(file_name, service_type):
    is_valid = False
    v_msg = ""
    try:
        if service_type == "HTML" or service_type == "JSON" or service_type == "PDF":
            num_of_files = len(os.listdir(file_name))
            if num_of_files <= 0:
                v_msg = "No data found for this search, sorry mate!"
            else:
                is_valid = True
        elif service_type == "CSV":
            df = pd.read_csv(file_name)
            if df.shape[0] <= 1:
                v_msg = "No data found for this search, sorry mate!"
            else:
                is_valid = True
        return is_valid, v_msg
    except:
        return False, "Some Exception Happaned mate!"


def get_examples(type_of_service):
    example = ""
    if type_of_service == AUTOSCRAPER_FLAG:
        example = """
            {
                "raw_model": {
                    "url": "https://www.shufersal.co.il/online/he/קטגוריות/סופרמרקט/חלב-וביצים/מעדנים-וקינוחים/c/A0110",
                    "duplications": true,
                    "parameters": {
                        "Title": [
                            "מילקי בטעם וניל"
                        ],
                        "Price": [
                            "2.90"
                        ]
                    }
                }
            }
        """
    elif type_of_service == GET_FILE_FLAG:
        example = """
            {
                "Add the following to the url path": "get_file?api_link=http://www.imageprocessingplace.com/downloads_V3/root_downloads/image_databases/standard_test_images.zip&file_name=standard_test_images.zip"
            }
        """
    elif type_of_service == POST_FILE_FLAG:
        example = """
            {
                "api_link": "http://www.imageprocessingplace.com/downloads_V3/root_downloads/image_databases/standard_test_images.zip",
                "file_name": "standard_test_images.zip"
            }
        """
    elif type_of_service == MAYA_FLAG:
        example = """
            {
                "GET":
                    {
                        "Add the following to the url path": "get_maya?service_type=HTML&eng_report=Tav049&heb_report=ת049&start_date=2021-08-11&end_date=2021-08-21&inner_format=HTML&example=N"
                    },
                "POST":
                    {
                        "maya_model": {
                            "service_type": "HTML",
                            "eng_report": "Tav049",
                            "heb_report": "ת049",
                            "start_date": "2021-08-11",
                            "end_date": "2021-08-21",
                            "inner_format": "HTML"
                        }
                    }
            }
        """
    elif type_of_service == QUERIES_XPATH_FLAG:
        example = """
            {
                "queries_model": {
                    "urls": [
                        "https://www.ynet.co.il/news/category/185"
                    ],
                    "prefixes": [
                        "https://www.ynet.co.il/news/article"
                    ],
                    "metadata": {
                        "source": "ynet",
                        "date": "02-11-2021"
                    },
                    "queries": {
                        "title": "Ly9oMVtAY2xhc3M9Im1haW5UaXRsZSJdL3RleHQoKQ=="
                    },
                    "project": "example__project",
                    "out": "request_data"
                }
            }
        """
    elif type_of_service == PDF_PARSER_FLAG:
        example= """
            {
                "data_type": "all",
                "start_text": "Lorem ipsum",
                "end_text": "maximus ultricies",
                "_file" : [
                        "Choose a file from the following url and use it", 
                        "https://file-examples.com/index.php/sample-documents-download/sample-pdf-download/"
                    ]
            }
        """
    elif type_of_service == AZURE_DATALAKE_FLAG:
        example = """
            {
                "functionality": "create_request",
                "entity": {
                    "DestinationID": "2",
                    "cron": "1 * * 5 *",
                    "end_date": "1943-01-01",
                    "start_date": "1937-01-01",
                    "serviceID": "1",
                    "description": "FastAPI- Raw",
                    "user": "Reuven P",
                    "output_name": "reuven_maya.zip",
                    "parameters": {
                        "raw_model": {
                            "url": "https://www.shufersal.co.il/online/he/קטגוריות/סופרמרקט/חלב-וביצים/מעדנים-וקינוחים/c/A0110",
                            "duplications": true,
                            "parameters": {
                                "Title": [
                                    "מילקי בטעם וניל"
                                ],
                                "Price": [
                                    "2.90"
                                ]
                            }
                        }
                    }
                }
            }
        """
    return json.loads(example)


def check_tables_desire(table_name: str, method:str) -> bool: # And what are your desires? Hmmm...
    if ((method == AZURE_FUNCTIONS[1] and (table_name == 'Parameters' or table_name == 'AutoScraperParametersTable')) or 
        (table_name == 'Services' or table_name == 'Destinations' or table_name == 'AutoScraperServicesTable' or table_name == 'AutoScraperDestinationsTable')):
        return False
    else:
        return True


def send_email_for_request_approval(request_data: dict, request_type: str): # This comment is a building block.
    email_data = {
        "recipients": [
            "<INSERT RECIPIENT EMAIL HERE>",
            "<INSERT RECIPIENT EMAIL HERE>",
            "<INSERT RECIPIENT EMAIL HERE>"
        ],
        "email_subject": f"Request: {request_type}",
        "email_body": str(request_data) + ""
    }
    from logic_functions.send_email_logic import build_email # Import must stay here inside of this method, otherwise it causes an 'ImportError: partially initialized module'
    email_recipients = email_data["recipients"]
    email_subject = email_data["email_subject"]
    body_data = email_data["email_body"].replace(',', ',<br>').replace("{'", "{<br>'").replace("'}", "'<br>}")
    email_body = "<u>JSON Format Data:</u><br>" + body_data
    email_status = build_email(recipients=email_recipients, email_subject=email_subject, email_body=email_body)
    return email_status


def check_get_dag_default_state(action_: str) -> bool:
    """
        - create, disable :: return bool
        - delete          :: return None
    """
    actions_ = ['create', 'disable', 'delete']
    if action_ not in actions_:
        raise ValueError("Invalid action type. Expected one of: %s" % actions_)
    if action_ == actions_[0]:
        return False
    elif action_ == actions_[1]:
        return True
    elif action_ == actions_[2]:
        return None


def maintenance_msg(msg:str = None) -> str:
    if msg:
        return f"We are sorry but this function is under maintance mate!\n{msg}"
    return "We are sorry but this function is under maintance mate!"
# End of file.