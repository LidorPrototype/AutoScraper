import os
from maya_html import download_html
from maya_html_to_json import download_json
from maya_json_to_csv import json_to_csv
from maya_pdf import download_pdf


def ensure_dir(folder):
    """
        If the directory :folder: does not exists, create it
    """
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
    except OSError as e:
        raise
            

def activate_maya_logic(_source, _hebsource, _from, _to, _, _round=1):
    '''
        Parameters:
            :param _source: English report name and name of the saved directory
            :param _hesource: Hebrew report name
            :param _from: Start date
            :param _to: End date
            :param _: Flag to indicate which format to download the reports
        Return:
            :return source: Name of the file
    '''
    source=_source
    ensure_dir(source)
    hebsource=_hebsource
    if _ == "HTML":
        download_html(source, hebsource, _from, _to)
        return source
    elif _ == "JSON":
        download_json(source, hebsource, _from, _to)
        return source
    elif _ == "CSV": # Need to use the json first, then convert it to CSV
        if _round == 1:
            download_json(source, hebsource, _from, _to)
            return source
        if _round == 2:
            file_name = json_to_csv(source)
            return file_name
    elif _ == "PDF":
        download_pdf(source, hebsource, _from, _to)
        return source
        
        