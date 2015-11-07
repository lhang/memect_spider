# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MemectSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source_name = scrapy.Field()
    source_link = scrapy.Field()
    time = scrapy.Field()
    intro = scrapy.Field()
    link = scrapy.Field()
    tag = scrapy.Field()
    keyword = scrapy.Field()
    crawl_from = scrapy.Field()
