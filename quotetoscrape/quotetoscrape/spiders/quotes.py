# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    # name of spider is quotes

    def start_requests(self):
        # Start request for scraping
        yield scrapy.Request(
            url="http://quotes.toscrape.com/",
            callback=self.parsed,
        )

    def parsed(self, response):
        # All quote in quotes
        quotes = response.xpath("//div/div[2]/div[1]/div")
        for quote in quotes:
            # one by one yielding values
            yield {
                'Quote': quote.xpath(".//span[1]/text()").get(),
                'By': quote.xpath(".//span[2]/small/text()").get()
            }

        print()
        print("moving to next page")
        print()

        # check for next page xpath
        nextpage = response.xpath("//div/div[2]/div[1]/nav/ul/li[@class='next']/a/@href").get()

        # if next page xpath exists then parse for next page
        # if not then scraping is finsihed
        if nextpage:
            absurl = f"http://quotes.toscrape.com/{nextpage}"
            yield scrapy.Request(
                url=absurl,
                callback=self.parsed
            )
