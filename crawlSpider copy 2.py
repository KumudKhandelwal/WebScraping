# -*- coding: utf-8 -*-
import scrapy
import csv
import re
import sys
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from testScrapeProject.items import TestscrapeprojectItem
from testScrapeProject import config



items = []

class ScrapySpider(CrawlSpider):
    # The name of the spider
    name = "scrapyspider_c2"

    # Starting URLs for each domain
    start_urls = config.EXTRACTING_URLS
   
    # The domains that are allowed (links to other domains are skipped)
    # Fetch the domains from a separate file 'settings.py' to make it more dynamic
    allowed_domains = [f"{url.replace('https://','').replace('www.','')}" for url in start_urls]
    
    # This spider has one rule: extract all (unique and canonicalized) links, follow them 
    # and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        rel_path = './downloaded_URLs_2'
        for url in self.start_urls:
            
            file = f"{rel_path}/{url.replace('https://','').replace('www.','').replace('/','.')}.csv"
            os.mkdir(file)
            os.chmod(file, 0o777)

            print("file... ", file)
            # print(os.path.exists(rel_path))
            with open(file, 'w+') as f_obj:
                yield scrapy.Request(
                    url, 
                    callback=self.parse_items,
                    dont_filter=True,
                    cb_kwargs={'f_obj':f_obj}
                )

    # Method for parsing items
    def parse_items(self, response, f_obj):
        # The list of items that are found on the particular page
        
        # Only extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        
        # Now go through all the found links
        for link in links:
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True

            # If it is allowed, create a new item and add it to the list of found items
            if is_allowed:
                global items
                item = TestscrapeprojectItem()
                item['url_from'] = response.url
                item['url_to'] = link.url
                if item not in items:
                    items.append(item)
                yield response.follow(link.url, callback=self.parse_items)
        
        for item in items:
            # rel_path = './downloaded_URLs_2'
            # if 'www' in response.url:
            #     file_name = f"{response.url.replace('https://www.', '').replace('/', '.')}"
            # else:
            #     file_name = f"{response.url.replace('https://', '').replace('/', '.')}"
            
            # write the URLs in a separate file with filename as that of domain
            # with open(f'{rel_path}/{file_name}.csv', 'a+') as f_obj:
                f_obj.write(item['url_to'])
                f_obj.write('\n')
                
        # Return all the found items
        return items