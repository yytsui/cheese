from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from base import RecipeBaseSpider
from cheese.utils import stringify_children, get_text_or_none, unicode_pprint

class DodocookSpider(RecipeBaseSpider):
    name = 'dodocook'
    start_urls = ['http://dodocook.com/recipe/%d' % i for i in range(1,1200)]
    #start_urls = ['http://dodocook.com/recipe/2000']

    def parse(self, response):
        self._on_receive_html(response)
        if  not self.title:
            return None
        else:
            return self.recipe

    @property
    def title(self):
        return self.get_first_text('//span[@id="LabelRecipeName"]/text()')

    @property
    def domain(self):
        return  'dodocook.com'

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
        ps = self.hxs.select('//div[@class="ProcedureBox2"]') or\
                self.hxs.select('//span[@class="Process"]')

        steps = []
        for i, p in enumerate(ps):
            lele = p.root
            order = i + 1
            image = lele.find('.//img')
            if image is not None:
                picture = image.attrib['src']
            else:
                picture = None
            instruction_ele = lele.find('.//pre')
            instruction = get_text_or_none(instruction_ele)
            steps.append(dict(order=order, instruction=instruction, picture=picture))
        return steps


    @property
    def tags(self):
        tags = self.get_first_text('//span[@id="LabelRecipeTag"]/text()')
        if tags:
            _tags = tags.strip().split(' ')
        else:
            _tags = []
        return _tags

    @property
    def author(self):
        return self.get_first_text('//a[@id="lnkAuthor2"]/text()')

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


