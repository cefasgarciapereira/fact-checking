import scrapy
import pandas as pd
import re, datetime
import datefinder
from ..items import PoynterNewsItem
import re
#Esta spider e responsavel por coletar as informacoes das noticias na pagina
#inical da lupa

#Command to run: scrapy crawl poynter -o poynter_output.csv/.json

class PoynterSpider(scrapy.Spider):
    name = "poynter"
    item_id = 0

    def start_requests(self):
        df = pd.read_csv("poynter_links_false.csv")
        urls = df['link']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = PoynterNewsItem()

        all_div_posts = response.css('.post-container')

        for div in all_div_posts:
            PoynterSpider.item_id += 1
            title = response.css('.entry-title::text').extract()[1] 
            title = re.sub('\t','',str(title))
            title = re.sub('\n','',str(title))
            title = re.sub(r'[^\w\s]','',title)
            title = title.lower()
            title = title.replace(',',' ')

            source = response.css('.entry-content__text--org::text').extract()[0] 
            source = re.sub('Fact-checked by:','',str(source))

            date = response.css('strong::text').extract()[0]
            
            # get list of countries
            date_and_country = date.split('|')
            countries = date_and_country[1].split(',')
            countries = [c.replace(' ','') for c in countries]
            title = re.sub(r'[^\w\s]','',title)
            countries = '- '.join(countries)

            print(countries)
            match = list(datefinder.find_dates(str(date)))
            
            loc = re.sub('[^a-zA-Z]+',' ',str(date))
            date = match[0]
            
            poynter_link = response.request.url
            
            label = response.css('.entry-title--red::text').extract()[0] 
            label = re.sub(':','',str(label))

            justify = response.css('.entry-content__text--explanation::text').extract()[0].lower()  
            justify = justify.replace(',', ' ')
            justify = re.sub(r'[^\w\s]','',justify)


            checked_link = response.css('a.button.entry-content__button.entry-content__button--smaller').attrib['href']

            items['id'] = PoynterSpider.item_id
            items['title'] = title
            items['date'] = date
            items['countries'] = countries
            items['source'] = source
            items['poynter_link'] = poynter_link
            items['label'] = label
            items['justify'] = justify
            items['checked_link'] = checked_link
            yield items