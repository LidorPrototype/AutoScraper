import numpy as np
import pandas as pd
import requests
import os
import chardet

from logic_functions.general_utils import ensure_dir


def get_dataframe_data(_url):
    global wanted_columns
    response = requests.get(_url, allow_redirects=True)
    res_code = response.status_code
    if res_code != 200:
        return (pd.DataFrame, False)
    encoding_guess = chardet.detect(response.content)
    open('list_temp.csv', 'wb').write(response.content)
    fresh_df = pd.read_csv('list_temp.csv', encoding=encoding_guess['encoding'])[wanted_columns]
    os.remove('list_temp.csv')
    return (fresh_df, True)


def get_full_file(_base_url):
    global wanted_columns
    main_df = pd.DataFrame(columns=wanted_columns)
    status = True
    for page in range(1, 100):
        curr_url = base_url.format(page_num=page)
        (new_df, status) = get_dataframe_data(_base_url.format(page_num=page))
        if not status:
            break
        main_df = main_df.append(new_df)
    return main_df


def engineer_dataframe(old_df):
    new_df = old_df.copy()
    new_df['empty_col'] = " "
    new_cols_order = ['id', 'empty_col', 'time_value', 'data_value', 'price_value', 
                  'calc_value', 'unit_value', 'path_level1_value', 'update', 'obs_time_period', 'obs_value']
    new_df = new_df[new_cols_order]
    new_cols_name = ['id', 'LAMAS_SERIES_NAME', 'LAMAS_TIME_CODE', 'LAMAS_DATA_CODE', 'PRICE_CODE', 'CALC_CODE', 'UNIT_CODE', 
                 'TOP_CODE', 'PUBLISH_DATE', 'obs_time_period', 'obs_value']
    new_df.columns = new_cols_name
    return new_df


def run_file():
    global base_url, wanted_columns
    full_path = 'download_files/retails_trade.txt'
    ensure_dir(full_path.split('/')[0])
    base_url = "https://apis.cbs.gov.il/series/data/list?page={page_num}&PageSize=1000&id=3971,3972,3973,3974,3975,3976,3977,3978,3979,3980,3981,3982,3983,3984,3985,3986,3987,3988&format=csv"
    wanted_columns = ['id', 'time_value', 'data_value', 'price_value', 'calc_value', 'unit_value', 'path_level1_value', 'update', 'obs_time_period', 'obs_value']
    full_data = engineer_dataframe(get_full_file(base_url))
    full_data.to_csv(full_path, header=None, index=None, sep='|', mode='a') 
    return full_path
