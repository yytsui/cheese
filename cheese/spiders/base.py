from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from pprint import pprint

class NotImplementError(Exception):
    pass

class BaseSpider(CrawlSpider):
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
    def recipe(self):
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

    def parse(self, response):
        self._on_receive_html(response)
        pprint(self.recipe)

