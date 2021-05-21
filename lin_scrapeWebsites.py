# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scraper import config

class ScrapySpider(CrawlSpider):
    # The name of the spider
    name = "scrape_websites"

    # Starting URLs for each domain
    start_urls = config.EXTRACTING_URLs
    # start_urls = ['https://dexi.io']  # url for testing the algorithm
    
    # The domains that are allowed (links to other domains are skipped)
    # Fetch the domains from a separate file 'config.py' to make it more dynamic
    allowed_domains = [f"{url.replace('https://','').replace('www.','')}" for url in start_urls]
    
    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        for url in self.start_urls:
            rel_path = './supporting_files/lin_scraped_URLs1'
            if not os.path.exists(rel_path):
                os.mkdir(rel_path)
            if 'www' in url:
                file_name = f"{url.replace('https://www.', '').replace('/', '.')}"
            else:
                file_name = f"{url.replace('https://', '').replace('/', '.')}"
            
            file_path = f'{rel_path}/{file_name}.txt'
                
        # create the file as below
            with open(file_path, 'w+', encoding='UTF8'):
                # We just want to create the file, so just pass the body.
                # We will write to this file later post urls have been scraped.
                pass
        
            yield scrapy.Request(url, callback=self.parse, dont_filter=True, cb_kwargs=dict(file_path=file_path))
    
    # method to parse main url
    def parse(self, response, file_path):
        urls = self.process_requests(response, file_path)
        
        # for each url scapred from main url, crawl over each of them and scrape new urls
        for url in urls:
            yield response.follow(url, callback=self.parse_urls, dont_filter=True, cb_kwargs=dict(file_path=file_path))
        
        return None
    
    # method to parse all sub-urls
    def parse_urls(self, response, file_path):
        self.process_requests(response, file_path)
        return None

    def process_requests(self, response, file_path):
        # Only extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        # 1. For each fetched link, verify that the link is an allowed one and not blacklisted too
        # 2. Once verified, append it to a temporary list
        # Once all the urls have gone through step 1 and 2, return the final list
        urls = self.verify_and_append_urls(links)
        # For each url in the final list, check if it has already been written to the output file.
        # If not already been written, write it. Otherwise, ignore and skip.
        self.write_to_file(file_path, urls)
        return urls

    def verify_and_append_urls(self, links):
        # list to store the scraped URLs
        urls = []
        # list of domains not permitted for scraping because of irrelevance to the project
        blacklisted_domains = config.BLACKLISTED_DOMAINS
        # Now go through all the found links
        for link in links:
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            # Check whether the domain of the URL is not in blacklisted list of domains
            is_blacklisted = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
                    for blacklisted_domain in blacklisted_domains:
                        if blacklisted_domain in link.url:
                            is_blacklisted = True

            # If it is allowed, create a new item and add it to the list of found items
            if is_allowed and not is_blacklisted:
                if link.url not in urls:
                    urls.append(link.url)
        return urls

    def write_to_file(self, file_path, urls):
        with open(file_path, 'r', encoding='UTF8') as f_obj:
            lines = [line.replace('\n', '').replace('https://','').replace('http://','').replace('www.','') for line in f_obj]
            for url in urls:
                if url.replace('https://','').replace('http://','').replace('www.','') not in lines:
                    with open(file_path, 'a', encoding='UTF8') as fp:
                        fp.write(url)
                        fp.write('\n')