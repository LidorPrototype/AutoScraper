import scrapy
from datetime import date
from scrapy.crawler import CrawlerProcess
import pandas as pd
import numpy as np


class TmpltSpider(scrapy.Spider):
    """
        A templater scrapy spider.
        Assumtions:
            - There is a csv folder containing:
                - urls.csv - Cannot be empty
                - prefix.csv
                - metadata.csv
                - queries.csv - Cannot be empty
    """
    name = 'tmplt'
    pre=np.array(pd.read_csv('csvs\\urls.csv').url)
    print(pre)
    prefixurl = ""
    try:
        prefixurl=np.array(pd.read_csv('csvs\\prefix.csv').prefix)[0]
    except IndexError:
        prefixurl = ""
    namemeta=pd.read_csv('csvs\\metadata.csv')
    namemeta=dict(zip(namemeta.name, namemeta.value))
   
    namequery=pd.read_csv('csvs\\queries.csv')
    namequery=dict(zip(namequery.name, namequery['query']))
    
    def start_requests(self):
        for i in self.pre:
            yield scrapy.Request(url = i,
                         callback = self.parse_front)

    def parse_front(self, response):
        links_to_follow=response.xpath('//@href').extract()
        links_to_follow=[link for link in links_to_follow if link.startswith(self.prefixurl)]
        links_to_follow = list(dict.fromkeys(links_to_follow))
    
        print(links_to_follow)
        for url in links_to_follow:
            try:
                yield response.follow(url = url,callback = self.parse)
            except Exception:
                   print('error parse_front')                         
 
    def parse(self, response):
        try:
            scraped_info={'page':response.url}
            for key, value in self.namequery.items():
                scraped_info[key]=response.xpath(value).extract_first()             
            scraped_info.update(self.namemeta)
            yield scraped_info

            NEXT_PAGE_SELECTOR = '.ui-pagination-active + a::attr(href)'
            next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
            if next_page:
                yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse)
        except Exception as e:
            print('error parse')
            print(e)