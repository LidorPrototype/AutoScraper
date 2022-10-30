import json
import requests
import pandas as pd
import time
from scrapy import Selector


def get_data(page, hebsource, _from, _to):
    """
        Goal:
            Getting the data from the desired webstie
        Parameters:
            :param page: desired page to download
            :param hebsource: report name in the hebrew language
            :param _from: from which date to download
            :param _to: till which date to download
    """
    payload = {
        'DateFrom': _from, # "2019-01-01T22:00:00.000Z",
        'DateTo': _to, # "2020-01-01T21:00:00.000Z",
        'Form': None,
        'GroupData': [],
        'IsBreakingAnnouncement': False,
        'IsForTaseMember': False,
        'IsSpecificFund': False,
        'IsTradeHalt': False,
        'Page': page,
        'Q': hebsource,
        'QOpt': 1,
        'ViewPage': 2
    }
    header = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'he-IL',
                'Connection': 'keep-alive',
                'Content-Length':'243',
                'Content-Type': 'application/json;charset=UTF-8',
                'Host': 'mayaapi.tase.co.il',
                'Origin':'https://maya.tase.co.il',
                'Referer': 'https://maya.tase.co.il/',
                'sec-ch-ua': '"Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                'sec-ch-ua-mobile': '?0',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'X-Maya-With': 'allow'
                }

    with requests.Session() as session:
        r = session.post('https://mayaapi.tase.co.il/api/report/filter',data=json.dumps(payload),
                         headers=header)
    return r


def download_json(source, hebsource, _from, _to):
    """
        Goal:
            Download reports in a json format from the html
        Parameters:
            :param source: source name, English version of the report name
            :param hebsource: report name in the hebrew language
            :param _from: from which date to download
            :param _to: till which date to download
    """
    r=get_data(1, hebsource, _from, _to)
    page=1
    continiue=False
    num=0
    num_jsons=0
    if len(r.json()['Reports'])>0:
        num=len(r.json()['Reports'])
        continiue=True
    while(continiue):
        print("Number of reports:{0}".format(num))
        page+=1
        for rpt in r.json()['Reports']:
            h=str(rpt['RptCode'])
            rang1=(h[:4]+'001')
            rang2=(str(int(h[:4])+1)+'000')
            url='https://mayafiles.tase.co.il/RHtm/'+rang1+'-'+rang2+'/H'+h+'.htm'
            print(url)
            res = requests.get(url)
            res.encoding =res.apparent_encoding
            sel=Selector(text=res.text)
            values=sel.xpath('//*[@fieldalias!="" and text()!=""]/text()').extract()
            keys=sel.xpath('//*[@fieldalias!=""  and text()!=""]/@fieldalias').extract()
            d=dict(rpt)
            if len(keys)>0:
                for k,v in zip(keys,values):
                    if k in d.keys():
                        d[k].append(v)
                    else:
                        d[k]=list()
                        d[k].append(v)

                folder='{0}/'.format(source)
                with open(folder+str(rpt['RptCode'])+'.json', 'w', encoding='utf-8') as f:
                    json.dump(d, f, ensure_ascii=False, indent=4)
                    num_jsons+=1
        r=get_data(page, hebsource, _from, _to)
        if len(r.json()['Reports'])>0:
            continiue=True
            num+=len(r.json()['Reports'])
        else:
            continiue=False
    print('All reports downladed successfully, {0} reports'.format(num_jsons))



