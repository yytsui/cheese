
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from base import RecipeBaseSpider
from cheese.utils import stringify_children, get_text_or_none, unicode_pprint


class CookShowSpider(RecipeBaseSpider):
    name = 'cookshow'
    #start_urls = [ 'http://www.cookshow.com.tw/foodlist-in3.php?P_Id=183']
    start_urls = [ 'http://www.cookshow.com.tw/newrecipe.php']

    rules = (
            Rule(SgmlLinkExtractor(allow=r'newrecipe.php'), callback='parse_list', follow=True),
            Rule(SgmlLinkExtractor(allow=r'foodlist-in3.php'), callback='parse_detail', follow=True),
    )


    @property
    def title(self):
        return self.get_first_text('//td[@class="text10-white-15-b"]/text()')

    @property
    def image_domain(self):
        return  'www.cookshow.com.tw'

    @property
    def main_picture(self):
        return self.get_first_text('//img[@class="pp-cooklist-in3"]/@src')

    @property
    def ingredients(self):
        ingdivs = self.hxs.select('//table[@width="333"]/tr')
        ingredients = []
        principal_section = dict(section_name='principal', ings=[])
        sauce_section = dict(section_name='sauce', ings=[])
        for idiv in ingdivs:
            ele = idiv.root
            ### ingredients
            ing = ele.find('.//td[@width="306"]')
            ing_name = get_text_or_none(ing)
            amount = ele.find('.//td[@width="105"]')
            ing_amount = get_text_or_none(amount)
            if ing_name:
                principal_section['ings'].append(dict(name=ing_name, amount=ing_amount))

            ### sauce
            ing = ele.find('.//td[@width="231"]')
            ing_name = get_text_or_none(ing)
            amount = ele.find('.//td[@width="102"]')
            ing_amount = get_text_or_none(amount)
            if ing_name:
                sauce_section['ings'].append(dict(name=ing_name, amount=ing_amount))

        ingredients = [principal_section, sauce_section]
        return ingredients

    @property
    def steps(self):
        steptrs = self.hxs.select('//table[@class="box-cooklist-step"]/tr')
        steps = []
        step_dict = dict(instruction=None, picture=None)
        order = 0
        for tr in steptrs:
            _tr = tr.root
            step_img = _tr.find('.//img[@class="pp-cooktop3"]')
            if step_img is not None:
                step_dict['picture'] = step_img.attrib['src']
            step_text = _tr.find('.//td[@class="text08-12-bw"]')
            if step_text is not None:
                step_dict['instruction'] = step_text.text
                order += 1
                step_dict['order'] = order
                steps.append(step_dict)
                step_dict = dict(instruction=None, picture=None)

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




