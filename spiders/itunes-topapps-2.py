import scrapy
from scrapy.item import Item, Field

class ItunesItem(Item):
    app_name = Field()
    category = Field()
    appstore_link_url = Field()
    img_src_url = Field()
    star_rating = Field()
    number_of_ratings = Field()

class ItunesSpider(scrapy.Spider):
    name = "applev2"
    handle_httpstatus_list = [404, 403]
    allowed_domains = ["apple.com"]
    start_urls = ["https://www.apple.com/itunes/charts/free-apps/"]
    custom_settings = {'DOWNLOAD_DELAY': 0.5}
     
    def parse(self, response):
        apps = response.xpath("//*[@class='section-content']//ul/li")
        for app in apps:
            item = ItunesItem()
            item['app_name'] = app.xpath('.//h3/a/text()').extract()
            item['category'] = app.xpath('.//h4/a/text()').extract()
            appstore_link_url = app.xpath('.//h3/a/@href').extract()
            details_url = ''.join(appstore_link_url) 
            item['appstore_link_url'] = appstore_link_url
            item['img_src_url'] = 'https://www.apple.com' + ''.join(app.xpath('.//a/img/@src').extract())
            request = scrapy.Request(details_url, callback=self.parse_details)
            request.meta['item'] = item
            yield request
            
    def parse_details(self, response):
        item = response.meta['item'] 
        rating_string = response.xpath('//figcaption/text()').extract()
        rating_parts = ''.join(rating_string).split(',')
        item['star_rating'] = rating_parts[0]
        item['number_of_ratings'] = rating_parts[1]
        yield item        