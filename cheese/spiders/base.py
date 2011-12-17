from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider

from cheese.utils import get_first_text_or_none
from cheese.items import RecipeItem

class NotImplementError(Exception):
    pass

class RecipeBaseSpider(CrawlSpider):
    name = 'base spider for interface purpose only'

    def parse_list(self, response):
        pass

    def _on_receive_html(self, response):
        self.url = response.url
        self.hxs = HtmlXPathSelector(response)

    @property
    def title(self):
        raise NotImplementError

    @property
    def main_picture(self):
        raise NotImplementError

    @property
    def ingredients(self):
        raise NotImplementError

    @property
    def steps(self):
        raise NotImplementError

    @property
    def tags(self):
        raise NotImplementError

    @property
    def author(self):
        raise NotImplementError

    @property
    def view_count(self):
        raise NotImplementError

    @property
    def fav_count(self):
        raise NotImplementError

    @property
    def comments(self):
        raise NotImplementError

    @property
    def misc_text(self):
        raise NotImplementError

    @property
    def image_domain(self):
        raise NotImplementError

    def get_recipe_raw_dict(self):
        return dict(url=self.url,
                    title=self.title,
                    main_picture=self.main_picture,
                    ingredients=self.ingredients,
                    steps=self.steps,
                    tags=self.tags,
                    author=self.author,
                    view_count=self.view_count,
                    fav_count=self.fav_count,
                    comments=self.comments,
                    misc_text=self.misc_text
                )

    @property
    def _recipe_raw_dict_with_image_urls(self):
        recipe_raw_dict = self.get_recipe_raw_dict()
        image_urls = []
        main_picture = recipe_raw_dict['main_picture']
        if main_picture:
            recipe_raw_dict['main_picture'] = self.get_image_url(main_picture)
            image_urls.append(recipe_raw_dict['main_picture'])
        for s in recipe_raw_dict['steps']:
            if s['picture']:
                s['picture'] = self.get_image_url(s['picture'])
                image_urls.append(s['picture'])
        recipe_raw_dict.update(dict(image_urls=image_urls))
        return recipe_raw_dict

    def get_image_url(self, image_path):
        if image_path.startswith('http'):
            return image_path
        else:
            return 'http://%s%s' % (self.image_domain, image_path)

    @property
    def recipe(self):
        recipe = RecipeItem()
        for (k,v) in self._recipe_raw_dict_with_image_urls.items():
            recipe[k] = v
        return recipe

    def get_first_text(self, xpath):
        return get_first_text_or_none(self.hxs, xpath)


    def parse_item(self, response):
        self._on_receive_html(response)
        return self.recipe

