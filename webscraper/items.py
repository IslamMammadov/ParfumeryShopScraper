# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ParfumeItem(Item):
    parfume = Field()
    price = Field()
    volume = Field()
    category = Field()
    url = Field()




