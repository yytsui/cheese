from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from cheese.items import CheeseItem
from base import BaseSpider

def stringify_children(node):
    #http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

def get_text_or_none(ele):
    if ele is not None:
        return ele.text
    else:
        return None

def get_first_text_or_none(hxs , xpath):
    texts = hxs.select(xpath).extract()
    if texts:
        return texts[0]
    else:
        return None


class IcooktwSpider(BaseSpider):
    name = 'icooktw'
    #start_urls = ['http://www.ytower.com.tw/recipe/iframe-search.asp']
    start_urls = [
            'http://icook.tw/recipes/15075', 'http://icook.tw/recipes/15116',
            'http://icook.tw/recipes/15124', 'http://icook.tw/recipes/15074',
            'http://icook.tw/recipes/14827'
            ]

    """
    rules = (
            Rule(SgmlLinkExtractor(allow=r'recipe-search2.asp'), callback='parse_list', follow=True),
            Rule(SgmlLinkExtractor(allow=r'iframe-recipe.asp'), callback='parse_detail', follow=True),
    )
    """

    def parse_list(self, response):
       pass

    @property
    def title(self):
        return get_first_text_or_none(self.hxs, '//h2[@itemprop="name"]/a/text()')

    @property
    def main_picture(self):
        return get_first_text_or_none(self.hxs, '//img[@class="main-pic"]/@src')

    @property
    def ingredients(self):
        ingdivs = self.hxs.select('//ul[@itemprop="ingredient"]/li/div')
        ingredients = []
        ings_1 = []
        for idiv in ingdivs:
            ele = idiv.root
            ing = ele.find('.//span[@itemprop="name"]')
            ing_name = get_text_or_none(ing)
            amount = ele.find('.//span[@itemprop="amount"]')
            ing_amout = get_text_or_none(amount)
            ings_1.append(dict(name=ing_name, amount=ing_amout))
        ingredients.append(dict(section_name='principal', ings=ings_1))

        ululs = self.hxs.select('//ul[@itemprop="ingredient"]/ul')
        if ululs is not None:
            for ul in ululs:
                _ul = ul.root
                section_name = _ul.find('.//li[@class="group-name"]').text
                ings = []
                for ele in _ul.findall('.//li/div'):
                    ing = ele.find('.//span[@itemprop="name"]')
                    ing_name = get_text_or_none(ing)
                    amount = ele.find('.//span[@itemprop="amount"]')
                    ing_amout = get_text_or_none(ing)
                    ings.append(dict(name=ing_name, amount=ing_amout))
                ingredients.append(dict(section_name=section_name, ings=ings))

        return ingredients

    @property
    def steps(self):
        lis = self.hxs.select('//ul[@itemprop="instructions"]/li')
        steps = []
        for li in lis:
            lele = li.root
            order = lele.find('.//big')
            instruction = lele.find('.//p/span[@class="step-img"]')
            if instruction is not None:
                step =  stringify_children(lele.find('.//p')).strip()
                big_picture = instruction.find('a').attrib['href']
                small_picture = instruction.find('.//img').attrib['src']
            else:
                #text only instruction
                text_only_instruction = lele.find('.//p')
                if text_only_instruction is not None:
                    step = stringify_children(text_only_instruction).strip()
                big_picture = None
                small_picture = None
        steps.append(dict(order=order, step=step, big_picture=big_picture, small_picture=small_picture))
        return steps



    @property
    def tags(self):
        tags = self.hxs.select('//div[@class="section list-of-recipes"]/ul/li/a/text()').extract()
        _tags = []
        if tags:
            for tag in tags:
                if len(tag.strip()) > 0:
                    _tags.append(tag.strip())
        return _tags

    @property
    def author(self):
        return get_first_text_or_none(self.hxs, '//span[@itemprop="author"]/text()')

    @property
    def view_count(self):
        return get_first_text_or_none(self.hxs, '//span[@class="view-count"]/text()')
 

    @property
    def fav_count(self):
        return get_first_text_or_none(self.hxs, '//span[@class="fav-count"]/text()')

    @property
    def comments(self):
        return None

    @property
    def misc_text(self):
        return None


    """
    def parse(self, response):
        url = response.url
        print "url=>%s" % url
        hxs = HtmlXPathSelector(response)
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
