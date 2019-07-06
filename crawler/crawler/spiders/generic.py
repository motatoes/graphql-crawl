# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from pymongo import MongoClient

class GenericSpider(scrapy.Spider):
    name = 'generic'
    allowed_domains = ['generic.com']
    start_urls = []

    def __init__(self, start="http://bbc.co.uk"):
        self.allowed_domains = [start.replace("https://", "").replace("http://", "")]
        self.start_urls.append(start)

    def start_requests(self):
        self.MONGO_HOST = self.settings.attributes["MONGO_HOST"].value
        self.MONGO_USER = self.settings.attributes["MONGO_USER"].value
        self.MONGO_PASS = self.settings.attributes["MONGO_PASS"].value
        self.MONGO_PORT = self.settings.attributes["MONGO_PORT"].value

        print(self.MONGO_HOST, self.MONGO_PASS, self.MONGO_PORT, self.MONGO_USER)
        self.client = MongoClient(
            self.MONGO_HOST,
            username=self.MONGO_USER,
            password=self.MONGO_PASS,
            port=self.MONGO_PORT
        )
        self.db = self.client.crawl

        collection_name = self.allowed_domains[0]
        self.collection_name = re.sub(r"[\ \\\/\.]", "_", collection_name)
        
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        for link in LxmlLinkExtractor(allow=self.allowed_domains).extract_links(response):
            # print(link.url)
            yield scrapy.Request(link.url, self.parse)

        # extracting descriptiona and meta from site
        soup = BeautifulSoup(response.text, "lxml")

        title = soup.title.string
        og_type =  soup.find("meta",  property="og:type")
        og_site_name =  soup.find("meta",  property="og:site_name")
        og_image =  soup.find("meta",  property="og:image")
        og_title = soup.find("meta",  property="og:title")
        og_url = soup.find("meta",  property="og:url")
        raw_text = soup.get_text()
        
        og_type = og_type.get("content", None) if og_type else None
        og_site_name = og_site_name.get("content", None) if og_site_name else None
        og_image = og_image.get("content", None) if og_image else None
        og_title = og_title.get("content", None) if og_title else None
        og_url = og_url.get("content", None) if og_url else None

        collection = self.db.pages

        # update or insert
        collection.update(
            {"url": response.url},
            { 
                "$set": {
                    "url": response.url,
                    "domain": self.allowed_domains[0],
                    "title": title,
                    "og_type": og_type,
                    "og_site_name": og_site_name,
                    "og_image": og_image,
                    "og_title": og_title,
                    "og_url": og_url,
                    "raw_text": raw_text
              }
            },
            upsert=True
        )

