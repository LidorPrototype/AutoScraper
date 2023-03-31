import pandas as pd

from logic_functions.queries_scripts import generic_scrapy_builder as gsb
from logic_functions.general_utils import ensure_dir

# Author: Lidor Eliyahu Shelef

def use_xpath_scraping(data, _ = False):
    """
        Goal:
             a little validation (the rest is getting checked at the utils file), and
             activatin the generic scrapy and afterwards let the user download the results
        Parameters:
            :param data: dictionary holding all the wanted data from the user
             - data keys:
                - urls: list of urls the user want to scrape through
                - prefixes: list of prefixes the user would like to add (usually there is only 1)
                - metadata: dictionary holding the metadata, keys:
                    - names: list of names for the metadata values
                    - values: list of values to be put as the metadata
                - queries: dictionary holding the queries, keys:
                    - names: list of names for each query data
                    - xpaths: list of xpaths commands to be run
        Returns:
            :return status: Status of the scraping
            :return result_df or pd.DataFrame(): Result dataframe or an empty one in case of any problems
    """    
    result_df = pd.DataFrame()
    path_to_vir_env = "demo/AutoScraperSpiders"
    template_path = "demo/tmplt.py"
    ensure_dir(path_to_vir_env)
    split_metadata = {
        "names": list(data['metadata'].keys()),
        "values": list(data['metadata'].values())
    }
    split_queries = {
        "names" : list(data['queries'].keys()),
        "xpaths": list(data['queries'].values())
    }
    (result_df, status) = gsb.gs_builder(
                                path_vir_env=path_to_vir_env, 
                                src_tmplt=template_path,
                                project=data['project'], 
                                out=data['out'], 
                                urls=data['urls'], 
                                prefixes=data['prefixes'], 
                                metadata=split_metadata, 
                                queries=split_queries
                            )
    return result_df, status
    if not result_df.empty:
        return result_df, status
    else:
        return pd.DataFrame(), status
