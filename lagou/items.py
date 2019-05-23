# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_class = scrapy.Field()
    job_url = scrapy.Field()

    position_name = scrapy.Field()
    city = scrapy.Field()
    company_name = scrapy.Field()
    salary = scrapy.Field()
    work_years = scrapy.Field()
    company_industry = scrapy.Field()
    desc = scrapy.Field()
