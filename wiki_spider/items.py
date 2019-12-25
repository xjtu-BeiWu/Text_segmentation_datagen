# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WikiSpiderItem(scrapy.Item):
    # 课程名
    class_name = scrapy.Field()
    # 主题名
    topic_name = scrapy.Field()
    # html
    html = scrapy.Field()
    # 分面名:文本 dict
    facets = scrapy.Field()
