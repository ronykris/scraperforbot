import scrapy
import re
from scrapy.linkextractors import LinkExtractor
import pandas as pd
import sys

#QUERYSTRING = 'not+getting+sleep'
#gURL = 'https://www.google.com/search?q='+QUERYSTRING



class gooSpider(scrapy.Spider):
    
    name = 'gooCrawler'
    start_urls = []
       

    def __init__(self, start_urls, QUERYSTRING, *argv, **kwargv):
        super(gooSpider, self).__init__(*argv, **kwargv)
        self.start_urls = start_urls
        self.QUERYSTRING = QUERYSTRING

    def request(self):
        scrapy.request(url=start_urls, callback=self.parse)
        
        
    def parse(self, response):

        #df = pd.DataFrame()        
        xlink = LinkExtractor()
        link_list=[]
        QUERYSTRING = ''

        #item = gooItem()    

        for link in xlink.extract_links(response):
            if len(str(link))>200 or QUERYSTRING in link.text:
                #print(len(str(link)), link.text,link, "\n")
                surl = re.findall('q=(http.*)&sa', str(link))   
                if surl:                      
                    link_list.extend(surl)
                  
        
        print(link_list)
        #item['links'] = link_list
        #return item                   
        #df['links']=link_list
        #df['link_text']=link_text
        #df['text_meta'] = text_list
        #df.to_csv('glinks.csv')

           