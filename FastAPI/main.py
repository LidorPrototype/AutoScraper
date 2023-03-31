import requests
import pandas as pd
import shutil
import os
import io
import json, ast
import base64
import sys
from typing import Optional
from fastapi import FastAPI, Query, File, UploadFile
from fastapi.params import Body
from fastapi.responses import RedirectResponse, FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
# Custom Functions Import
from logic_functions.raw_as_logic import scrape_similarities
from logic_functions.api_logic import return_file
from logic_functions.maya_logic import download_maya_pdf, download_maya_pure_html, download_maya_json, download_maya_csv
from logic_functions.queries_logic import use_xpath_scraping
from logic_functions.pdf_parsing_logic import get_text_ignore_tables, get_entire_pdf_as_str, get_tables_only
from logic_functions.general_utils import check_tables_desire, get_examples, send_email_for_request_approval, maintenance_msg
from logic_functions.send_email_logic import dummy_email, build_email
from logic_functions.azure_datalake_tables.azure_tables import TableEntityDatalake
from logic_functions.dag_creation_file import request_dag_creation
# Models
from models import RawModel, MayaModel, QueriesModel, EmailsModel, TableEntityModel
# BatSheva File
from logic_functions.retail_trades import run_file
from fastapi.responses import StreamingResponse
# Key and Flags Import
from logic_functions.general_utils import ACCESS_KEY, DSG_KEY, BS_KEY, MAYA_HTML_KEY, MAYA_JSON_KEY, MAYA_CSV_KEY, MAYA_PDF_KEY, PDF_ALL_KEY, PDF_TEXT_KEY, PDF_TABLES_KEY
from logic_functions.general_utils import AUTOSCRAPER_FLAG, GET_FILE_FLAG, POST_FILE_FLAG, MAYA_FLAG, QUERIES_XPATH_FLAG, PDF_PARSER_FLAG, AZURE_DATALAKE_FLAG
from logic_functions.general_utils import AZURE_FUNCTIONS
from logic_functions.general_utils import check_get_dag_default_state

# Author: Lidor Eliyahu Shelef
# Activation function: uvicorn main:app --reload


app = FastAPI()

# You Shall Not Pass!
u_access_token = ACCESS_KEY
dsg_access = DSG_KEY
batsheva_access = BS_KEY
#  Variable to add to Exception when debugging for easier debugging the locations
tester_error_msg = ""

favicon_path = 'favicon.ico'


@app.exception_handler(StarletteHTTPException)
def custom_http_exception_handler(request, exc): # Magic. Do not touch.
    # url_end = str(request.url).split('/')[-1]
    # if url_end == "":
    #     return RedirectResponse("/home")
    return RedirectResponse("/home?redirected=You have been redirected due to an invalid api call")


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/")
def root(redirected: str = None, get_requirements: bool = False):
    """
        <u><b>Information function</b></u> \n
            Returns:
             - Dataframe in a json format explaining all of the autoscrapper functions\n
             - List of all the requirements\n

        <i><li> <b>For an example of each method, use the 'example' flag on each of the method (not the deprecated ones)</b></li></i> \n

        <i><u><h2>
        #158 - docstrings updated and grammered fixed + remove irrelevant stuff
        </h2></u></i>
    """
    if get_requirements:
        with open("requirements.txt", "r") as f:
            requirements_txt = f.readlines()
            return requirements_txt
    functions = {
        "post_autoscraper": ("Using the AutoScraper in order to scrape the raw data", "Valid"),
        "get_file": ("Takes the URL in the header, with the param 'api_link'", "Valid"),
        "post_file": ("Takes the URL in the body, with the param 'api_link", "Valid"),
        "get_maya": ("Handles all the Maya website reports download and parsing, 5 Parameters", "Valid"),
        "post_maya": ("Handles all the Maya website reports download and parsing, 5 Parameters In body embdded", "Valid"),
        "post_queries": ("Handles the scraping of givens urls based on given xpaths and more parameters, and bs4 scraping of a given url and commands", "Valid"),
        "post_pdf_file": ("A method that accept a PDF file and returns it's content based on pre defined parameters", "Valid"),
        "post_email": ("Send us an email about some stuff", "Valid"),
        "azure_datalake_function": ("All the functionality related to the Azure Datalake", "Valid"),
        "create_dag": ("All the functionality related to the Airflow platform and the DAG creations", "Valid")
    }
    result = functions
    if redirected:
        result = redirected, functions
    return result


@app.post("/post_autoscraper")
def post_autoscraper(raw_model: RawModel = Body(..., embed=True), example: Optional[str] = Query("N", max_length=1, min_length=1, regex=r"[YyNn]")):
    """
        Goal: \n
            Scraping the given url based on similarities and collecting them \n
        Parameters In Body: \n
            :param raw_model: A RawModel model with the following attributes:
                :attribute url: A string representation of the url of which the scraping should occur
                :attribute duplications: A boolean flag indicating how to handle the duplication in the data
                :attribute parameters: A Dictionary object containing all of the scraping data
                                            Dictionary format should be: {field_name: field_values}\n
                                            Dictionary types should be: {str: list}\n
            :param example: See end of this docstring \n
        Returns a dataframe with all the similarities of each example the user has given\n
        <hr>
        Example of a request body can be obtain by setting the example flag to 'Y' or 'y' in the url path.
    """
    if example.upper() == 'Y':
        return get_examples(AUTOSCRAPER_FLAG)
    try:
        if not raw_model.parameters:
            return "Please supply us with parameters for the scrape mate!"
        scrape_elements = {}
        for key in raw_model.parameters:
            scrape_elements[key] = raw_model.parameters[key]
            # If this comment is removed the program will blow up 
        return "Result is: ", scrape_similarities(raw_elements=scrape_elements, _url=raw_model.url, duplications_status=raw_model.duplications, re_headers = None)
    except Exception as e:
        return str(e)


@app.get("/get_file")
def get_file(api_link: Optional[str] = None, file_name: str = None, example: Optional[str] = Query("N", max_length=1, min_length=1, regex=r"[YyNn]")):
    """
        <h2><u>Deprecated, please use the post equivalence of this method!</u></h2>
        Goal: \n
            Return the downloaded file to the user \n
        Parameters: \n
            :param api_link: A string representing the API url the user wishes to download \n
            :param file_name: A string representing the output file name of the file \n
            :param example: See end of this docstring \n
        Instructions: \n
            The parameter :api_link" will be given in the url address as follows:
                https://www.example.com/get_file/?api_link={replace this with the link it self} \n
        Returns the file itself
        <hr>
        Example of a request can be obtain by setting the example flag to 'Y' or 'y' in the url path.
    """
    if example.upper() == 'Y':
        return get_examples(GET_FILE_FLAG)
    return return_file(api_link, file_name)


@app.post("/post_file")
def post_file(api_link: Optional[str] = Body(..., embed=True), file_name: Optional[str] = Body(..., embed=True), example: Optional[str] = Query("N", max_length=1, min_length=1, regex=r"[YyNn]")):
    """
        Goal: \n
            Return the downloaded file to the user \n
        Parameters: \n
            :param api_link: A string representing the API url the user wishes to download \n
            :param file_name: A string representing the output file name of the file \n
            :param example: See end of this docstring \n
        Instructions: \n
            The parameter :api_link" will be given in the body of the request, witht he keyword 'api_link' \n
        Returns the file itself
        <hr>
        Example of a request body can be obtain by setting the example flag to 'Y' or 'y' in the url path.
    """
    # return maintenance_msg()
    if example.upper() == 'Y':
        return get_examples(POST_FILE_FLAG)
    return return_file(api_link, file_name)


@app.get("/get_maya")
def get_maya(service_type: str = "", eng_report: str = "", heb_report: str = "", start_date: str = "", end_date: str = "", inner_format: Optional[str] = "HTML", example: Optional[str] = Query("N", max_length=1, min_length=1, regex=r"[YyNn]")):
    """
        <h2><u>Deprecated, please use the post equivalence of this method!</u></h2>
        Goal: \n
            Return the downloaded file/s to the user, based on the chosen format \n
        Parameters: \n
            :param service_type: A string representing the type of subservice ("HTML \ PDF")
            :param eng_report: A string representing the English report name
            :param heb_report: A string representing the Hebrew report name
            :param start_date: A string representing the start of the date period
            :param end_date: A string representing the end of the date period
            :param inner_format: An Optional parameter, getting used on the HTML part only to indicate which type of format the user wants (HTML, JSON, CSV)
            :param example: See end of this docstring \n
        Instructions: \n
            The parameters should be in the url itself, after the '?' and with & between them as follows:
                https://www.example.com/maya_pdf/{service_type}/?&eng_report=...&heb_report=...&{so on and so forth}
            Optional parameter :inner_format: is used when :service_type: is set to HTML, in order to decide on the reports format (HTML, JSON, CSV) \n
        Returns: \n
            The zip file of all the reports together, if it's HTML-CSV it will return a single CSV file
        Empty Case:
            In case the search will give no valid data the method will return the following string: "No data found for this search, sorry mate!"
        <hr>
        Example of a request body can be obtain by setting the example flag to 'Y' or 'y' in the url path.
    """
    if example.upper() == 'Y':
        return get_examples(MAYA_FLAG)
    activation_function = None
    error_msg = ""
    if service_type.strip().upper() == MAYA_HTML_KEY:
        if inner_format:
            if inner_format.strip().upper() == MAYA_HTML_KEY:
                activation_function = download_maya_pure_html
            elif inner_format.strip().upper() == MAYA_JSON_KEY:
                activation_function = download_maya_json
            elif inner_format.strip().upper() == MAYA_CSV_KEY:
                activation_function = download_maya_csv
        else:
            error_msg = "Parameter inner_format need to be added, read documentation for more details mate!"
    elif service_type.strip().upper() == MAYA_PDF_KEY:
        activation_function = download_maya_pdf
    if activation_function:
        return activation_function(eng_report, heb_report, start_date, end_date)
    else:
        return error_msg


@app.post("/post_maya")
def post_maya(maya_model: MayaModel = Body(..., embed=True), example: Optional[str] = Query("N", max_length=1, min_length=1, regex=r"[YyNn]")):
    """
        Goal: \n
            Return the downloaded file/s to the user, based on the chosen format \n
        Parameters: \n
            :param maya_model:
                :attr service_type: A string representing the type of subservice the user want ("HTML \ PDF")
                :attr eng_report: A string representing the English report name
                :attr heb_report: A string representing the Hebrew report name
                :attr start_date: A string representing the start of the date period
                :attr end_date: A string representing the end of the date period
                :attr inner_format: An Optional parameter, getting used on the HTML part only to indicate which type of format the user wants (HTML, JSON, CSV)
            :param example: See end of this docstring \n
        Returns: \n
            The zip file of all the reports together, if it's HTML-CSV it will return a single CSV file
        Empty Case:
            In case the search will give no valid data the method will return the following string: "No data found for this search, sorry mate!"
        <hr>
        Example of a request body can be obtain by setting the example flag to 'Y' or 'y' in the url path.
    """
    if example.upper() == 'Y':
        return get_examples(MAYA_FLAG)
    activation_function = None
    error_msg = ""
    if maya_model.service_type.strip().upper() == MAYA_HTML_KEY:
        if maya_model.inner_format:
            if maya_model.inner_format.strip().upper() == MAYA_HTML_KEY:
                activation_function = download_maya_pure_html
            elif maya_model.inner_format.strip().upper() == MAYA_JSON_KEY:
                activation_function = download_maya_json
            elif maya_model.inner_format.strip().upper() == MAYA_CSV_KEY:
                activation_function = download_maya_csv
        else:
            error_msg = "Parameter inner_format need to be added, read documentation for more details mate!"
    elif maya_model.service_type.strip().upper() == MAYA_PDF_KEY:
        activation_function = download_maya_pdf
    if activation_function:
        return activation_function(maya_model.eng_report, maya_model.heb_report, maya_model.start_date, maya_model.end_date)
    else:
        return error_msg


@app.post("/post_queries")
def post_queries(queries_model: QueriesModel = Body(..., embed=True), example: Optional[str] = Query("N", max_length=1, min_length=1, regex=r"[YyNn]")):
    """
        Goal: \n
            Scraping the given urls, based on the xpath commands given, with prefixes and metadata \n
        Parameters In Body: \n
            :param queries_model:
                :attribute urls: List of string representations of the given urls
                :attribute prefixes: List of string representations of the given prefixes
                :attribute metadata: A Dictionary that holds all the metadata names and values
                                            Dictionary format should be: {metadata_name: metadata_values}
                                            Dictionary types should be: {str: str}
                :attribute queries: A Dictionary that holds all the queries names and xpaths
                                            Dictionary format should be: {queries: queries_xpaths}
                                            Dictionary types should be: {str: str}
                                        Importent!!! queries should come in an encode base64 format and it will be treated as such!
                :attribute project: A string representation of the project name
                :attribute out: A string representation of the output result file
            :param example: See end of this docstring \n
        Returns a dataframe with all the scraped data from the XPATH or BS4 depending on what the user requested
        <hr>
        Example of a request body can be obtain by setting the example flag to 'Y' or 'y' in the url path.
    """
    if example.upper() == 'Y':
        return get_examples(QUERIES_XPATH_FLAG)
    try:
        shutil.rmtree("demo/AutoScraperSpiders")
    except Exception as e: 
            print("----------------------------------------------------------")
            print(str(e))
    try:
        # If you are reading this, please add a checkmark here [V,]
        (result, status) = pd.DataFrame(), "Not Started!"
        if queries_model == None:
            queries_model = QueriesModel()
        _urls = queries_model.urls
        _prefixes = queries_model.prefixes
        _metadata = queries_model.metadata
        _queries = queries_model.queries
        _queries_decoded = {}
        try:
            for key, value in _queries.items():
                encoded_value_bytes = base64.b64decode(value)
                decoded_value = encoded_value_bytes.decode("ascii")
                _queries_decoded[key] = decoded_value
        except Exception as e:
            return f"Queries should be in a base64 encoded format ------------- {str(e)}"
        _data = {
                'urls' : _urls,
                'prefixes' : _prefixes,
                'metadata' : _metadata,
                'queries' : _queries_decoded,
                'project': queries_model.project or "project__test",
                'out': queries_model.out or "request__data"
            }
        (result, status) = use_xpath_scraping(_data)
        return result, status, ("Data Received", str(dict(queries_model)))
    except Exception as e:
        return "ERROR is:  " + str(e)
    finally:
        try:
            shutil.rmtree("demo/AutoScraperSpiders")
        except FileNotFoundError as e: 
            print("----------------------------------------------------------")
            print(str(e))


@app.post("/post_pdf_file/") # Need a "pip install python-multipart" for using UploadFile, File
def post_pdf_file(_file: Optional[UploadFile] = File(None), file_link: str = Body(None, embed=True), data_type: str = Body("all", embed=True), from_text: str = Body(None, embed=True), to_text: str = Body(None, embed=True), pages_devider: str = Body("\n", embed=True), example: Optional[str] = Query("N", max_length=1, min_length=1, regex=r"[YyNn]")):
    """
        Goal: \n
            Returning the content of a given PDF file \n
        Parameters In Body: \n
            :param data_type: type of content the user wishes to get:
                :attribute all: Get the entire PDF file content in str format
                :attribute text: Get the text data only, while ignoring the tables data
                :attribute tables: Get only the tables in the PDF file, while ignoring outside texts
            :param start_text, end_text: Apply to the 'text' :data_type:, 
                                        indicating from where to where the user wish to get text in the PDF file
                                        - Defaults to None, None
            :param pages_devider: The String that will be between each page, defaults to "\\n" apply to the 'all' key only
            :param _file: The PDF file itself
            :param file_link: A str link to the PDF file
            :param example: See end of this docstring \n
        Returns a dataframe with all the scraped data from the XPATH or BS4 depending on what the user requested 
        <hr>
        Example of a request body can be obtain by setting the example flag to 'Y' or 'y' in the url path.\n
            --> Make sure to supply a demo file (FastAPI request won't let it be optional), the file will be ignored tho
    """
    if example.upper() == 'Y':
        return get_examples(PDF_PARSER_FLAG)

    if _file is not None:
        file_name = _file.filename
        if not _file.filename.endswith('.pdf'):
            return "This methos works only with PDF files mate!"
    elif file_link is not None:
        file_name = ""
    else:
        return "Please provide us with a file mate . . ."
    if _file is None and not file_link.endswith('.pdf'):
        return "This methos works only with PDF files mate!"
    try:
        result_str = "Invalid data parameter mate!"
        # Get the file
        if _file is not None:
            with open(file_name, 'wb+') as file_obj:
                file_obj.write(_file.file.read())
        elif file_link is not None:
            file_name = ""
            response = requests.get(file_link)
            file_name = "download_files/temp.pdf"
            file = open("" + file_name, "wb")
            file.write(response.content)
            file.close()
        # Parse the file
        if data_type == PDF_ALL_KEY:
            result_str = get_entire_pdf_as_str(file_name, from_text, to_text, page_devider=pages_devider)
        elif data_type == PDF_TEXT_KEY:
            result_str = get_text_ignore_tables(file_name, from_text, to_text)
        elif data_type == PDF_TABLES_KEY:
            result_str = get_tables_only(file_name)
        return result_str
    except Exception as e:
        return f"Some Exception occurred while processing your request: ( {str(e)} )"
    finally:
        try:
            os.remove(file_name)
        except FileNotFoundError as fe:
            try:
                os.remove("download_files/" + file_name)
            except: pass
    

@app.post("/post_email")
def post_email(send_dummy: bool = False, email_model: EmailsModel = Body(..., embed=True)):
    """
        Goal: \n
            Send an email to recipients \n
        Parameters In Body: \n
            :param send_dummy: Dummy flag in order to send a dummy email to the developer
            :param email_model: Holds all of the email data using a model as follows:
                :attribute recipients: List of all the email recipients
                :attribute email_subject: String representation of the email's subject
                :attribute email_body: String representation of the email's body
        Returns the status code of the email http request
    """
    email_status = ""
    if send_dummy:
        email_status = dummy_email()
    else:
        recipients_of_email = email_model.recipients
        subject_of_email = email_model.email_subject
        body_of_email = email_model.email_body
        email_status = build_email(recipients=recipients_of_email, email_subject=subject_of_email, email_body=body_of_email)
    return email_status


@app.post("/azure_datalake_functions")
def azure_datalake_functions(functionality: str = Body(AZURE_FUNCTIONS[0], embed=True), special_access: str = Body(None, embed=True), table_name: str = Body(None, embed=True), 
                                entity: TableEntityModel = Body(None, embed=True), partitionKey: str = Body(None, embed=True), rowKey: str = Body(None, embed=True), 
                                example: Optional[str] = Query("N", max_length=1, min_length=1, regex=r"[YyNn]")):
    """
        Goal:\n
            Responsible for all of the Azure Datalake functionality\n
        Parameters:\n
            :param functionality: Determine what is the function you wish to apply
                :attr list_all: Provide the parameter 'table_name' in the body with the desired table name
                :attr create_request: Provide the parameter 'entity' to be created
                :attr update_request: Provide the location of the entity to update with the parameters 'partitionKey', 'rowKey', 'table_name' and the 'entity' itself
                :attr approve_request, disable_request, delete_request: Provide the 'partitionKey' and 'rowKey' in the UserRequests table
                :attr delete@all: A special command to delete all of the tables -> Need a special access key
                :attr restart_default: A special command to restart all of the tables to default state -> Need a special access key
            :param special_access: A special key, meant for the deletion of everything or resetting of everything
            :param table_name: The name of the desired table
            :param entity: The table entity itself (All Attribute Are Strings)
                :attr DestinationID: Destination of the output file
                :attr cron: The cron Schedule of this request
                :attr end_date: Final date for this request
                :attr start_date: Since when this request is active
                :attr serviceID: Type of service this request is requesting (digit)
                :attr description: Free Text
                :attr user: The username/full name/email of the user that request this request
                :attr output_name: Output file name
                :attr parameters: String representation of a Dictionary of the parameters (See Additional Notes)
            :param partitionKey: The partitionKey of the request in the desired table
            :param rowKey: The rowKey of the request in the desired table
        <hr>\n
        <u>Additional Notes:</u>\n
        <ol>
            <li><b>The attribute named 'parameters' must be a legit <u>dict object {valueName: valueValue}</u> that has been converted to a string format in order for this to work, the method json.loads(json.dumps()) will be used on it</b></li>
            <li><b>You must pass the attribute 'parameters' as a base64 format.</b></li>
        </ol>
    """
    if example.upper() == 'Y':
        return get_examples(AZURE_DATALAKE_FLAG)
    if functionality not in AZURE_FUNCTIONS:
        return f"Please provide a functionality from the following options: {AZURE_FUNCTIONS}"
    _obj_ = TableEntityDatalake()
    if entity and functionality in AZURE_FUNCTIONS[1:4]:
        entity = dict(entity)
        encoded_value_bytes = base64.b64decode(entity['parameters'])
        decoded_value = encoded_value_bytes.decode("utf-8")
        entity['parameters'] = decoded_value
    if functionality == AZURE_FUNCTIONS[0]: # list_all -> 'table_name'
        if not table_name:
            return "Please provide a table name to list in the parameter 'table_name'"
        elif table_name not in _obj_.table_names:
            return f"Please provide one of the following as the 'table_name': {list(_obj_.table_names.keys())}"
        return _obj_.get_all_entities(table_name=_obj_.table_names[table_name])
    elif functionality == AZURE_FUNCTIONS[1]: # create_request -> 'entity'
        if not check_tables_desire(table_name=table_name, method=AZURE_FUNCTIONS[1]):
            return f"You don't have premissions to create a request in the following table: <{table_name}> mate !"
        if not entity:
            return "Please provide an entity object (TableEntityModel) in the parameter 'entity'"
        entity = dict(entity)
        entity["status"] = "pending"
        entity['parameters'] = ast.literal_eval(json.loads(json.dumps(entity['parameters'])).replace("true", "True").replace("false", "False"))
        creation_status = _obj_.update_datalake_storage_with_request(request_data=entity)
        if creation_status == -17:
            return f"Please provide all the following parameters {_obj_.maya_vars}"
        email_status = send_email_for_request_approval(request_data=entity, request_type=functionality)
        return (creation_status, email_status)
    elif functionality == AZURE_FUNCTIONS[2]: # update_request -> 'entity', 'table_name', 'partitionKey', 'rowKey'
        if not check_tables_desire(table_name=table_name, method=AZURE_FUNCTIONS[2]):
            return "You Don't Have Premissions To Do That Mate !"
        if table_name not in _obj_.table_names.keys():
            return f"Please make sure that the table name is one of the follwing: {list(_obj_.table_names.keys())}"
        if partitionKey is None or rowKey is None or table_name is None or entity is None:
            return "Please provide all of the following: ['entity', 'partitionKey', 'rowKey', 'table_name']"
        entity = dict(entity)
        entity['PartitionKey'] = partitionKey
        entity['RowKey'] = rowKey
        update_status = _obj_.update_entity(table_name=table_name, _entity=entity, creation_flag=False)
        email_status = send_email_for_request_approval(request_data=entity, request_type=functionality)
        return (update_status, email_status)
    elif functionality == AZURE_FUNCTIONS[3]: # delete_request -> 'table_name', 'partitionKey', 'rowKey'
        if table_name is None:
            table_name = 'UserRequests'
        if not check_tables_desire(table_name=table_name, method=AZURE_FUNCTIONS[3]):
            return "You Don't Have Premissions To Do That Mate !"
        if partitionKey is None or rowKey is None or table_name is None:
            return "Please provide all of the following: ['partitionKey', 'rowKey', 'table_name']"
        if table_name not in _obj_.table_names.keys():
            return f"Please provide make sure that the table name is one of the follwing: {list(_obj_.table_names.keys())}"
        entity = dict(entity)
        entity['status'] = 'disabled'
        email_status = send_email_for_request_approval(request_data=entity, request_type=functionality + ' - disable')
        delete_status = _obj_.delete_entity(table_name=table_name, entity_partition_key=partitionKey, entity_row_key=rowKey, termination_flag=True)
        return (delete_status, email_status)
    elif functionality == AZURE_FUNCTIONS[4]: # approve_request -> 'partitionKey', 'rowKey'
        if partitionKey is None or rowKey is None:
            return "Please provide all of the following: ['partitionKey', 'rowKey']"
        table_name = "UserRequests"
        entity = _obj_.get_entity(table_name=table_name, partition_key=partitionKey, row_key=rowKey)
        entity['PartitionKey'] = partitionKey
        entity['RowKey'] = rowKey
        entity['status'] = 'created'
        update_status = _obj_.update_entity(table_name=table_name, _entity=entity, creation_flag=False)
        email_status = send_email_for_request_approval(request_data=entity, request_type=functionality)
        return (update_status, email_status)
    elif functionality == AZURE_FUNCTIONS[5]: # disable_request -> 'partitionKey', 'rowKey'
        if table_name is None or table_name not in _obj_.table_names.keys():
            table_name = 'UserRequests'
        if partitionKey is None or rowKey is None:
            return "Please provide all of the following: ['partitionKey']"
        if table_name not in _obj_.table_names.keys():
            return f"Please provide make sure that the table name is one of the follwing: {list(_obj_.table_names.keys())}"
        entity = _obj_.get_entity(table_name=table_name, partition_key=partitionKey, row_key=rowKey)
        entity['status'] = 'disabled'
        email_status = send_email_for_request_approval(request_data=entity, request_type=functionality + ' - disable')
        delete_status = _obj_.delete_entity(table_name=table_name, entity_partition_key=partitionKey, entity_row_key=rowKey, disable_flag=True)
        return (delete_status, email_status)
    elif functionality == AZURE_FUNCTIONS[6] or functionality == AZURE_FUNCTIONS[7]: # delete@all -> special comman to delete all the tables -> 'special_access'
        if special_access == dsg_access:
            if functionality == AZURE_FUNCTIONS[4]:
                return _obj_.delete_tables()
            elif functionality == AZURE_FUNCTIONS[5]:
                return _obj_.restart_tables()
        else:
            return "Unauthorized Access Mate!"


@app.get("/manage_dag")
def manage_dag(partitionKey_: str, rowKey_: str, action_: str):
    """
        Goal:\n
            Manage all of the airflow process (creating, disabling and deleting the DAGS)
        Parameters:\n
            :param partitionKey_: str representing the partitionKey in the azure datalake of the desired request (UserRequest table)
            :param rowKey_: str representing rowKey in the azure datalake of the desired request (UserRequest table)
            :param action_: str setting the action you would like to perform (create, disable, delete)
    """
    dag_default_state = False
    try:
        dag_default_state = check_get_dag_default_state(action_=action_)
    except ValueError as ve:
        return str(ve)
    if dag_default_state is None:
        return "Delete option is not supported to the public yet mate !"
    try:
        # Magic. Do not touch. (Removing this comment will result in a forrest fire)
        # Examples: 
        # json_encoded_raw="ewogICJyYXdfbW9kZWwiOiB7CiAgICAidXJsIjogImh0dHBzOi8vd3d3LnNodWZlcnNhbC5jby5pbC9vbmxpbmUvaGUv16fXmNeS15XXqNeZ15XXqi/XodeV16TXqNee16jXp9eYL9eX15zXkS3XldeR15nXpteZ150v157XoteT16DXmdedLdeV16fXmdeg15XXl9eZ150vYy9BMDExMCIsCiAgICAiZHVwbGljYXRpb25zIjogdHJ1ZSwKICAgICJwYXJhbWV0ZXJzIjogewogICAgICAiVGl0bGUiOiBbCiAgICAgICAgItee15nXnNen15kg15HXmNei150g15XXoNeZ15wiCiAgICAgIF0sCiAgICAgICJQcmljZSI6IFsKICAgICAgICAiMi45MCIKICAgICAgXQogICAgfQogIH0KfQ=="
        # json_encoded_api="ewoJImFwaV9saW5rIjogImh0dHA6Ly93d3cuaW1hZ2Vwcm9jZXNzaW5ncGxhY2UuY29tL2Rvd25sb2Fkc19WMy9yb290X2Rvd25sb2Fkcy9pbWFnZV9kYXRhYmFzZXMvc3RhbmRhcmRfdGVzdF9pbWFnZXMuemlwIiwKCSJmaWxlX25hbWUiOiAic3RhbmRhcmRfdGVzdF9pbWFnZXMuemlwIgp9"
        # json_encoded_queries="ewogICJxdWVyaWVzX21vZGVsIjogewogICAgImlzX3hwYXRoIjogdHJ1ZSwKICAgICJpc19iczQiOiBmYWxzZSwKICAgICJ1cmxzIjogWwogICAgICAiaHR0cHM6Ly93d3cueW5ldC5jby5pbC9uZXdzL2NhdGVnb3J5LzE4NSIKICAgIF0sCiAgICAicHJlZml4ZXMiOiBbCiAgICAgICJodHRwczovL3d3dy55bmV0LmNvLmlsL25ld3MvYXJ0aWNsZSIKICAgIF0sCiAgICAibWV0YWRhdGEiOiB7CiAgICAgICJzb3VyY2UiOiAieW5ldCIsCiAgICAgICJkYXRlIjogIjAyLTExLTIwMjEiCiAgICB9LAogICAgInF1ZXJpZXMiOiB7CiAgICAgICJ0aXRsZSI6ICJMeTlvTVZ0QVkyeGhjM005SW0xaGFXNVVhWFJzWlNKZEwzUmxlSFFvS1E9PSIKICAgIH0sCiAgICAicHJvamVjdCI6ICJleGFtcGxlX19wcm9qZWN0IiwKICAgICJvdXQiOiAicmVxdWVzdF9kYXRhIgogIH0KfQ=="
        # json_encoded_maya="c2VydmljZV90eXBlPUhUTUwKZW5nX3JlcG9ydD1UYXYwNDkKaGViX3JlcG9ydD3XqjA0OQpzdGFydF9kYXRlPTIwMjEtMDgtMTEKZW5kX2RhdGU9MjAyMS0wOC0yMQppbm5lcl9mb3JtYXQ9SFRNTA=="
        if sys.platform.startswith('win'):
            path = r'\dags'
        else:
            path = r'/dags'
        if partitionKey_ is None or rowKey_ is None:
            return "Please provide all of the following: ['partitionKey', 'rowKey']"
        _obj_ = TableEntityDatalake()
        table_name = "UserRequests"
        tester_error_msg = "before entity"
        entity = _obj_.get_entity(table_name=table_name, partition_key=partitionKey_, row_key=rowKey_)
        service_type = _obj_.service_by_code[entity["serviceID"]]
        dag_id = partitionKey_
        cron = entity["cron"]
        owner = entity["user"]
        start_date = entity["start_date"]
        end_date = entity["end_date"]
        tester_error_msg = "before get_json_encoded_parameters"
        json_encoded = _obj_.get_json_encoded_parameters(partition_key=partitionKey_, row_key=rowKey_)
        email_subject = entity["DAG_Name"] + " <-> " + table_name
        tester_error_msg = "before request_dag_creation"
        recipients_list=['<INSERT RECIPIENT EMAIL HERE>']
        dag_str = request_dag_creation(
            service_type_=service_type,
            id_=dag_id,
            cron_=cron,
            owner_=owner,
            start_date_=start_date,
            end_date_=end_date,
            json_encoded_=json_encoded,
            email_subject_=email_subject,
            _recipients_list=recipients_list,
            filename_=None,
            extension_=None, 
            default_state=dag_default_state
        )
        tester_error_msg = "before writing the DAG"
        with open(os.path.join(path, f'{entity["DAG_Name"]}.py'), 'w', encoding="utf-8-sig") as file:
            file.write(dag_str.replace(";.;", ""))
        entity["status"] = 'created'
        tester_error_msg = "before update_entity"
        _obj_.update_entity(table_name=table_name, _entity=entity)
    except Exception as e:
        return f"ERROR--->>>|    {str(e)}      |     {tester_error_msg}"
    return "Success, go check the new DAG out!"


@app.get("/retails_trade")
def retails_trade(access: str):
    """
        ## Limited method for Batsheva Rich, to help her with her clients - API only
        :access: key is needed
    """
    # This method is adding the 'chardet' library to the requirements - Need to add!
    try:
        if access != batsheva_access and access != u_access_token:
            return "Unauthorized access mate!"
        wanted_file_path = run_file()
        temp_file = None
        with open (wanted_file_path, mode="rb") as _f:
            temp_file = _f.read()
        final_file = io.BytesIO(temp_file)
        shutil.rmtree(wanted_file_path.split('/')[0])
        return StreamingResponse(final_file)
    except Exception as e:
        return str(e)
# End of file.