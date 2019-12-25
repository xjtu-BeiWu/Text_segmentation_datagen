# -*- coding: utf-8 -*-
import os


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WikiSpiderPipeline(object):
    def process_item(self, item, spider):
        class_name = item['class_name']
        topic_name = item['topic_name']
        html = item['html']
        facets = item['facets']

        # 保存html
        if not os.path.exists('../output/html/' + class_name + '/'):
            os.mkdir('../output/html/' + class_name + '/')
        with open('../output/html/' + class_name + '/' + topic_name + '.html', 'w', encoding='utf-8') as f_html:
            f_html.write(str(html, encoding='utf-8'))

        # 保存分面
        if not os.path.exists('../output/text/' + class_name + '/'):
            os.mkdir('../output/text/' + class_name + '/')
        os.mkdir('../output/text/' + class_name + '/' + topic_name + '/')
        for facet in facets:
            with open('../output/text/' + class_name + '/' + topic_name + '/' + facet + '.txt', 'w', encoding='utf-8') as f_facet:
                f_facet.write(facets[facet])
        return True
