import scrapy
import grequests
import aiohttp
import asyncio
import re

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


async def get_clicks(session, url):
    async with session.get(url) as resp:
        page = await resp.json()
        return page['views']


def get_company(headline, companies):
    for company in companies:
        if re.search(r'{}'.format(company), headline.lower()):
            return company


class NewsSpider(scrapy.Spider):
    name = "news"
    companies = ['tesla', 'gamestop']
    base_url = 'https://www.forbes.com/search/?q={company}'

    def start_requests(self):
        for company in self.companies:
            url = self.base_url.format(company=company)
            yield scrapy.Request(url)

    def parse(self, response):
        for article in response.css('.stream-item__title::attr(href)').getall():
            yield response.follow(article,
                                  callback=self.parse_article)

    def parse_article(self, response):
        PARAGRAPH_SELECTOR = '//*[@id="article-stream-0"]/div[2]/div[2]/div[3]/div[1]/p//text()'
        HEADLINE_SELECTOR = '//*[@id="article-stream-0"]/div[2]/div[2]/div[1]/div/h1/text()'
        DATE_SELECTOR = '//*[@id="article-stream-0"]/div[2]/div[2]/div[1]/div/div/div/time/text()'
        paragraphs = response.xpath(PARAGRAPH_SELECTOR).getall()
        headline = response.xpath(HEADLINE_SELECTOR).get()

        company = get_company(headline, self.companies)

        date = response.xpath(DATE_SELECTOR).get()
        blog_id = response.xpath("/html/head/meta[@property ='article:id']/@content")[0].extract()
        url = 'https://www.forbes.com/tamagotchi/v1/fetchLifetimeViews/?id=' + blog_id
        clicks = "to do "
        yield {
            'headline': headline,
            'company': company,
            'date': date,
            'paragraphs': paragraphs,
            'clicks': clicks,
            'blog_id': blog_id
        }


