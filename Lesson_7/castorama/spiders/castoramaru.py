import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from Lesson_7.castorama.items import CastoramaItem


class CastoramaruSpider(scrapy.Spider):
    name = "castoramaru"
    allowed_domains = ["castorama.ru"]
    start_urls = ["https://www.castorama.ru/decoration/wallpaper/"]

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        pass

        links = response.xpath("//a[contains(@class, 'product-card__name')]/@href").getall()
        if links:
            for link in links:
                yield response.follow(link, callback=self.goods_parser)


    def goods_parser(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaItem(), response=response)
        loader.add_xpath('goods', "//h1/text()")
        loader.add_xpath('price', "//span[@class='price']/span/span/text()")
        loader.add_xpath('photo', "//img[contains(@class, 'top-slide__img')]/@data-src")
        loader.add_value('url', response.url)
        yield loader.load_item()

        # goods = response.xpath("//h1/text()").get()
        # price = response.xpath("//span[@class='price']/span/span/text()").getall()
        # url = response.url
        # photo = response.xpath("//img[contains(@class, 'top-slide__img')]/@data-src").get()
        # yield CastoramaItem(goods=goods, price=price, photo=photo, url=url)