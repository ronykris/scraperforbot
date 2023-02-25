import scrapy
from scrapy.linkextractors import LinkExtractor
import pandas as pd

QUERYSTRING = 'not+getting+sleep'
gURL = 'https://www.google.com/search?q='+QUERYSTRING

class myspider(scrapy.Spider):
    name = 'corpusspider'
    start_urls = [gURL]

    def parse(self, response):
        df = pd.DataFrame()
        xlink = LinkExtractor()
        link_list=[]
        link_text=[]
        divs = response.xpath('//div')
        text_list=[]
        for span in divs.xpath('text()'):
            if len(str(span.get()))>100:
                text_list.append(span.get())
        for link in xlink.extract_links(response):
            if len(str(link))>200 or QUERYSTRING in link.text:
                #print(len(str(link)), link.text,link, "\n")
                link_list.append(link)
                link_text.append(link.text)
        for i in range(len(link_text)-len(text_list)):
            text_list.append(" ")
        df['links']=link_list
        df['link_text']=link_text
        df['text_meta'] = text_list
        df.to_csv('contents.csv')