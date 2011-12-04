
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from cheese.items import CheeseItem

class IcooktwSpider(CrawlSpider):
    name = 'icooktw'
    #start_urls = ['http://www.ytower.com.tw/recipe/iframe-search.asp']
    start_urls = ['http://icook.tw/recipes/15075', 'http://icook.tw/recipes/15116']

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
        print "url=>%s" % url
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//h2[@itemprop="name"]/a/text()').extract()[0]
        print "title=>%s" % title

        _main_pic = hxs.select('//img[@class="main-pic"]/@src').extract()
        if _main_pic:
            main_pic = _main_pic[0]
            print "main-pic=>%s" % main_pic

        ingdivs = hxs.select('//ul[@itemprop="ingredient"]/li/div')
        for idiv in ingdivs:
            ele = idiv.root
            ing = ele.find('.//span[@itemprop="name"]')
            print ing.text
            amount = ele.find('.//span[@itemprop="amount"]')
            print amount.text

        lis = hxs.select('//ul[@itemprop="instructions"]/li')
        for li in lis:
            lele = li.root
            order = lele.find('.//big')
            print order.text
            instruction = lele.find('.//p/span[@class="step-img"]')
            if instruction:
                print "instruction => %s" % instruction.tail.strip()
                big_picture = instruction.find('a').attrib['href']
                print "big_picture => %s" % big_picture
                small_picture = instruction.find('.//img').attrib['src']
                print "small_picture => %s" % small_picture
            else:
                text_only_instruction = lele.find('.//p')
                print "instruction => %s" % text_only_instruction.text

