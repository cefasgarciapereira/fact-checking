import scrapy
import pandas as pd
import re
from ..items import PoynterImagesItem
import utils
#Esta spider e responsavel por coletar todos os links das noticias originais na pagina
#e verificar se são referentes ao twitter ou facebook
#Command to run: scrapy crawl poynter_social -o poynter_social.csv

class PoynterImagesSpider(scrapy.Spider):
    name = "poynter_images"
    item_id = 0
    counter = 0

    def start_requests(self):
        df = pd.read_csv("poynter_false.csv")

        def isNaN(string):
            return string != string

        def formaturl(url):
            if not re.match('(?:http|ftp|https)://', url):
                return 'http://www.{}'.format(url)
            
            return url

        for index, row in df.iterrows():
            if(not isNaN(str(row['checked_link']))):
                yield scrapy.Request(url=formaturl(str(row['checked_link'])), callback=self.parse, meta={'row' : row})   
 

    def parse(self, response):
        #attributes
        items = PoynterImagesItem()
        PoynterImagesSpider.item_id += 1
        df = response.meta.get('row')
        images = []
        
        url = response.url
        base_url = url.rsplit('/',1)[0]  
                
        body = response.css('body')

        images_urls = body.css('img::attr(src)').extract()

        for image_url in images_urls:
            if(".jpg" in image_url or ".png" in image_url):
                if(base_url in image_url):
                    images.append(image_url)
                else:
                    images.append(base_url+image_url)



        items['id'] = df['id']
        items['checked_link'] = response.request.url
        items['countries'] = df['countries']
        items['date'] = str(df['date']).replace(' 00:00:00','')
        items['justify'] = df['justify']
        items['label'] = df['label']
        items['source'] = df['source']
        items['title'] = df['title']
        items['poynter_link'] = df['poynter_link']
        items['images'] = images
        yield items