import pdfplumber
import fitz
import tabula as tb
import pandas as pd
import re
import glob
import shutil

from logic_functions.general_utils import ensure_dir

# Author: Lidor Eliyahu Shelef

def get_text_in_area(raw_text, from_text: str = None, to_text: str = None) -> str:
    text_in_area = ""
    if from_text:
        start_idx = raw_text.find(from_text)
    if to_text:
        end_idx = raw_text.find(to_text)
    if from_text and to_text:
        text_in_area = raw_text[start_idx:end_idx]
    elif from_text:
        text_in_area = raw_text[start_idx:]
    elif to_text:
        text_in_area = raw_text[:end_idx]
    else:
        text_in_area = raw_text
    return text_in_area

# --------------------------------------------------------------------------------
def get_entire_pdf_as_str(pdf_file_path, from_text: str = None, to_text: str = None, page_devider = "\n") -> str:
    """
        Option 1: mix the next 2 methods (use them in this one)
        Option 2: https://towardsdatascience.com/how-to-extract-text-from-pdf-245482a96de7
    """
    with fitz.open(pdf_file_path) as doc:
        text = ""
        for page in doc:
            text += re.sub(r'\n+', '\n', page.get_text()).strip()
            text += page_devider
    return text
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
def get_text_ignore_tables(pdf_path, from_text: str = None, to_text: str = None) -> str:
    clean_text = get_text_without_tables_data(pdf_path)
    return get_text_in_area(clean_text, from_text, to_text)


def get_text_without_tables_data(pdf_file_path) -> str:
    def not_within_bboxes(obj):
        """
            Goal:
            Check if the object is in any of the table's bbox.
        """
        def obj_in_bbox(_bbox):
            """
                Methos is based on:
                    - https://github.com/jsvine/pdfplumber/blob/stable/pdfplumber/table.py#L404
            """
            v_mid = (obj["top"] + obj["bottom"]) / 2
            h_mid = (obj["x0"] + obj["x1"]) / 2
            x0, top, x1, bottom = _bbox
            return (h_mid >= x0) and (h_mid < x1) and (v_mid >= top) and (v_mid < bottom)
        return not any(obj_in_bbox(__bbox) for __bbox in bboxes)


    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            full_raw_text = page.extract_text()
            try:
                bboxes = [
                    table.bbox
                    for table in page.find_tables(
                        table_settings={
                            "vertical_strategy": "explicit",
                            "horizontal_strategy": "explicit",
                            "explicit_vertical_lines": page.curves + page.edges,
                            "explicit_horizontal_lines": page.curves + page.edges,
                        }
                    )
                ]
                text_without_tables = page.filter(not_within_bboxes).extract_text()
                return text_without_tables
            except:
                return full_raw_text
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
def get_tables_only(pdf_file_path) -> str:
#   # Ugly but working way - returns as a big csv file format
    # The parameter :combined_csv: is a beautiful DataFrame, but for some reason I can return it
    #  it causes many errors that I'm yet to understand so for now it gets converted to a csv file 
    #  using the method "to_csv" of the pandas library
    data = pd.DataFrame()
    csvs_dir = 'csvs_files'
    ensure_dir(csvs_dir)
    try:
        data=tb.read_pdf(pdf_file_path, multiple_tables=True, pages='all')
        for idx, df in enumerate(data):
            df.to_csv(f'{csvs_dir}/table_{idx}.csv')
        all_filenames = [i for i in glob.glob(csvs_dir + '/*.csv')]
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
        return combined_csv.to_csv()
    except Exception as e:
        return "No Tables Found Mate!", "ERROR: " + str(e)
    finally:
        shutil.rmtree(csvs_dir)
# --------------------------------------------------------------------------------
