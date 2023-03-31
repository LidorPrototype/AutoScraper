from typing import Dict, List
from datetime import datetime
from pydantic import BaseModel

# Author: Lidor Eliyahu Shelef
#
#    ROFL:ROFL:LOL:ROFL:ROFL
#        ______/|\____
#  L    /          [] \
# LOL===_      ROFL    \_
#  L     \_______________]
#            I      I
#        /---------------/

class RawModel(BaseModel):
    """
        Raw service model in order to get all the parameters in one place at the request body
        Parameters:
            :param url: A string representation of the url to scrape from
            :param duplications: A boolean flag indicates if I should remove duplications or not
            :param parameters: A Dictionary that holds all of the parameters for the scraping itself
                                            Dictionary format should be: {field_name: field_values}
                                            Dictionary types should be: {str: list}
    """
    url: str
    duplications: bool
    parameters: Dict[str, List[str]]

class MayaModel(BaseModel):
    """
        Maya service model in order to get all the parameters in one place at the request body
    """
    service_type: str
    eng_report: str
    heb_report: str
    start_date: str
    end_date: str
    inner_format: str

class QueriesModel(BaseModel):
    """
        Queries based service responsible for the XPATH scraping
        Parameters:
            :param urls: List of urls to scrape
            :param prefixes: List of prefixes for each url
            :param metadata: Dictionary of metadata (name: value)
            :param queries: Dictionary of queries to run (name: xpath)
            :param project: Project name
            :param out: Project output file name
    """
    urls: List[str] = None
    prefixes: List[str] = None
    metadata: Dict[str, str]
    queries: Dict[str, str]
    project: str = None
    out: str = None

class EmailsModel(BaseModel):
    """
        Holds an email object data, related to the email sending mechanism
        Parameters:
            :param recipients: Recipients of the email
            :type recipients: list
            :param email_subject: Email subject
            :type email_subject: str
            :param email_body: Email body data
            :type email_body: str
    """
    recipients: list = None
    email_subject: str = None
    email_body: str = None

class TableEntityModel(BaseModel):
    """
        Representing the entity that is to be inserted / updated in the Azure Datalake
    """
    DestinationID: str
    cron: str
    end_date: str
    start_date: str
    serviceID: str
    description: str
    user: str
    output_name: str
    parameters: str = None

