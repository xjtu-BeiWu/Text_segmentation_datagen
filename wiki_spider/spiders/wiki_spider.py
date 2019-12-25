# -*- coding:utf-8 -*-
import scrapy
import csv
import bs4
from bs4 import BeautifulSoup
from wiki_spider.items import WikiSpiderItem


class WikiSpider(scrapy.Spider):
    name = 'wiki_spider'
    allowed_domains = ['en.wikipedia.org']

    def __init__(self):
        super(WikiSpider, self).__init__()
        # url
        self.base_url = 'http://en.wikipedia.org'
        # 所有课程名
        self.class_names = ['Solid Mechanics', 'Crystallography']
        # 当前的课程
        self.class_index = 0
        # 当前的主题列表
        self.topic_list = self.get_data_csv(self.class_names[self.class_index])
        # 当前的主题
        self.topic_index = 0

    def start_requests(self):
        # 发起请求
        url = self.base_url + '/wiki/' + self.topic_list[self.topic_index]
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        # html页面
        html = soup.prettify(encoding='utf-8')

        # 分面和文本
        # 搜索所有的一级分面
        facets = {}
        texts_body = soup.find('div', id='mw-content-text')
        contents = texts_body.find('div', id='toc')

        if contents is not None:
            # 所有一级分面标签
            lis = contents.find_all('li', class_='toclevel-1')
            for li in lis:
                # 分面名
                facet = li.find('span', class_='toctext').text
                facet_id = li.find('a')['href'][1:]
                print(facet_id)
                # 获取文本
                facet_node = texts_body.find('span', id=facet_id).parent
                text = ''
                # 从title结点往后遍历 直到h2截止
                facet_node = facet_node.next_sibling
                while facet_node is not None and facet_node.name != 'h2':
                    if type(facet_node) is not bs4.element.NavigableString and type(
                            facet_node) is not bs4.element.Comment:
                        if facet_node.name not in ['div', 'table'] and facet_node.text.strip() != '':
                            text += (facet_node.text.strip() + '\n')
                    facet_node = facet_node.next_sibling
                facets[facet] = text

        # 保存
        items = WikiSpiderItem()
        items['class_name'] = self.class_names[self.class_index]
        items['topic_name'] = self.topic_list[self.topic_index]
        items['html'] = html
        items['facets'] = facets
        yield items

        # 下一个请求
        self.topic_index += 1
        if self.topic_index < len(self.topic_list):
            yield scrapy.Request(url=self.base_url + '/wiki/' + self.topic_list[self.topic_index], callback=self.parse)
        else:
            self.class_index += 1
            if self.class_index < len(self.class_names):
                self.topic_index = 0
                self.topic_list = self.get_data_csv(self.class_names[self.class_index])
                yield scrapy.Request(url=self.base_url + '/wiki/' + self.topic_list[self.topic_index],
                                     callback=self.parse)

    def get_data_csv(self, class_name):
        with open('../data/' + class_name + '.csv') as f:
            f_csv = csv.reader(f)
            return [r[0].replace(' ', '_') for r in f_csv]
