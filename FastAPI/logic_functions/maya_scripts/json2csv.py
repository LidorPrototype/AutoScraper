#!/usr/bin/env python
# coding: utf-8

import json 
import pandas as pd 
from pandas.io.json import json_normalize
from pandas.io.json import build_table_schema

def json2csv(f):
    """
        Goal:
            Converting a json file into a csv file
        Parameters:
            :param f: file path
    """
    try:
        d=json.load(f,encoding='utf-8')
    except:
        d=json.load(f)
    fields=dict()
    columns_main=list()
    for k,v in d.items():
        if k not in ['Companies', 'Files']:
            if isinstance(d[k],str) or isinstance(d[k],int):
                columns_main.append(k)
            elif isinstance(d[k],list) and len(d[k])==1:    
                columns_main.append(k)
            elif isinstance(d[k],list) and len(d[k])>1:
                fields[k]=len(d[k])
    df = pd.json_normalize(d)
    df=df.drop(['Companies', 'Files'], axis=1)
    for c in columns_main:
        df[c]=df[c].apply(lambda x: x[0] if (type(x)==list and len(x)==1) else x)
        df[c]=df[c].apply(lambda x: '' if (type(x)==list and len(x)==0) else x)
    first=True
    sort_fields = sorted(fields.items(), key=lambda x: x[1], reverse=False)
    
    if not bool(fields):
        return df
    else:
        for value in sort_fields:
            f=value[0]
            columns=list(columns_main)
            columns.append(f)
            if first:
                df_temp=df[columns].copy(deep=True)
                df_new=df_temp[f].apply(pd.Series).merge(df_temp, right_index = True, left_index = True).drop([f], axis = 1).melt(id_vars =columns_main, value_name = f).drop("variable", axis = 1).dropna()
                first=False

            elif df_new.shape[0]<value[1]:
                df=pd.concat([df]*df_new.shape[0]).reset_index().drop("index", axis = 1)
                df_temp=df[columns].copy(deep=True)
                df_new=pd.concat([df_new]*value[1]).reset_index().drop("index", axis = 1)
                df_new[f]=df_temp[f].apply(pd.Series).merge(df_temp, right_index = True, left_index = True).drop([f], axis = 1).melt(id_vars =columns_main, value_name = f).drop("variable", axis = 1).dropna()[f]
            else:
                df_temp=df[columns].copy(deep=True)
                df_new[f]=df_temp[f].apply(pd.Series).merge(df_temp, right_index = True, left_index = True).drop([f], axis = 1).melt(id_vars =columns_main, value_name = f).drop("variable", axis = 1).dropna()[f]
    return df_new
