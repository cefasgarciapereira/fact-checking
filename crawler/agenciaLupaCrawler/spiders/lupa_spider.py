import scrapy
import pandas as pd
from ..items import LupaNewsItem
#Esta spider e responsavel por coletar as informacoes das noticias na pagina
#inical da lupa

#Command to run: scrapy crawl lupa -o lupa.csv

class LupaSpider(scrapy.Spider):
    name = "lupa"
    item_id = 0

    def start_requests(self):
        df = pd.read_csv("links.csv")
        urls = df['link']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        LupaSpider.item_id += 1
        items = LupaNewsItem()
        label = '' #label que identifica se a 
        #noticia e falsa, verdadeira, exagerada, etc
        #comeca com valor vazio e eh alterada se houver
        title = response.css('h2.bloco-title::text').extract()[0] 
        author = response.css('.bloco-autor a::text').extract()[0]
        date = response.css('.bloco-meta::text').extract()[0]
        date = date.replace(',','')
        date = date.replace('|','')
        date = date.replace(' ','')
        date = date.replace('\n','')
        date = date.replace('\r','')
        time = response.css('.bloco-meta span::text').extract()[0]
        link = response.request.url
        #cada noticiapode estar em formato
        #caso um falhe o proximo eh tentado
        try:
            body = str(response.css('.post-inner span::text').extract())
        except:
            try: 
                body = str(response.css('.post-inner p::text').extract())
            except:
                pass
        try:
            label = response.css('.post-inner .etiqueta::text').extract()[0]
        except:
            pass
        items['id'] = LupaSpider.item_id
        items['title'] = title
        items['author'] = author
        items['date'] = date
        items['time'] = time
        items['link'] = link
        items['body'] = body
        items['label'] = label
        yield items