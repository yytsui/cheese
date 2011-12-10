# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from cheese.utils import unicode_pprint

class RecipePipeline(object):
    def process_item(self, item, spider):
        unicode_pprint.pprint(item)
        return item
