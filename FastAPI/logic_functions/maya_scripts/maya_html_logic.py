import json
import requests

# Author: Lidor Eliyahu Shelef

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
        'Page': page,
        'GroupData': [],
        'DateFrom': _from, # "2019-01-01T22:00:00.000Z",
        'DateTo': _to, # "2020-01-01T21:00:00.000Z",
        'Form': None,
        'IsBreakingAnnouncement': False,
        'IsTradeHalt': False,
        'IsForTaseMember': False,
        'IsSpecificFund': False,
        'Q': hebsource,
        'QOpt': 1,
        'ViewPage': 2
    }
    header = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'he-IL',
                'Connection': 'keep-alive',
                'Content-Length': '243',
                'Content-Type': 'application/json;charset=UTF-8',
                'Host': 'mayaapi.tase.co.il',
                'Origin':'https://maya.tase.co.il',
                'Referer': 'https://maya.tase.co.il/',
                'Sec-Fetch-Dest':'empty',
                'Sec-Fetch-Mode':'cors',
                'Sec-Fetch-Site':'same-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
                'X-Maya-With': 'allow',
                }

    with requests.Session() as session:
        r = session.post('https://mayaapi.tase.co.il/api/report/filter',data=json.dumps(payload), headers=header)
    return r


def download_html(source, hebsource, _from, _to):
    """
        Goal:
            Download the reports in an html format
        Parameters:
            :param source: source name, English version of the report name
            :param hebsource: report name in the hebrew language
            :param _from: from which date to download
            :param _to: till which date to download
    """
    r=get_data(1,hebsource, _from, _to)
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
            print('https://maya.tase.co.il/reports/details/'+str(rpt['RptCode']))
            h=str(rpt['RptCode'])
            companyId=str(rpt['Companies'][0]['CompanyEntity']['CompanyId'])
            files=rpt['Files']
            temp=[item for item in rpt['Files'] if item['Type']==1]
            if len(temp)>0:
                ind=sorted(temp, key = lambda i: i['Size'],reverse=True)[0]['Index']
                pubDate=str(rpt['PubDate'].split('T')[0].replace('-',''))
                print(companyId,pubDate,)
                c=len(h)-3
                rang1=(h[:c]+'001')
                rang2=(str(int(h[:c])+1)+'000')
                url='https://mayafiles.tase.co.il/RHtm/'+rang1+'-'+rang2+'/H'+str(h)+'.htm'
                print(url)
                res = requests.get(url)
                r = requests.get(url, stream=True)
                folder='{0}/'.format(source)
                with open(folder+companyId+'_'+pubDate+'.htm', 'wb') as f:
                    f.write(r.content)
                    num_jsons+=1
        r=get_data(page, hebsource, _from, _to)
        if len(r.json()['Reports'])>0:
            continiue=True
            num+=len(r.json()['Reports'])
        else:
            continiue=False
    print('All reports downladed successfully, {0} reports'.format(num_jsons))
    