from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from cheese.items import CheeseItem

class YtowerSpider(CrawlSpider):
    name = 'ytower'
    #start_urls = ['http://www.ytower.com.tw/recipe/iframe-search.asp']
    start_urls = ['http://www.ytower.com.tw/recipe/iframe-recipe.asp?seq=A01-0840']

    """
    rules = (
            Rule(SgmlLinkExtractor(allow=r'recipe-search2.asp'), callback='parse_list', follow=True),
            Rule(SgmlLinkExtractor(allow=r'iframe-recipe.asp'), callback='parse_detail', follow=True),
    )
    """

    def parse_list(self, response):
        #hxs = HtmlXPathSelector(response)
        #i = CheeseItem()
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        #return i
        pass

    #def parse_detail(self, response):
    def parse(self, response):
        url = response.url
        hxs = HtmlXPathSelector(response)
        img = hxs.select('//td[@height="25"]/img[@width="210"]/@src').extract()
        ings = hxs.select('//table/tr/td[@class="sh13pt"]/a[@class="sh13pt_link"]/text()').extract() #ingredients
        steps = hxs.select('//span[@class="sh13pt"]/text()').extract() #step
        for t in hxs.select('//table/tr/td[@colspan="2"]/font/text()').extract(): #section
            print t.strip()
        for i in ings:
            print i
        #print "uuuuuuuuuuuuuuuu %s %s %s" %(url,img,ings)
        for s in steps:
            print s
        print img

