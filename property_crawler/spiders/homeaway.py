# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.http import Request
from scrapy.loader.processors import MapCompose, Join
import urlparse

from scrapy.crawler import CrawlerProcess


logger = logging.getLogger("Property-Crawler")
fh = logging.FileHandler("crawler.log")

fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)


from property_crawler.items import PropertyCrawlerItem

# x = response.xpath("//h3[@class='hit-headline']/a[@class='hit-url js-hitLink']/@href")[10].extract()
class PropertyCrawlSpider(CrawlSpider):
    name = "Homeaway-Property-Crawler"
    allowed_domains = ["www.homeaway.com"]
    start_urls = (
        'https://www.homeaway.com/search/refined/keywords:United+Kingdom/Property+Type:apartment/page:14',
        # 'https://www.homeaway.com/vacation-rental/p1913068',
    )

    def parse(self, response):
        print (response.url)
        propertiesLinks = response.xpath("//a[@class='hit-url js-hitLink']/@href")
        for link in propertiesLinks.extract():
            request = Request(urlparse.urljoin("https://www.homeaway.com", link), callback=self.parse_item)
            request.meta["property_link"] = link
            print "................"
            print urlparse.urljoin("https://www.homeaway.com", link)
            yield request

    def parse_item(self, response):
        l = ItemLoader(item=PropertyCrawlerItem(), response=response)
        l.add_xpath('imageUrl', '//div[@class="visible-xs phone-headline"]/h1/text()')
        return l.load_item()

#
#
# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# })
#
# process.crawl(PropertyCrawlSpider)
#
# process.start()


