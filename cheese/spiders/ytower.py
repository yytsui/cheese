from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from base import RecipeBaseSpider
from cheese.utils import stringify_children, get_text_or_none, unicode_pprint

class YtowerSpider(RecipeBaseSpider):
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
    """
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

    def parse(self, response):
        self._on_receive_html(response)
        unicode_pprint.pprint(self._recipe_raw_dict)
    """

    @property
    def title(self):
        return self.get_first_text('//span[@class="mv15pt80bk01"]/text()')

    @property
    def image_domain(self):
        return  'www.ytower.com.tw'


    @property
    def main_picture(self):
        return self.get_first_text('//td[@height="25"]/img[@width="210"]/@src')

    @property
    def ingredients(self):
        trs = self.hxs.select('//td[@width="200"]/table/tr')
        ingredients = []
        for tr in trs:
            ele = tr.root # lxml element
            section =  ele.find('.//td[@colspan="2"]/font')
            section_name = get_text_or_none(section)
            if section_name:
                section_dict = dict(section=section_name,ings=[])
                ingredients.append(section_dict)
            ing = ele.find('.//td[@width="68%"]/a[@class="sh13pt_link"]')
            ing_name = get_text_or_none(ing)
            amount = ele.find('.//td[@width="32%"]')
            ing_amount = get_text_or_none(amount)
            if ing_name:
                section_dict['ings'].append(dict(name=ing_name, amount=ing_amount))
        return ingredients

    @property
    def steps(self):
        instructions= self.hxs.select('//span[@class="sh13pt"]/text()').extract() #step
        steps = []
        for i, ins in enumerate(instructions):
            step = dict(order=i+1, instruction=ins, picture=None)
            steps.append(step)
        return steps

    @property
    def tags(self):
        return None

    @property
    def author(self):
        return None

    @property
    def view_count(self):
        return None

    @property
    def fav_count(self):
        return None

    @property
    def comments(self):
        return None

    @property
    def misc_text(self):
        return None



