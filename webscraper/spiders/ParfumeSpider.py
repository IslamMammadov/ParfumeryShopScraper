import scrapy
from webscraper.items import ParfumeItem
import logging
from scrapy.utils.log import configure_logging

class ParfumeSpider(scrapy.Spider):
    name = 'parfume'
    start_urls = ['https://parfumedeeurope.az/product-category/kisi-etirleri/',
                  'https://parfumedeeurope.az/product-category/qadin-etirleri/',
                  'https://parfumedeeurope.az/product-category/unisex-%c9%99tirl%c9%99r/',
                  ]
    custom_settings = {'FEEDS' : {'result.json' : {'format' : 'json', 'owerwrite' : True}}}

    configure_logging(install_root_handler = False)
    logging.basicConfig(
        filename = r'C:\Users\mislam\Desktop\Backend\DataEng\Scraping1\webscraper\log.txt',
        format = '%(levelname)s: %(message)s',
        level = logging.INFO
    )

    def parse(self, response):
        parfume_item = ParfumeItem() 
        for parfume in response.css('div.woocommerce-loop-product__wrapper'):
            parfume_item['parfume'] = parfume.css('h3.woocommerce-loop-product-title a::text').get()
            parfume_item['price'] = parfume.css('span.price bdi::text').get()
            parfume_item['volume'] =  parfume.css("div.variations.pa_olcu select#pa_olcu::attr(data-default_value)").get()
            parfume_item['category'] = response.css('div.page-title-container .page-title::text').get()
            parfume_item['url'] = parfume.css('h3.woocommerce-loop-product-title a::attr(href)').get()
            yield parfume_item

        next_page = response.css('nav.woocommerce-pagination .next.page-numbers::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)
            




