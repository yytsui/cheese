from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from cheese.items import CheeseItem

class YtowerSpider(CrawlSpider):
    name = 'ytower'
    start_urls = ['http://www.ytower.com.tw/recipe/iframe-search.asp']

    rules = (
            Rule(SgmlLinkExtractor(allow=r'recipe-search2.asp'), callback='parse_list', follow=True),
            Rule(SgmlLinkExtractor(allow=r'iframe-recipe.asp'), callback='parse_detail', follow=True),
    )

    def parse_list(self, response):
        #hxs = HtmlXPathSelector(response)
        #i = CheeseItem()
        print "l"*10, response.url
        print "h"*10, response.headers
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        #return i

    def parse_detail(self, response):
        print "d"*10, response.url
