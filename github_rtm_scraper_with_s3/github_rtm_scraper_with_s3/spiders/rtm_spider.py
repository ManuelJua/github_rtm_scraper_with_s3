import scrapy
from github_rtm_scraper_with_s3.items import GithubRtmScraperWithS3Item
from scrapy.loader import ItemLoader

from datetime import date

class RtmSpider(scrapy.Spider):
    name="rtm"

    first_part_url='https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E475'
    index_url='&index='
    second_part_url='&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords='

    start_urls=[first_part_url+second_part_url]

    
    custom_settings={
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'prop-{}.csv'.format(date.today())
    }

    def parse(self,response): #I get the urls for the list of properties
        first_part_url='https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E475'
        index_url='&index='
        second_part_url='&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords='

        total_num_prop_xpath='//span[@class="searchHeader-resultCount"]/text()'
        total_num_prop=int(response.xpath(total_num_prop_xpath).get())

        if total_num_prop%24==0:#24 is the number of properties displayes in a single webpage
            num_webpages=int(total_num_prop//24)
        else:
            num_webpages=int(total_num_prop//24+1)

        for i in range(num_webpages):
            url=first_part_url+index_url+str(i*24)+second_part_url
            yield scrapy.Request(url=url, callback=self.parse_webpage)

    def parse_webpage(self,response): #Parse webpage to get properties urls
        partial_prop_urls=response.xpath('//a[@class="propertyCard-priceLink propertyCard-rentalPrice"]/@href').getall()
        prop_urls=['https://www.rightmove.co.uk'+partial_prop_url for partial_prop_url in partial_prop_urls]
      
        for url in prop_urls:
            yield scrapy.Request(url=url, callback=self.parse_property,cb_kwargs=dict(url=url))
        
    def parse_property(self,response,**kwargs): #parse each property url to get info

        l=ItemLoader(item=GithubRtmScraperWithS3Item(),selector=response)
    
        l.add_xpath('price','//div[@class="_1gfnqJ3Vtd1z40MlC0MzXu"]/span/text()')
        l.add_xpath('address','//h1[@class="_2uQQ3SV0eMHL1P6t5ZDo2q"]/text()')
        l.add_xpath('letting_details','//dl[@class="_2E1qBJkWUYMJYHfYJzUb_r"]/div[@class="_2RnXSVJcWbWv4IpBC1Sng6"]/*/text()')
        l.add_xpath('partial_agent_url','//a[@class="_2rTPddC0YvrcYaJHg9wfTP"]/@href')
        l.add_xpath('property_details','//div[@class="_4hBezflLdgDMdFtURKTWh"]//text()')
        l.add_xpath('other_features','//ul[@class="_1uI3IvdF5sIuBtRIvKrreQ"]//text()')
        l.add_xpath('description','//div[@class="STw8udCxUaBUMfOOZu0iL _3nPVwR0HZYQah5tkVJHFh5"]//text()')
        l.add_xpath('date',str(date.today()))
            
        yield l.load_item()
        
        