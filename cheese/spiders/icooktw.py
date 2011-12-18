from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from base import RecipeBaseSpider
from cheese.utils import stringify_children, get_text_or_none

class IcooktwSpider(RecipeBaseSpider):
    name = 'icooktw'
    #start_urls = ['http://www.ytower.com.tw/recipe/iframe-search.asp']
    #start_urls = [
            #'http://icook.tw/recipes/15075', 'http://icook.tw/recipes/15116',
            #'http://icook.tw/recipes/15124', 'http://icook.tw/recipes/15074',
            #'http://icook.tw/recipes/14827'
            #]
    start_urls = ['http://icook.tw/recipes/latest']

    rules = (
            Rule(SgmlLinkExtractor(allow=r'recipes/latest?'), callback='parse_list', follow=True),
            Rule(SgmlLinkExtractor(allow=r'recipes/\d+$'), callback='parse_detail', follow=True),
    )

    def parse_list(self, response):
       pass

    @property
    def title(self):
        return self.get_first_text('//h2[@itemprop="name"]/a/text()')

    @property
    def image_domain(self):
        return  None

    @property
    def main_picture(self):
        return self.get_first_text('//img[@class="main-pic"]/@src')

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
            order = lele.find('.//big').text
            instruction = lele.find('.//p/span[@class="step-img"]')
            if instruction is not None:
                step =  stringify_children(lele.find('.//p')).strip()
                step_picture = instruction.find('a').attrib['href']
            else:
                #text only instruction
                text_only_instruction = lele.find('.//p')
                if text_only_instruction is not None:
                    step = stringify_children(text_only_instruction).strip()
                step_picture = None
            steps.append(dict(order=order, instruction=step, picture=step_picture))
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
        return self.get_first_text('//span[@itemprop="author"]/text()')

    @property
    def view_count(self):
        return self.get_first_text('//span[@class="view-count"]/text()')

    @property
    def fav_count(self):
        return self.get_first_text('//span[@class="fav-count"]/text()')

    @property
    def comments(self):
        return None

    @property
    def misc_text(self):
        return None



