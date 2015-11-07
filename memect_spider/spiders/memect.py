# -*- coding: utf-8 -*-
import urllib, pymongo

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Response

from memect_spider.items import MemectSpiderItem


class MemectSpider(CrawlSpider):
    name = 'memect'
    allowed_domains = ['memect.com']
    start_urls = ['http://forum.memect.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/page/'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/blog/'), callback='parse_item', process_links='link_filter', follow=False),
    )

    def __init__(self, category=None, *args, **kwargs):
        super(MemectSpider, self).__init__(*args, **kwargs)
        self.crwaled_link = []
        self.mongo_uri = 'localhost:27017'
        self.mongo_db = 'items'
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def closed():
        self.client.close()

    def link_filter(self, links):
        ret = []
        for link in links:
            print 'link is', link.url
            if link and self.db.MemectSpiderItem.find_one({"crawl_from": link.url}):
                print '已经爬取过，丢弃：', link.url
            elif link:
                ret.append(link)
            else:
                print '无效的链接'
        return ret

    def parse_list(self, response):
        print Response.url

    def parse_item(self, response):
        tag = response.css('a[class=fe_tag]::text').extract()
        for res in response.css('div[class=weibo]'):
            i = MemectSpiderItem()

            i['tag'] = tag
            i['source_name'] = res.css('b[class=screen_name]::text').extract()
            i['source_link'] = res.css('a[class=link_weibo_source]::attr(href)').extract()
            i['time'] = res.css('span[class=datetime]::text').extract()
            i['intro'] = res.css('div[class=text]::text').extract()
            i['link'] = res.xpath('.//div[contains(@class, "text")]/a/@href').extract()
            i['keyword'] = res.xpath('.//span[contains(@class, "keyword")]/text()').extract()
            i['crawl_from'] = response.url

            for index in range(len(i['link'])):
                print i['link'][index], 'is ', 't.cn' in str(i['link'][index])
                if 't.cn' in str(i['link'][index]):
                    i['link'][index] = urllib.urlopen(str(i['link'][index])).url
            yield i


