import scrapy
from scrapy_splash import SplashRequest
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from Lesson_8.avitoparser.items import AvitoparserItem


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["avito.ru"]
    start_urls = ["https://www.avito.ru/all/drugie_zhivotnye?cd=1"]

    def start_requests(self):
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)"
            )
        for url in self.start_urls:
            yield SplashRequest(url)

    def parse(self, response: HtmlResponse, **kwargs):
        links = response.xpath("//a[@data-marker='item-title']/@href").getall()
        if links:
            for link in links:
                yield SplashRequest("https://www.avito.ru/" + link, callback=self.ad_parser)

    def ad_parser(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_xpath('ad', "//span[@class='title-info-title-text']/text()")
        loader.add_xpath('price', "//span[@itemprop='price']/@content")
        loader.add_xpath('description', "//div[@data-marker='item-view/item-description']/text()")
        loader.add_xpath('photo', "//div[@data-marker='image-frame/image-wrapper']/img/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()

        # ad = response.xpath("//span[@class='title-info-title-text']/text()").get()
        # price = response.xpath("//span[@itemprop='price']/@content").getall()
        # description = response.xpath("//div[@data-marker='item-view/item-description']/text()").get()
        # photo = response.xpath("//div[@data-marker='image-frame/image-wrapper']/img/@src").get()
        # url = response.url
        # yield AvitoparserItem(ad=ad, price=price, description=description, photo=photo, link=url)