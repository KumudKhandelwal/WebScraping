import os
import scrapy

class ExtractHTML(scrapy.Spider):
    name = 'extract_html'
    path = './supporting_files/lin_scraped_URLs'
    html_path = './supporting_files/lin_scraped_HTMLs'
    
    def start_requests(self):
        if not os.path.exists(self.html_path):
            os.mkdir(self.html_path)
        
        file_list = os.listdir(self.path)
        for txt_file in file_list:
            with open(f'{self.path}/{txt_file}', 'r') as f:
                urls = f.readlines()
            
            for url in urls:
                yield scrapy.Request(url, callback=self.write_html, dont_filter=True, cb_kwargs={
                    'folder':self.html_path,
                    })

    def write_html(self, response, folder):
        path = f'{folder}'
        url = response.url
        file_name = f"{url.replace('https://','').replace('http://','').replace('/','_')}.html"
        
        with open(f'{path}/{file_name}', 'w+', encoding="utf-8") as f:
            f.write(response.text)