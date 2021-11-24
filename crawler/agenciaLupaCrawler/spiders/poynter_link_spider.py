import scrapy
import pandas as pd
import re, datetime
import datefinder
from ..items import PoynterLinkItem
import re
#Esta spider e responsavel por coletar as informacoes das noticias na pagina
#inical do poynter

#Command to run: scrapy crawl poynter_links -o poynter_links.csv

class PoynterSpider(scrapy.Spider):
    name = "poynter_links"

    def start_requests(self):
        urls = []
        for page in range(0, 211):    
            url = "https://www.poynter.org/ifcn-covid-19-misinformation/page/"+str(page)+"/?covid_countries=0&covid_rating=0&covid_fact_checkers=0#038;covid_rating=0&covid_fact_checkers=0"
            urls.append(url)
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = PoynterLinkItem()
        all_div_posts = response.css('.post-container')

        for div in all_div_posts:
            link = div.css('a.entry-content__button--smaller::attr(href)').extract() 

            items['link'] = link
            yield items