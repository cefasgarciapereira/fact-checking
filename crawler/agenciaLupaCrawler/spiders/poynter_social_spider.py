import scrapy
import pandas as pd
import re, datetime
import datefinder
import re
import time
from ..items import PoynterSocialItem
import utils
import sys
#Esta spider e responsavel por coletar todos os links das noticias originais na pagina
#e verificar se são referentes ao twitter ou facebook
#Command to run: scrapy crawl poynter_social -o poynter_social.csv

class PoynterSocialSpider(scrapy.Spider):
    name = "poynter_social"
    item_id = 0
    counter = 0

    def start_requests(self):
        #df = pd.read_csv("poynter_all.csv")
        #urls = df['checked_link']

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

        #for url in urls:
            #if(not isNaN(url)):
                #yield scrapy.Request(url=formaturl(url), callback=self.parse)   

    def parse(self, response):
        #attributes
        items = PoynterSocialItem()
        facebook_links = []
        facebook_ids = []
        twitter_links = []
        twitter_ids = []
        archive = []
        perma = []
        PoynterSocialSpider.item_id += 1
        df = response.meta.get('row')

        #methods
        def is_twitter_id_valid(twitter_id):
            valid = True
            
            for id_filter in utils.twitter_id_filter:
                if(twitter_id == id_filter):
                    valid = False
            
            if(not re.search("^[0-9]*$", twitter_id)):
                valid = False
            
            return valid
        
        def parse_twitterId(url):
            return url.split('/')[-1].split('?')[0]
        
        def is_facebook_url_valid(facebook_url):
            valid = True

            for url_filter in utils.facebook_url_filter:
                if(facebook_url == url_filter):
                    valid = False

            return valid
        
        def handle_social_medias():
            # 0 - none
            # 1 - only twitter
            # 2 - only facebook
            # 3 - twitter and facebook
            response = 0

            if(len(twitter_ids) > 0 and len(facebook_ids) > 0):
                response = 3
            elif(len(facebook_ids) > 0):
                response = 2
            elif(len(twitter_ids) > 0):
                response = 1
                
            return response
        
        def get_param_from_url(url, param_name):
            return [i.split("=")[-1] for i in url.split("?", 1)[-1].split("&") if i.startswith(param_name + "=")][0]
        
        def extract_facebook_id(url):
            fb_id = ''
            
            try:
                fb_id = get_param_from_url(url, 'id')
            except:
                try:
                    fb_id = get_param_from_url(url, 'fbid')
                except:
                    fb_id = ''
            
            return fb_id
        
        #main
        for href in response.css('a::attr(href)').getall():
            #captura todos os links e verifica se são do facebook ou twitter
            if(re.search(utils.facebookRegex, href)):
                if(is_facebook_url_valid(href)):
                    facebook_links.append(href)
                    fb_id = extract_facebook_id(href.replace('/posts/','/posts/?id='))
                    
                    if(fb_id != ''):
                        facebook_ids.append('_'+str(fb_id))
            
            if(re.search(utils.twitterRegex, href)):
                twitter_links.append(href)
                twitter_id = parse_twitterId(href)
                if(is_twitter_id_valid(twitter_id)):
                    twitter_ids.append('_'+str(twitter_id))
            
            if(href.find('archive.') != -1):
                archive.append(href)
            
            if(href.find('perma.') != -1):
                perma.append(href)
                #social words
        
        # search by body text
        whole_content =  ''.join(response.xpath('//body//text()').extract())
        words = []

        if(whole_content.find('facebook') != -1):
            words.append('facebook')
        
        if(whole_content.find('twitter') != -1):
            words.append('twitter')
        
        if(whole_content.find('https://twitter.com/') != -1):
            try:
                index = whole_content.find("https://twitter.com/")
                href = whole_content[index:]
                href = href.split(' ')[0]
                twitter_links.append(href)
                if(is_twitter_id_valid(twitter_id)):
                    twitter_ids.append('_'+str(twitter_id))
                    print('TWITTER ID KALUNGB: '+twitter_id)
            except:
                pass
        
        if(whole_content.find('https://facebook.com/') != -1):
            try:
                index = whole_content.find("https://facebook.com/")
                href = whole_content[index:]
                href = href.split(' ')[0]
                facebook_links.append(href)
                fb_id = extract_facebook_id(href.replace('/posts/','/posts/?id='))

                if(fb_id != ''):
                    facebook_ids.append(fb_id)
                    print('FACEBOOK ID KALUNGA: '+fb_id)
            except:
                pass

        items['id'] = df['id']
        items['checked_link'] = response.request.url
        items['countries'] = df['countries']
        items['date'] = str(df['date']).replace(' 00:00:00','')
        items['justify'] = df['justify']
        items['label'] = df['label']
        items['source'] = df['source']
        items['title'] = df['title']
        items['poynter_link'] = df['poynter_link']
        items['facebook_links'] = facebook_links
        items['facebook_ids'] = facebook_ids
        items['twitter_links'] = twitter_links
        items['twitter_ids'] = twitter_ids
        items['social_medias'] = handle_social_medias()
        items['archive_links'] = archive
        yield items