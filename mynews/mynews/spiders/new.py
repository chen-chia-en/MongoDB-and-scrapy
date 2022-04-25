from http.client import responses
import scrapy
from mynews.items import MynewsItem

class NewSpider(scrapy.Spider):
    name = 'new'
    allowed_domains = ['www.chinatimes.com']
    start_urls = ['https://www.chinatimes.com/politic/total/?chdtv']

    def parse(self, response):
        target = response.css("section > ul > li > div > div > div.col")
        for t in target:     
            data = MynewsItem()   
            data["href"] = t.css("h3.title a::attr(href)").get()
            data["title"] = t.css("h3.title a::text").get()
            data["date"] = t.css("div > time > span.date::text").get()
            data["content"] = t.css("p.intro::text").get()
            yield data
        
        next_pages = response.css("section > nav > ul > li > a::attr(href)").getall()
        for i, page in  enumerate(next_pages):
            yield response.follow(page, callback = self.parse)


