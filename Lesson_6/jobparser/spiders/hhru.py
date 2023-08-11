import scrapy
from scrapy.http import HtmlResponse
from Lesson_6.jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?text=Data+science&from=suggest_post&salary=&ored_clusters=true",
                  "https://hh.ru/search/vacancy?text=Data+scientist&salary=&ored_clusters=true"]

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parser)

    def vacancy_parser(self, response: HtmlResponse):
        vacancy = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']/span//text()").getall()
        city = response.xpath("//p[@data-qa='vacancy-view-location']/text()").get()
        url = response.url
        yield JobparserItem(vacancy=vacancy, city=city, salary=salary, link=url)
        print()