#!/usr/bin/env python3

import logging
import os
import scrapy
#from scrapy import signals
from scrapy.crawler import Crawler, CrawlerProcess
from itemadapter import ItemAdapter
from gooCrawler import gooSpider

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

QUERYSTRING = 'not+getting+sleep'
gURL = 'https://www.google.com/search?q='+QUERYSTRING
start_urls = [gURL]
gooLinks = []

#def getgooLinks(item, response, spider):
 #   items.append(item)
gc = gooSpider(start_urls,QUERYSTRING)
#gooLinks = gooItem()

crawler = Crawler(gooSpider)
#gS = gooSpider(gURL)
#crawler.signals.connect(getgooLinks, signals.item_scraped)

process = CrawlerProcess()
process.crawl(gooSpider, start_urls, QUERYSTRING)
process.start()  # the script will block here until the crawling is finished
print("links for corpus", gc.links)