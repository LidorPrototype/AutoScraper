import json2csv
import glob
import pandas as pd
import os
import time


def json_to_csv(_source):
    """
        Goal:
            Converting a json file to a csv file
        Parameter:
        :param _source: report name in the English language
    """
    df_list=list()
    source=_source
    json_files = [pos_json for pos_json in os.listdir(source) if pos_json.endswith('.json')]
    i=0
    for file in glob.glob("{0}/*.json".format(source)):
        #print(file)
        with open(file,encoding='utf-8') as f:
            df=json2csv.json2csv(f)
            df_list.append(df)
    df_all=pd.concat(df_list)
    #df_all=df_all.drop_duplicates()
    df_all.reset_index(drop=True)
    file_name = source+time.strftime("%Y%m%d_%H%M%S")+'.csv'
    df_all.to_csv(file_name,encoding='utf-8-sig')
    return file_name
    