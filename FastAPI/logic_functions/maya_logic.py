import os
import shutil
import io
from fastapi.responses import StreamingResponse

from logic_functions.maya_scripts.maya_pdf_logic import download_pdf
from logic_functions.maya_scripts.maya_html_logic import download_html
from logic_functions.maya_scripts.maya_html_2_json_logic import download_json
from logic_functions.maya_scripts.maya_json_2_csv_logic import download_csv
from logic_functions.general_utils import ensure_dir, check_data_validity
# Import Keys
from logic_functions.general_utils import MAYA_HTML_KEY, MAYA_JSON_KEY, MAYA_CSV_KEY, MAYA_PDF_KEY

# Author: Lidor Eliyahu Shelef

def download_maya_csv(english_report_name, hebrew_report_name, start_date_period, end_date_period):

    file_name = f"download_files/Maya/{english_report_name}_html_format.zip"
    ensure_dir(file_name[:-4])
    file_name = download_csv(file_name[:-4], hebrew_report_name, start_date_period, end_date_period)

    validity, v_msg = check_data_validity(file_name, MAYA_CSV_KEY)
    if not validity:
        return v_msg

    temp_file = None
    with open (file_name, mode="rb") as _f:
        temp_file = _f.read()
    final_file = io.BytesIO(temp_file)
    shutil.rmtree("download_files/Maya")

    return StreamingResponse(final_file)


def download_maya_json(english_report_name, hebrew_report_name, start_date_period, end_date_period):

    file_name = f"download_files/Maya/{english_report_name}_html_format.zip"
    ensure_dir(file_name[:-4])
    download_json(file_name[:-4], hebrew_report_name, start_date_period, end_date_period)

    validity, v_msg = check_data_validity(file_name[:-4], MAYA_JSON_KEY)
    if not validity:
        return v_msg

    shutil.make_archive(file_name[:-4], file_name[-3:], file_name[:-4])
    temp_file = None
    with open (file_name, mode="rb") as _f:
        temp_file = _f.read()
    final_file = io.BytesIO(temp_file)
    shutil.rmtree("download_files/Maya")
    # This comment is self explanatory.
    return StreamingResponse(final_file)


def download_maya_pure_html(english_report_name, hebrew_report_name, start_date_period, end_date_period):

    file_name = f"download_files/Maya/{english_report_name}_html_format.zip"
    ensure_dir(file_name[:-4])
    download_html(file_name[:-4], hebrew_report_name, start_date_period, end_date_period)

    validity, v_msg = check_data_validity(file_name[:-4], MAYA_HTML_KEY)
    if not validity:
        return v_msg

    shutil.make_archive(file_name[:-4], file_name[-3:], file_name[:-4])
    temp_file = None
    with open (file_name, mode="rb") as _f:
        temp_file = _f.read()
    final_file = io.BytesIO(temp_file)
    shutil.rmtree("download_files/Maya")

    return StreamingResponse(final_file)


def download_maya_pdf(english_report_name, hebrew_report_name, start_date_period, end_date_period):
    
    file_name = f"download_files/Maya/{english_report_name}_pdf_format.zip"
    ensure_dir(file_name[:-4])
    download_pdf(file_name[:-4], hebrew_report_name, start_date_period, end_date_period)

    validity, v_msg = check_data_validity(file_name[:-4], MAYA_PDF_KEY)
    if not validity:
        return v_msg

    shutil.make_archive(file_name[:-4], file_name[-3:], file_name[:-4])
    temp_file = None
    with open (file_name, mode="rb") as _f:
        temp_file = _f.read()
    final_file = io.BytesIO(temp_file)
    shutil.rmtree("download_files/Maya")

    return StreamingResponse(final_file)
