# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    title = scrapy.Field()
    job_detail_url = scrapy.Field()
    dateScraped = scrapy.Field()
    datePosted = scrapy.Field()
    validThrough = scrapy.Field()
    description = scrapy.Field()
    employmentType = scrapy.Field()
    industry = scrapy.Field()
    skills = scrapy.Field()
    hiringOrganization = scrapy.Field()
    jobLocation = scrapy.Field()
    jobLocationType = scrapy.Field()
    applicantLocationRequirements = scrapy.Field()
    educationRequirements = scrapy.Field()
    identifier = scrapy.Field()

    dynamicData = scrapy.Field()
