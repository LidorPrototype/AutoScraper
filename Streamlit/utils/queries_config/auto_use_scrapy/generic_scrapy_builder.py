import os
import pandas as pd
import streamlit as st
from shutil import copy


def startScrappy(_path_cmd_to_virtual, project_name, _outputname, scraper_name='tmplt'):
    """
        Goal:
            This function is activating and running the Scrapy spider in the given path based on its project name
        Parameters:
            - _path_cmd_to_virtual : Path to the virtual enviroment that we are activating including the cmb commands, such as -> 'cd../demo'
            - project_name : Name of the scrapy project, such as ->'onlinePrices'
            - _outputname : Name of the output file where everything will be saved, such as -> 'tester.csv'
            - scraper_name : Name of the spider itself, such as -> 'zara'
    """
    os.system(_path_cmd_to_virtual[:-len("\\AutoScraperSpiders")] + " && my_env\\scripts\\activate && " + " cd AutoScraperSpiders\\" + project_name + " && scrapy crawl -o " + _outputname + " " + scraper_name)


def createProject(_path_cmd_to_virtual, project_name):
    """
        Goal:
            This function is creating a new Scrapy project with the name of project_name
        Parameters:
            - _path_cmd_to_virtual : Path to the virtual enviroment that we are activating including the cmb commands, such as -> 'cd../demo'
            - project_name : Name of the scrapy project, such as ->'onlinePrices'
        'Scrapy startproject name_of_project'
    """
    os.system(_path_cmd_to_virtual[:-len("\\AutoScraperSpiders")] + '&& my_env\\scripts\\activate && ' + _path_cmd_to_virtual + ' && Scrapy startproject ' + project_name)


def insertTemplateSpider(_path_to_template, _path_to_spider_dest):
    """
        Goal:
            This function is taking the template from the _path_to_template and copying it to the _path_to_spider_dest location
        Parameters:
            - _path_to_template : Path to the template of the generic spider we are using
            - _path_to_spider_dest : Path of the directory which we want the spider to be in
    """
    copy(_path_to_template, _path_to_spider_dest)
    
    
def createCSVsFolder(_path_to_spider_folder):
    """
        Goal:
            This function is creating the folder for all the 4 csv files that the generic spider will use
        Parameters:
            - _path_to_spider_folder : Path to the directory the spider folder in (the one that is one above the one with the configuration scripts)
    """
    _path = _path_to_spider_folder + '\\csvs'
    if not os.path.exists(_path):
        os.makedirs(_path)


def createURLs(_urls, _path_to_spider_folder):
    """
        Goal:
            This function is creating a csv file with all of the user given urls, in the _path_to_spider_folder location
        Parameters:
            - _urls : List of user given urls that we need to scrape
            - _path_to_spider_folder : Path to the directory the spider folder in (the one that is one above the one with the configuration scripts)
    """
    df = pd.DataFrame({'url':_urls})
    df.to_csv(_path_to_spider_folder + '\\urls.csv', index=False, sep=',')
    

def createPrefixes(_prefix, _path_to_spider_folder):
    """
        Goal:
            This function is creating a csv file with all of the user given prefixes, in the _path_to_spider_folder location
        Parameters:
            - _prefix : List of user given _prefix that we need to add to our url to scrape from scrape
            - _path_to_spider_folder : Path to the directory the spider folder in (the one that is one above the one with the configuration scripts)
    """
    df = pd.DataFrame({'prefix': _prefix})
    df.to_csv(_path_to_spider_folder + '\\prefix.csv', index=False, sep=',')
    

def createMetadatas(_metadata_names, _metadata_values, _path_to_spider_folder):
    """
        Goal:
            This function is creating a csv file with all of the user given metadata, in the _path_to_spider_folder location
            Metadata will be made with the 'name,value' of each metadata each in individual line
        Parameters:
            - _metadata_names : List of names to the metadata that the user wants to add
            - _metadata_values : List of values to each of the metadata names we got
            - _path_to_spider_folder : Path to the directory the spider folder in (the one that is one above the one with the configuration scripts)
    """
    df = pd.DataFrame({'name': _metadata_names, 'value': _metadata_values})
    df.to_csv(_path_to_spider_folder + '\\metadata.csv', index=False, sep=',')
    

def createQueriess(_query_names, _query_xpaths, _path_to_spider_folder):
    """
        Goal:
            This function is creating a csv file with all of the user given queries, in the _path_to_spider_folder location
            Queries will be made with the 'name,xpath' of each query each in individual line
        Parameters:
            - _query_names : List of names of the fields that each query represent
            - _query_xpaths : List of xpaths to run, each xpath is a different query for us
            - _path_to_spider_folder : Path to the directory the spider folder in (the one that is one above the one with the configuration scripts)
    """
    df = pd.DataFrame({'name': _query_names, 'query': _query_xpaths})
    df.to_csv(_path_to_spider_folder + '\\queries.csv', index=False, sep=',')
    

def retrieve_data(path_to_data):
    """
        Parameters:
            - path_to_data: Path of the csv output file
    """
    try:
        return pd.read_csv(path_to_data)
    except:
        return pd.DataFrame()


def gs_builder(path_vir_env=None, project=None, out=None, src_tmplt=None, urls=[], prefixes=[""],metadata={"names": [""], "values": [""]}, queries={"names": [""], "xpaths": [""]}):
    """
        Goal:
            Responisble on initiating and assigning all the needer variables and make the entire autoscrapy flow work in order
        Parameters:
            *** None parameters are a must, it can run on empty and result as an empty csv file ***
            - path_vir_env: A cmd command to mode from the current location to the location the virtual enviroment is in, for 
                             now it includes a special folder that will contain everything from this method and sub-methods
            - project: Name for this project
            - out: Name for the output file that will hold all of the scraped data
            - src_tmplt: Path to the location where the template file (spider) is located at
            - urls: List of all wanted urls to scrape
            - prefixes: List of prefixes to be added to the scraping requests, will take for now the first one only
            - metadata: Dictionary with 2 keys: 'names', 'values'
                - names: List of names to be given to the metadata fields
                - values: List of values / example values to be added as metadata
            - queries: Dictionary with 2 keys: 'names', 'xpaths'
                - names: List of names to be given to the xpaths fields
                - xpaths: List of actual xpath queries, this are the queries that will be used in order to scrape the data
    """
    if len(urls) == 0:
        return (pd.DataFrame(), "Error, please provide at least 1 url mate...")
    if not bool(metadata):
        metadata={"names": [""],"values": [""]}
    if not bool(queries):
        return (pd.DataFrame(), "Error, please provide at least 1 query data mate...")
    else:
        if "" in [item.strip() for item in queries['names']] or not bool(queries['names']):
            return (pd.DataFrame(), "Error, please fill all the queries names mate...")
        if "" in [item.strip() for item in queries['xpaths']] or not bool(queries['xpaths']):
            return (pd.DataFrame(), "Error, please fill all the queries xpaths mate...")
    default_project_name = 'tester_temp'
    _path_to_virtual_env = f'cd {path_vir_env}' or 'cd demo\\AutoScraperSpiders' # cd../demo
    _project = project or default_project_name           # Get from user
    _output = out or f'{default_project_name}.csv'       # Get from user
    _scrap_name = 'tmplt'
    _source_template = src_tmplt or 'AutoScraper\\utils\\queries_config\\auto_use_scrapy\\tmplt.py'
    _spider_dest = f'demo\\AutoScraperSpiders\\{_project}\\{_project}\\spiders'
    _path_to_spider_folder = f'demo\\AutoScraperSpiders\\{_project}'
    _path_to_csvs_folder = f'demo\\AutoScraperSpiders\\{_project}\\csvs'
    _urls = urls                                    # Get from user -> ["https://www.ynet.co.il/news/category/185"]
    _prefixes = prefixes                            # Get from user -> ['https://www.ynet.co.il/news/article']
    _metadatas_names = metadata["names"]            # Get from user -> ['date', 'source']
    _metadatas_values = metadata["values"]          # Get from user -> ['02-11-2021', 'ynet']
    _queries_names = queries["names"]               # Get from user -> ['title']
    _queries_xpaths = queries["xpaths"]             # Get from user -> ['//h1[@class="mainTitle"]/text()']

    # Main Flow - Creation
    createProject(_path_to_virtual_env, _project)                                   # V
    insertTemplateSpider(_source_template, _spider_dest)                            # V
    createCSVsFolder(_path_to_spider_folder)                                        # V
    createURLs(_urls, _path_to_csvs_folder)                                         # V
    createPrefixes(_prefixes, _path_to_csvs_folder)                                 # V
    createMetadatas(_metadatas_names, _metadatas_values, _path_to_csvs_folder)      # V
    createQueriess(_queries_names, _queries_xpaths, _path_to_csvs_folder)           # V
    # Main Flow - Execution
    startScrappy(_path_to_virtual_env, _project, _output, _scrap_name)              # V
    path_and_name = f"{_path_to_spider_folder}/{_output}"
    st.write(path_and_name)
    df = retrieve_data(path_and_name)                                               # V
    return (df, "Success")

