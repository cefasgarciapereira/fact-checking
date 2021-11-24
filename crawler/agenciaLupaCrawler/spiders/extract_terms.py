import scrapy
import pandas as pd
import re, datetime
import datefinder
from ..items import ExtractTermsItem
import re
#Esta spider e responsavel por procurar palavras específicas em uma página

#Command to run: scrapy crawl extract_terms -o file_name.csv

class ExtractTermsSpider(scrapy.Spider):
    name = "extract_terms"
    item_id = 0

    def start_requests(self):        
        df = pd.read_csv('poynter_social_all.csv')
        urls = df[df['social_medias'] == 0]['checked_link']

        print(str(len(urls))+' links')

        def isNaN(string):
            return string != string

        def formaturl(url):
            if not re.match('(?:http|ftp|https)://', url):
                return 'http://www.{}'.format(url)
            
            return url

        for url in urls:
            if(not isNaN(url)):
                yield scrapy.Request(url=formaturl(url), callback=self.parse)   

    def parse(self, response):
        items = ExtractTermsItem()
        
        #social words
        whole_content =  ''.join(response.xpath('//body//text()').extract())
        words = []
        
        if(whole_content.find('facebook') != -1):
            words.append('facebook')
        
        if(whole_content.find('twitter') != -1):
            words.append('twitter')

        if(whole_content.find('tweet') != -1):
            words.append('tweet')

        if(whole_content.find('social media') != -1):
            words.append('social media')

        if(whole_content.find('hashtag') != -1):
            words.append('hashtag')

        if(whole_content.find('compartilhado') != -1):
            words.append('compartilhado')

        if(whole_content.find('postado') != -1):
            words.append('postado')
        

        items['id'] = ExtractTermsSpider.item_id
        items['link'] = response.request.url
        items['has_words'] = words
        yield items