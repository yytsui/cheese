
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from cheese.items import CheeseItem

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



        """
        ululs = hxs.select('//ul[@itemprop="ingredient"]/ul')
        if ululs is not None:
            for ul in ululs:
                _ul = ul.root
                section_name = _ul.find('.//li[@class="group-name"]').text
                print "section_name => %s" % section_name
                print "-"*50
                for ele in _ul.findall('.//li/div'):
                    ing = ele.find('.//span[@itemprop="name"]')
                    print ing.text
                    amount = ele.find('.//span[@itemprop="amount"]')
                    print amount.text
                print "-"*50



        lis = hxs.select('//ul[@itemprop="instructions"]/li')
        for li in lis:
            lele = li.root
            order = lele.find('.//big')
            print order.text
            instruction = lele.find('.//p/span[@class="step-img"]')
            if instruction is not None:
                print "instruction => %s" % stringify_children(lele.find('.//p')).strip()
                big_picture = instruction.find('a').attrib['href']
                print "big_picture => %s" % big_picture
                small_picture = instruction.find('.//img').attrib['src']
                print "small_picture => %s" % small_picture
            else:
                text_only_instruction = lele.find('.//p')
                print "instruction => %s" % stringify_children(text_only_instruction).strip()

        view_count = hxs.select('//span[@class="view-count"]/text()').extract()
        if view_count:
            print "view_count => %s" % view_count[0]
        fav_count = hxs.select('//span[@class="fav-count"]/text()').extract()
        if fav_count:
            print "fav_count => %s" % fav_count[0]

        tags = hxs.select('//div[@class="section list-of-recipes"]/ul/li/a/text()').extract()
        print "l"*30, len(tags)
        if tags:
            for tag in tags:
                if len(tag.strip()) > 0:
                    print "tag => %s" % tag.strip()

        author = hxs.select('//span[@itemprop="author"]/text()').extract()
        if author:
            print "author => %s" % author[0]

        #TODO: number of comments
        """
