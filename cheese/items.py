# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class RecipeItem(Item):
    # define the fields for your item here like:
    # name = Field()
    url = Field()
    title = Field()
    main_picture = Field()
    ingredients = Field()
    steps = Field()
    tags = Field()
    author = Field()
    view_count = Field()
    fav_count = Field()
    comments = Field()
    misc_text = Field()
