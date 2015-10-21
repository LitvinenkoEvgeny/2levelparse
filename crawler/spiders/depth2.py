# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class DepthCrawl(CrawlSpider):
    name = 'depth'

    def initial_data(self, urls):
        '''helper function for set domains and urls from file data'''
        for url in urls:
            if url.startswith('www'):
                self.allowed_domains.append(url)
                self.start_urls.append('http://{}'.format(url))
            else:
                self.allowed_domains.append('www.{}'.format(url))
                self.start_urls.append('http://www.{}'.format(url))

    def __init__(self, sites=False, *args, **kwargs):
        with open(sites, 'r') as f:
            self.allowed_domains = []
            self.start_urls = []

            # delete \n symbol
            self.urls = [url.strip() for url in f.readlines()]

            # prepare initial data
            self.initial_data(self.urls)

        super(DepthCrawl, self).__init__(*args, **kwargs)

    rules = (
        Rule(LinkExtractor(allow=('$')), callback='parse_obj', follow=True),
    )

    def parse_obj(self, response):
        if len(response.url.split("/")) < 5:
            print(response.url)
