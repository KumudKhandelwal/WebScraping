# -*- coding: utf-8 -*-
import scrapy
import csv
import re
import sys
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from testScrapeProject.items import TestscrapeprojectItem


class ScrapySpider(CrawlSpider):
    # The name of the spider
    name = "scrapyspider"

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = [
        'lincoln.fr'
        # 'quantmetry.com'
        # 'businessdecision.fr'
        # 'avisia.fr'
        # 'aneo.eu'
        # 'epsilon-france.com/fr'
        # 'umanis.com/fr'
        # 'aid.fr'
        # 'keyrus.com'
        # 'datavalue-consulting.com'
        ]
    
    # The URLs to start with
    start_urls = [
        f"https://www.{allowed_domains[0]}/"
        ]
    
    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
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
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_items, dont_filter=True)

    # Method for parsing items
    def parse_items(self, response):
        # The list of items that are found on the particular page
        items = []
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
                item = TestscrapeprojectItem()
                item['url_from'] = response.url
                item['url_to'] = link.url
                items.append(item)
                # yield response.follow(link.url, callback=self.parse_items)
        item_url_to = []
        for item in items:
            item_url_to.append(item['url_to'])

            with open(f"downloaded_URLs/{self.allowed_domains[0].replace('/', '.')}.csv", 'a+') as f_obj:
                f_obj.write(item['url_to'])
                f_obj.write('\n')
                
        # print(item_url_to)
        # Return all the found items
        return items