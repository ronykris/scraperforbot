#!/usr/bin/env python3

import logging
import os
import scrapy
from scrapy.crawler import Crawler, CrawlerProcess
from scrapper import webSpider

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class scrape():

    def scrape_user_response(user_response):
        QUERY = user_response
        crawler = Crawler(webSpider)
        process = CrawlerProcess()
        process.crawl(webSpider, QUERY)
        process.start()  # the script will block here until the crawling is finished
        return QUERY.replace(" ","")+".txt"
