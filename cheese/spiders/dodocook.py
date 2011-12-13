from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from base import RecipeBaseSpider
from cheese.utils import stringify_children, get_text_or_none, unicode_pprint

class DodocookSpider(RecipeBaseSpider):
    name = 'dodocook'
    start_urls = [
            'http://dodocook.com/recipe/854',
            ]

    def parse_list(self, response):
       pass

    def parse(self, response):
        self._on_receive_html(response)
        print self.title
        print self.main_picture
        unicode_pprint.pprint(self.ingredients)

    @property
    def title(self):
        return self.get_first_text('//span[@id="LabelRecipeName"]/text()')

    @property
    def main_picture(self):
        return self.get_first_text('//img[@id="ImageRecipe"]/@src')

    @property
    def ingredients(self):
        ingdivs = self.hxs.select('//div[@class="Material"]')
        ingredients = []
        for idiv in ingdivs:
            ele = idiv.root
            ings = []
            section_name = ele.find('.//div[@class="Title"]').text
            itemeles = ele.findall('.//div[@class="Item"]')
            for iele in itemeles:
                ing = iele.find('.//span[@class="Name"]')
                ing_name = get_text_or_none(ing)
                amount = iele.find('.//span[@class="Quantity"]')
                ing_amout = get_text_or_none(amount)
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


