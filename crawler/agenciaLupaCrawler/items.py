# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AgencialupacrawlerItem(scrapy.Item):
    link = scrapy.Field()
    pass

class LupaNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    link = scrapy.Field()
    body = scrapy.Field()
    label = scrapy.Field()
    pass

class PoynterLinkItem(scrapy.Item):
    link = scrapy.Field()
    pass

class PoynterNewsItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    date = scrapy.Field()
    countries = scrapy.Field()
    poynter_link = scrapy.Field()
    label = scrapy.Field()
    justify = scrapy.Field()
    checked_link = scrapy.Field()
    pass

class PoynterSocialItem(scrapy.Item):
    id = scrapy.Field()
    checked_link = scrapy.Field()
    countries = scrapy.Field()
    date = scrapy.Field()
    justify = scrapy.Field()
    label = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    poynter_link = scrapy.Field()
    facebook_links = scrapy.Field()
    facebook_ids = scrapy.Field()
    twitter_links = scrapy.Field()
    twitter_ids = scrapy.Field()
    checked_link = scrapy.Field()
    social_medias = scrapy.Field()
    has_social_words = scrapy.Field()
    archive_links = scrapy.Field()
    pass

class ExtractTermsItem(scrapy.Item):
    id = scrapy.Field()
    link = scrapy.Field()
    has_words = scrapy.Field()
    pass

class PoynterImagesItem(scrapy.Item):
    id = scrapy.Field()
    checked_link = scrapy.Field()
    countries = scrapy.Field()
    date = scrapy.Field()
    justify = scrapy.Field()
    label = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    poynter_link = scrapy.Field()
    images = scrapy.Field()
    pass