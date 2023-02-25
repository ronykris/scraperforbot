import scrapy
import re
from scrapy.linkextractors import LinkExtractor
import sys
from scrapy import Selector


gURL = 'https://www.google.com/search?q='


class webSpider(scrapy.Spider):
    
    name = 'webCrawler'
    start_urls = []
    QUERYSTRING = ''    
    body = ""
    starturl = gURL+QUERYSTRING

    def __init__(self, QUERY, *argv, **kwargv):
        super(webSpider, self).__init__(*argv, **kwargv)        
        self.QUERYSTRING = QUERY
        self.start_urls = [gURL+QUERY]
        
            
    #def request(self):
    #    scrapy.request(url=gURL+self.QUERYSTRING, callback=self.parse)

    def getBody(self, response):
            sel = Selector(response)
            #patterns = '//body//div//p//text()' or '//body//section//article//div//p//text()'
            body = "".join(sel.xpath('//body//div//p//text()').extract()).strip()
            print(body)
            #f = open("content.txt", "a+")
            #textfile = self.QUERYSTRING.replace(" ","")+".txt"
            textfile = "content.txt"
            f = open(textfile, "a+")
            f.write(body)
            f.close()


    def parse(self, response):
        
            xlink = LinkExtractor()
            link_list=[]
            
            for link in xlink.extract_links(response):
                if len(str(link))>200 or self.QUERYSTRING in link.text:
                    #print(len(str(link)), link.text,link, "\n")
                    surl = re.findall('q=(http.*)&sa', str(link))   
                    if surl:                      
                        link_list.extend(surl)                  
            
            print(link_list)
            #self.start_urls = link_list
            for url in link_list:
                yield scrapy.Request(url,callback=self.getBody)

      