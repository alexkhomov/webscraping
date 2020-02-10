from scrapy import Spider, Request
from Netflix.items import NetflixItem
import re


class NetflixSpider(Spider):
    name = 'netflix_release_spider'
    allowed_domains = ['www.whats-on-netflix.com']
    start_urls = ['https://www.whats-on-netflix.com/coming-soon']


    def parse(self,response):
        possible_urls = []

        for i in range(2015,2020):
            for j in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
                # possible_urls.append('https://www.whats-on-netflix.com/coming-soon/' + j + '-' + str(i) + '-new-netflix-releases-preview/')
                possible_urls.append('https://www.whats-on-netflix.com/coming-soon/whats-new-on-netflix-' + j + '-' + str(i))
                possible_urls.append('https://www.whats-on-netflix.com/coming-soon/' + j + '-' + str(i) + '-new-netflix-releases')
                possible_urls.append('https://www.whats-on-netflix.com/coming-soon/' + j + '-' + str(i) + '-netflix-new-releases')
                possible_urls.append('https://www.whats-on-netflix.com/coming-soon/whats-coming-to-netflix-in-'+ j + '-' + str(i))
                possible_urls.append('https://www.whats-on-netflix.com/coming-soon/whats-coming-to-netflix-' + j + '-' + str(i))
                possible_urls.append('https://www.whats-on-netflix.com/coming-soon/' + j + '-' + str(i) + '-new-netflix-us-releases')
                


        for url in possible_urls:
                yield Request(url=url, callback=self.parse_result_page)


    def parse_result_page(self, response):

        # lines = response.xpath('//*[@id="page"]//div//ul/li/strong/text()') + response.xpath('//*[@id="page"]//div//ul/li/text()')

        if response.xpath('//*[@id="page"]//div//ul/li/strong/text()') == [] or len(response.xpath('//*[@id="page"]//div//ul/li/strong/text()') ) == 1:
            lines = response.xpath('//*[@id="page"]//div//ul/li/text()')
        else:
            lines = response.xpath('//*[@id="page"]//div//ul/li/strong/text()')

        for line in lines:
            title = line.extract().strip()


            month = re.findall('(January|February|March|April|May|June|July|August|September|October|November|December)', response.xpath('//h1/text()').extract()[0])[0]
            year = re.findall('\d+',response.xpath('//h1/text()').extract()[0])[0]

            if title.lower().find('season') != -1 or title.lower().find('series') != -1:
                content_type = 'TV Show'
            else:
                content_type = 'Movie'


            item = NetflixItem()
            item['year'] = year
            item['month'] = month
            item['title'] = title
            item['content_type'] = content_type


            yield item

# //*[@id="page"]/div/div/div/div[1]/div/article/div[5]/div[1]/ul[1]/li[10]

