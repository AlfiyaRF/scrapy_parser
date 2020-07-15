import json
import scrapy
from googlesearch import search

looking_for = "лучшие фильмы"

urls = []
for i in search(looking_for,
                tld = 'com',
                lang = 'en',
                num = 3,
                start = 0,
                stop = 3,
                pause = 2.0,
               ):
    urls.append(i)

class FilmsSpider(scrapy.Spider):
    name = "films"
    def start_requests(self):
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        response_url = response.url
        response_title = response.css('title::text').extract_first(default='not-found')
        imgs = []
        for img in response.css('img').getall():
            imgs.append({
                'img_src': response.css('img').xpath('@src').get(),
                'img_alt': response.css('img').xpath('@alt').get(),
            })
        return {
            'url': response_url,
            'title': response_title,
            'imgs': imgs,
        }