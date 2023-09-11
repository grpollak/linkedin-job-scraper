import json
from typing import List, Union

import scrapy
from scrapy.shell import inspect_response

from ..items import JobItem


class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin-jobs"
    SPACE = "%20"
    API_BASE_URL = (
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?"
    )

    def __init__(
        self, search_terms: Union[str, List[str], None] = None, *args, **kwargs
    ):
        super(LinkedJobsSpider, self).__init__(*args, **kwargs)
        self.search_terms = search_terms
        # api_url = "keywords={}&location={}&start={}"
        self.API_URL = (
            self.API_BASE_URL
            + "&keywords=((Python%20OR%20C++))"
            + "&location=United%20States"
        )

    def start_requests(self):
        url = self.API_URL + "&start=0"
        print(100 * "=")
        print(self.API_URL)
        print(100 * "=")
        yield scrapy.Request(
            url=url,
            callback=self.parse_next_job_page,
            meta={"page_job_idx": 0},
        )

    def parse_next_job_page(self, response):
        page_job_idx = response.meta["page_job_idx"]

        job_item = JobItem()
        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("******* Num Jobs Returned *******")
        print(num_jobs_returned)
        print("*****")

        for job in jobs:
            # job_item["job_title"] = job.css("h3::text").get(default="not-found").strip()
            job_item["job_detail_url"] = (
                job.css(".base-card__full-link::attr(href)")
                .get(default="not-found")
                .strip()
            )
            job_detail_url = (
                job.css(".base-card__full-link::attr(href)")
                .get(default="not-found")
                .strip()
            )
            yield scrapy.Request(
                url=job_detail_url,
                callback=self.parse_job_details,
                meta={"job_item": job_item},
            )

        if num_jobs_returned > 0:
            page_job_idx = int(page_job_idx) + num_jobs_returned
            next_url = self.API_URL + f"&start={page_job_idx}"
            print(f"{100*'='}{self.API_URL}{100*'='}")
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_next_job_page,
                meta={"page_job_idx": page_job_idx},
            )

    def parse_job_details(self, response):
        # import pudb
        # pudb.set_trace()
        data = {}
        job_item = response.meta["job_item"]
        # Process Detail Job
        json_ld_data = response.css('script[type="application/ld+json"]::text').get()
        if json_ld_data:
            # Clean up the extracted data by removing extra spaces and newline characters
            json_ld_data = json_ld_data.strip()
            # Parse the JSON-LD data
            data = json.loads(json_ld_data)

        job_item["title"] = data.pop("title", None)
        job_item["datePosted"] = data.pop("datePosted", None)
        job_item["description"] = data.pop("description", None)
        job_item["employmentType"] = data.pop("employmentType", None)
        job_item["dynamicData"] = data
        yield job_item
