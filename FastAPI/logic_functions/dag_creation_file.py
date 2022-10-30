# Want to see recursion? look at the bottom of the file
from datetime import datetime, timezone
import sys, base64, ast
from typing import Tuple

# Author: Lidor Eliyahu Shelef

default_desc = "No Description Provided"


def get_service_link(script_type: str) -> str:
    if script_type == "API":
        return "https://boirndextautoscrapper.azurewebsites.net/get_file?api_link={api_link}&example=N"
    elif script_type == "RAW":
        return "https://boirndextautoscrapper.azurewebsites.net/post_autoscraper"
    elif script_type == "MAYA":
        return "https://boirndextautoscrapper.azurewebsites.net/get_maya?service_type={service_type}&eng_report={eng_report}&heb_report={heb_report}&start_date={start_date}&end_date={end_date}&inner_format={inner_format}&example=N"
    elif script_type == "QUERIES":
        return "https://boirndextautoscrapper.azurewebsites.net/post_queries"
    else:
        return ""


def get_service_function(script_type: str, service_parameters: dict, recipients_:list) -> str:
    if script_type == "API":
        return f"""
def use_fast_api(url_: str):
    try:
        json_encoded = '{service_parameters['json_encoded']}'
        json_string = base64.b64decode(json_encoded)
        api_model = json.loads(json_string)
        api_url = api_model['api_link']
        if api_url[0] == "\\\"":
            api_url = api_url[1:]
            if api_url[-1] == "\\\"":
                api_url = api_url[:-1]
        _url_ = url_.format(api_link=api_url)
        res = requests.get(_url_)
        output_file = api_model['file_name'] # '{service_parameters['_file_name_']}' + '{service_parameters['_extension_']}'
        # with open(output_file, 'wb') as _file:
        #     _file.write(res.content)
        send_mail(body_data=str(res.text), subject='{service_parameters['email_subject']}', recipients={recipients_})
    except Exception as e:
        if hasattr(e, 'message'):
            send_mail(body_data=str(e) + "<br>" + str(e.message), subject='AutoScraper - API ERROR', recipients={recipients_})
        else:
            send_mail(body_data=str(e), subject='AutoScraper - API ERROR', recipients={recipients_})
        """
    elif script_type == "RAW":
        return f"""
def use_fast_api(url_: str):
    try:
        json_encoded = '{service_parameters['json_encoded']}'
        json_string = base64.b64decode(json_encoded)
        raw_model = json.loads(json_string)
        raw_model['raw_model'] = ast.literal_eval(raw_model['raw_model'].replace('true', 'True'))
        res = requests.post(url_, data = json.dumps(raw_model))
        df = pd.DataFrame.from_dict(res.json()[1])
        send_mail(body_data=df.to_html(), subject='{service_parameters['email_subject']}', recipients={recipients_})
    except Exception as e:
        if hasattr(e, 'message'):
            send_mail(body_data=str(e) + "<br>" + str(e.message), subject='AutoScraper - RAW ERROR', recipients={recipients_})
        else:
            send_mail(body_data=str(e), subject='AutoScraper - RAW ERROR', recipients={recipients_})
        """
    elif script_type == "MAYA":
        maya_data=[]
        maya_data_dict = dict(ast.literal_eval(base64.b64decode(service_parameters["json_encoded"]).decode('utf-8')))
        for key, value in maya_data_dict.items():
            maya_data.append(value.replace("\"", ""))
        return f"""
def use_fast_api(url_: str):
    try:
        res = requests.get(url_.format(service_type="{script_type}", eng_report="{maya_data[0]}", heb_report="{maya_data[1]}", start_date="{maya_data[2]}", end_date="{maya_data[3]}", inner_format="{maya_data[4]}"))
        output_file = '{service_parameters['_file_name_']}' + '{maya_data[4].lower()}'
        # with open(output_file, 'wb') as _file:
        #     _file.write(res.content)
        msg = str(res.status_code) + " : " + str(res.url)
        send_mail(body_data=msg, subject='{service_parameters['email_subject']}', recipients={recipients_})
    except Exception as e:
        if hasattr(e, 'message'):
            send_mail(body_data=str(e) + "<br>" + str(e.message), subject='AutoScraper - MAYA ERROR', recipients={recipients_})
        else:
            send_mail(body_data=str(e), subject='AutoScraper - MAYA ERROR', recipients={recipients_})
        """
    elif script_type == "QUERIES":
        return f"""
def use_fast_api(url_: str):
    try:
        json_encoded = '{service_parameters['json_encoded']}'
        json_string = base64.b64decode(json_encoded)
        queries_model = json.dumps(json.loads(json_string))
        queries_model['queries_model'] = ast.literal_eval(queries_model['queries_model'].replace('true', 'True'))
        res = requests.post(url=url_, data = queries_model)
        df = pd.DataFrame.from_dict(res.json()[0])
        send_mail(body_data=df.to_html(), subject='{service_parameters['email_subject']}', recipients={recipients_})
    except Exception as e:
        if hasattr(e, 'message'):
            send_mail(body_data=str(e) + "<br>" + str(e.message), subject='AutoScraper - QUERIES ERROR', recipients={recipients_})
        else:
            send_mail(body_data=str(e), subject='AutoScraper - QUERIES ERROR', recipients={recipients_})
        """
    else:
        return """"""


def create_dag(dag_data) -> Tuple[bool, str]: # Magic, Don't touch
    try:
        dag_str = get_custom_dag_data(
            DAG_DefaultArguments = dag_data['DAG_DefaultArguments'],
            DAG_Name = dag_data['DAG_Name'],
            DAG_Description = dag_data['DAG_Description'],
            DAG_CronOrKeyword = dag_data['DAG_CronOrKeyword'],
            Service_Type = dag_data['type_of_service'],
            Service_Parameters = dag_data['Service_Parameters'],
            _url_ = dag_data['ServiceLink'],
            recipients_ = dag_data['RECIPIENTS'],
            is_paused_upon_creation = dag_data['DEFAULT_STATE'],
        )
        if sys.platform.startswith('win'):
            path = r'C:\\Users\\t22q\\Desktop\\DSG\\AutoScraper\\AutoDAGs\\dags'
        else:
            path = r'/dags'
        return True, dag_str
    except Exception as e:
        print("create_dag:\n", str(e))
        return False, ""


def get_custom_dag_data(DAG_DefaultArguments: dict, DAG_Name: str, DAG_Description: str, DAG_CronOrKeyword: str, Service_Type: str, 
                            Service_Parameters: dict, _url_: str, recipients_: list, is_paused_upon_creation: bool) -> str:
    """
        Goal:
            Creating a custom dag in order to run the specified service script
        Arguments to fill:
         - ScriptFolder: str
         - Destination: str = Example: '/user/local/folder_3/another_folder/<insert destination folder>'
         - DAG_DefaultArguments: dict
                - owner: str = Creator of the DAG,
                - depends_on_past: boolean = False,
                - start_date: datetime(YEAR, MONTH, DAY) = When this DAG should start running
                - end_date: datetime(YEAR, MONTH, DAY) = When this DAG should stop running
                - email: ["airflow@example.com"],
                - email_on_failure: False,
                - email_on_retry: False,
                - #"retries": 1,
                - #"retry_delay": timedelta(minutes=60),
         - DAG_Name: str
         - DAG_Description: str
         - DAG_CronOrKeyword: str
         - ScriptName: str
        Returns the dag itself as a docstring
    """
    return f"""import os
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
import base64
from sendgrid import SendGridAPIClient
import datetime
import requests
import json
import pandas as pd
import base64
import ast
from airflow import DAG
from airflow.operators import PythonOperator
from airflow.operators.dummy_operator import DummyOperator


def send_mail(body_data: str = None, subject: str = None, file_location: str = None, file_name: str = None, recipients: list = [], _error_msg_: str = None):
    ".;.""
        Todays date will be added to the subject with a " - " before it
        Email will be sent from 'Cloudedge@BOI.org.il'
        Parameters:
            :param body_data -> str: The body that will be inside of the email
            :param subject -> str: The subject of the email
            :param file_location -> str: Location of the file that you want to send (need to be a full path)
            :param file_name -> str: Name of the file that you want to send
            :param recipients -> list: List of the people you wish that will receive this email
            :param _error_msg_ -> str: If you want you can specify the str of the error you want to get back if anything goes wrong
        Return a dictionary as follows:
            :attr Status -> str: Email response status
            :attr Body -> str: Body that was sent in this email
            :attr Headers -> str: The headers we got back form the email sending request
    ".;.""
    if not subject and not file_name:
        return _error_msg_ or "You must specify either a subject or a file name for this method mate ;)"
    os.environ["SENDGRID_API_KEY"] ="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"
    todaydate=datetime.datetime.today().strftime('%Y-%m-%d')
    to_emails = recipients
    _subject_ = subject or file_name.split('.')[0]
    _subject_ += " - " + todaydate
    try:
        message = Mail(
                from_email='Cloudedge@BOI.org.il',
                to_emails=to_emails,
                subject=_subject_,
                html_content=body_data
            )
        if file_location and file_name:
            with open(file_location, 'rb') as f:
                data = f.read()
                f.close()
            encoded_file = base64.b64encode(data).decode()
            attachedFile = Attachment(
                FileContent(encoded_file),
                FileName(file_name),
                FileType('application/pdf'),
                Disposition('attachment')
            )
            message.attachment = attachedFile
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        return ~
            "Status": response.status_code,
            "Body": response.body,
            "Headers": response.headers
        %.%
    except Exception as e:
        return _error_msg_ or str(e)

{get_service_function(Service_Type, Service_Parameters, recipients_)}

default_args = {DAG_DefaultArguments}

dag = DAG(
    "{DAG_Name}",
    description="{DAG_Description}",
    schedule_interval='{DAG_CronOrKeyword}',
    default_args=default_args,
    catchup=False,
    is_paused_upon_creation={is_paused_upon_creation},
)

start = DummyOperator(
    task_id='start',
    dag=dag
)

t_fastapi = PythonOperator(
    task_id='use_fast_api_function',
    python_callable=use_fast_api,
    op_kwargs=~"url_": '{_url_}'%.%,
    dag=dag
)

# sets downstream from start
start >> t_fastapi
""".replace("~", "{").replace("%.%", "}").replace(".;.", "")


def get_configurations(service_type: str, _ID_: str, cron: str, owner: str, start_date: datetime, end_date: datetime, 
                        params: dict, recipients_: list, default_state_: bool, description: str = default_desc) -> dict:
    # Parameters for the DAG - get them from the datalake or user
    dag_name = f"dag_{service_type.lower()}_{_ID_}"
    # Configurations for the DAG
    configs = {}
    configs['type_of_service'] = service_type
    configs['DAGsFolder'] = "dags"
    configs['DAG_Name'] = dag_name
    configs['DAG_Description'] = description
    configs['DAG_CronOrKeyword'] = cron
    configs['ServiceLink'] = get_service_link(service_type)
    configs['Service_Parameters'] = params
    configs['RECIPIENTS'] = recipients_
    configs['DEFAULT_STATE'] = default_state_
    configs['DAG_DefaultArguments'] = {
        "owner": owner,
        "depends_on_past": False,
        "start_date": start_date,
        "end_date": end_date,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
    }
    return configs


def get_plain_date(date_string) -> datetime:
    try:
        date_object = datetime.fromisoformat(date_string[:-1]).astimezone(timezone.utc)
        date_object = date_object.strftime('%Y-%m-%d')
        date_object = datetime.strptime(date_object, "%Y-%m-%d")
    except ValueError as ve:
        if str(ve).startswith("Invalid isoformat string"):
            date_object = datetime.strptime(date_string, "%Y-%m-%d")
    return date_object


def request_dag_creation(service_type_: str, id_: str, cron_: str, owner_: str, start_date_: str, end_date_: str, json_encoded_: str, email_subject_: str,
                                _recipients_list: str, filename_: str = None, extension_: str = None, default_state: bool = False) -> str:
    func_params = {
        "json_encoded": json_encoded_,
        "email_subject": email_subject_,
        "_file_name_": filename_,
        "_extension_": extension_
    }
    dag_configurations = get_configurations(
                            service_type=service_type_, _ID_=id_, cron=cron_, owner=owner_, 
                            start_date=get_plain_date(start_date_), end_date=get_plain_date(end_date_), 
                            params=func_params, recipients_=_recipients_list, default_state_=default_state, description=default_desc)
    _status_, new_dag = create_dag(dag_configurations)
    print(_status_)
    return new_dag
# Want to see recursion? look at the top of the file
