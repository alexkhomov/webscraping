from scrapy import Spider, Request
from Netflix_Deletions.items import Netflix_DeletionsItem
import re





class Netflix_Deletions(Spider):
    name = 'netflix_deletions_spider'
    allowed_domains = ['www.whats-on-netflix.com']
    start_urls = ['https://www.whats-on-netflix.com/leaving-soon']


    def parse(self, response):

        possible_urls = []

        for i in range(2015,2020):
            for j in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
                possible_urls.append('https://www.whats-on-netflix.com/leaving-soon/titles-leaving-netflix-in-' + j + '-' + str(i))
                possible_urls.append('https://www.whats-on-netflix.com/leaving-soon/netflix-titles-expiring-in-' + j + '-' + str(i))
                possible_urls.append('https://www.whats-on-netflix.com/leaving-soon/titles-leaving-netflix-' + j + '-' + str(i))
                possible_urls.append('https://www.whats-on-netflix.com/leaving-soon/whats-leaving-netflix-usa-in-' + j + '-' + str(i))
                possible_urls.append('https://www.whats-on-netflix.com/leaving-soon/titles-expiring-on-netflix-in-' + j + '-' + str(i))
                possible_urls.append('https://www.whats-on-netflix.com/leaving-soon/complete-list-of-titles-expiring-from-netflix-us-in-' + j + '-' + str(i))
                possible_urls.append('https://www.whats-on-netflix.com/leaving-soon/netflix-titles-expiring-on-netflix-in-' + j + '-' + str(i))
                possible_urls.append('https://www.whats-on-netflix.com/leaving-soon/netflix-titles-expiring-in-' + j + '-' + str(i))


        for url in possible_urls:
                yield Request(url=url, callback=self.parse_result_page)



    def parse_result_page(self, response):

         lines = response.xpath('//*[@id="page"]//div//ul/li/text()') + response.xpath('//table//tbody//td/b/text()')


         for line in lines:
             title = line.extract().strip()



             month = re.findall('(January|February|March|April|May|June|July|August|September|October|November|December)', response.xpath('//h1/text()').extract()[0])[0]
             year = re.findall('\d+',response.xpath('//h1/text()').extract()[0])[0]



             if title.lower().find('season') != -1 or title.lower().find('series') != -1:
                content_type = 'TV Show'
             else:
                content_type = 'Movie'

             item = Netflix_DeletionsItem()
             item['year'] = year
             item['month'] = month
             item['title'] = title
             item['content_type'] = content_type




             yield item




