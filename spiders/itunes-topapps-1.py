import scrapy

class ItunesSpider(scrapy.Spider):
    name = "applev2"
    handle_httpstatus_list = [404, 403]
    allowed_domains = ["apple.com"]
    start_urls = ["https://www.apple.com/itunes/charts/free-apps/"]
    custom_settings = {'DOWNLOAD_DELAY': 0.5}
     
    def parse(self, response):
        apps = response.xpath("//*[@class='section-content']//ul/li")
        for app in apps:
            yield {
                'app_name': app.xpath('.//h3/a/text()').extract(),
                'category': app.xpath('.//h4/a/text()').extract(),
                'appstore_link_url': app.xpath('.//h3/a/@href').extract(),
                'img_src_url': app.xpath('.//a/img/@src').extract()
            }