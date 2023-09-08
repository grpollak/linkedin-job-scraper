from typing import List, Union

import scrapy


class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin-jobs"
    SPACE_SYMBOL = "%20"
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
            self.API_BASE_URL + "&keywords=Python" + "&location=United%20States"
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

        job_item = {
            "title": str,
            "company": str,
            "company_link": str,
            "detail_url": str,
            "date_listed": str,
            "job_title": str,
        }
        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("******* Num Jobs Returned *******")
        print(num_jobs_returned)
        print("*****")

        for job in jobs:
            job_item["job_title"] = job.css("h3::text").get(default="not-found").strip()
            job_item["job_detail_url"] = (
                job.css(".base-card__full-link::attr(href)")
                .get(default="not-found")
                .strip()
            )
            job_item["job_listed"] = (
                job.css("time::text").get(default="not-found").strip()
            )

            job_item["company_name"] = (
                job.css("h4 a::text").get(default="not-found").strip()
            )
            job_item["company_link"] = job.css("h4 a::attr(href)").get(
                default="not-found"
            )
            job_item["company_location"] = (
                job.css(".job-search-card__location::text")
                .get(default="not-found")
                .strip()
            )
            yield job_item

        if num_jobs_returned > 0:
            page_job_idx = int(page_job_idx) + num_jobs_returned
            next_url = self.API_URL + f"&start={page_job_idx}"
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_next_job_page,
                meta={"page_job_idx": page_job_idx},
            )
