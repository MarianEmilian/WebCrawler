import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        'https://www.forbes.com/?sh=14cb6dd22254',
    ]

    def parse(self, response):
        for post in response.css('div.oxy-post'):
            yield{
                'title': post.css('.oxy-post-wrap a::text')[0].get()
            }