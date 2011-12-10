
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

def stringify_children(node):
    #http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

class CookShowSpider(CrawlSpider):
    name = 'cookshow'
    #start_urls = ['http://www.ytower.com.tw/recipe/iframe-search.asp']
    start_urls = [
            'http://www.cookshow.com.tw/foodlist-in3.php?P_Id=183'
            ]

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
        title = hxs.select('//td[@class="text10-white-15-b"]/text()').extract()[0]
        print "title=>%s" % title

        _main_pic = hxs.select('//img[@class="pp-cooklist-in3"]/@src').extract()
        if _main_pic:
            main_pic = _main_pic[0]
            print "main-pic=>%s" % main_pic

        ingdivs = hxs.select('//table[@width="333"]/tr')
        for idiv in ingdivs:
            ele = idiv.root
            ### ingredients
            ing = ele.find('.//td[@width="306"]')
            if ing is not None:
                print ing.text
            amount = ele.find('.//td[@width="105"]')
            if amount is not None:
                print amount.text

            ### sauce
            ing = ele.find('.//td[@width="231"]')
            if ing is not None:
                print ing.text
            amount = ele.find('.//td[@width="102"]')
            if amount is not None:
                print amount.text

        steptrs = hxs.select('//table[@class="box-cooklist-step"]/tr')
        print len(steptrs)

        for tr in steptrs:
            _tr = tr.root
            step_img = _tr.find('.//img[@class="pp-cooktop3"]')
            if step_img is not None:
                print step_img.attrib['src']
            step_text = _tr.find('.//td[@class="text08-12-bw"]')
            if step_text is not None:
                print step_text.text




