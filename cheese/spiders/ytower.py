from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from cheese.items import CheeseItem

class YtowerSpider(CrawlSpider):
    name = 'ytower'
    #allowed_domains = ['ytower.com.tw']
    start_urls = ['http://www.ytower.com.tw/recipe/iframe-search.asp']

    rules = (
            #Rule(SgmlLinkExtractor(allow=r'/recipe-search2.asp?\.+'), callback='parse_item', follow=True),
            Rule(SgmlLinkExtractor(allow=r'recipe-search2.asp'), callback='parse_list', follow=True),
            Rule(SgmlLinkExtractor(allow=r'iframe-recipe.asp'), callback='parse_detail', follow=True),
            #Rule(SgmlLinkExtractor(restrict_xpaths='/html/body/table[2]/tbody/tr/td/table'), callback='parse_item', follow=False),
            #Rule(SgmlLinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_list(self, response):
        #hxs = HtmlXPathSelector(response)
        #i = CheeseItem()
        print "l"*10, response.url
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        #return i

    def parse_detail(self, response):
        print "d"*10, response.url
