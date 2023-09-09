# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    title = scrapy.Field()
    job_detail_url = scrapy.Field()
    datePosted = scrapy.Field()
    description = scrapy.Field()
    employmentType = scrapy.Field()

    dynamicData = scrapy.Field()
