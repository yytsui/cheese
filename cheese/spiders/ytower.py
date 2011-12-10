from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

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

        title = hxs.select('//span[@class="mv15pt80bk01"]/text()').extract()[0].strip()
        print "title=>%s" % title

        trs = hxs.select('//td[@width="200"]/table/tr')
        for tr in trs:
            ele = tr.root # lxml element
            section =  ele.find('.//td[@colspan="2"]/font')
            ing = ele.find('.//td[@width="68%"]/a[@class="sh13pt_link"]')
            amount = ele.find('.//td[@width="32%"]')
            if section is not None:
                print section.text
            if ing is not None:
                print ing.text
            if amount is not None:
                print amount.text

        img = hxs.select('//td[@height="25"]/img[@width="210"]/@src').extract()
        steps = hxs.select('//span[@class="sh13pt"]/text()').extract() #step
        print img[0]
        for s in steps:
            print s
        print "url=>%s" % url

