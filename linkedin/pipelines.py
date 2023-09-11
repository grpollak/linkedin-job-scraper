import logging
import sys

import pymongo
from scrapy.exceptions import IgnoreRequest

from .items import JobItem

# useful for handling different item types with a single interface


class LinkedinPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline:
    def __init__(self, mongodb_uri, mongodb_db, mongodb_collection):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        self.mongodb_collection = mongodb_collection
        self.logger = logging.getLogger(__name__)
        if not self.mongodb_uri:
            sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get("MONGODB_URI"),
            mongodb_db=crawler.settings.get("MONGODB_DATABASE", "scrapy"),
            mongodb_collection=crawler.settings.get(
                "MONGODB_COLLECTION", "linkedin_jobs"
            ),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        # self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_request(self, request, spider):
        collection = self.db[self.mongodb_collection]
        if collection.find_one({"job_detail_url": request.url}):
            self.logger.info(
                f"URL {request.url} already exists in the database. Skipping..."
            )
            raise IgnoreRequest("URL already exists in the database")

    def process_item(self, job_item, spider):
        collection = self.db[self.mongodb_collection]
        data = dict(job_item)
        if not collection.find_one({"job_detail_url": data["job_detail_url"]}):
            collection.insert_one(data)
        return job_item
