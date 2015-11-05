# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from memect_spider.items import MemectSpiderItem


class MemectSpider(CrawlSpider):
    name = 'memect'
    allowed_domains = ['memect.com']
    start_urls = ['http://forum.memect.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/page/'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/blog/'), callback='parse_item', follow=False),
    )

    def parse_list(self, response):
        pass

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
            i['crwal_from'] = response.url

            for index in range(len(i['link'])):
                print i['link'][index], 'is ', 't.cn' in str(i['link'][index])
                if 't.cn' in str(i['link'][index]):
                    print i['link'][index]
                    i['link'][index] = urllib.urlopen(str(i['link'][index])).url
                    print '*************************', i['link'][index]
            yield i


