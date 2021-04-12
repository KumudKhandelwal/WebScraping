from bs4 import BeautifulSoup
# import requests

import os
import scrapy

class ExtractHTML(scrapy.Spider):
    name = 'extract_html'
    path = './downloaded_URLs'
    def start_requests(self):
        file_list = os.listdir(self.path)
        for index, file in enumerate(file_list):
            print(f'File {index+1}: ',file)
            folder = f"{self.path}/{file.replace('.csv','')}"
            os.mkdir(folder)
            os.chmod(folder, 0o777)
            with open(f'{self.path}/{file}', 'r') as f:
                urls = f.readlines()
            # print(f'{file}:\n', urls)
            for url in urls:
                # print(url)
                yield scrapy.Request(url, callback=self.parse_html, dont_filter=True, cb_kwargs={
                    'file':file,
                    'folder':folder,
                    })

    def parse_html(self, response, file, folder):
        path = f'{folder}'
        url = response.url
        file_name = f"{url.replace('https://','').replace('/','_')}.html"
        
        with open(f'{path}/{file_name}', 'w+', encoding="utf-8") as f:
            f.write(response.text)

        # with open(f"./downloaded_HTMLs/{url.replace('https://','').replace('/','_')}.html", 'w+', encoding="utf-8") as f:
        #     f.write(response.text)
   
    # return file_list



# from pathlib import Path
# entries = Path('downloaded_URLs/')
# for entry in entries.iterdir():
#     print(entry.name)
