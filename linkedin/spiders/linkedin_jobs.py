import json
from datetime import datetime, timedelta
from typing import Dict, List, Union

import scrapy
from linkedin.items import JobItem
from scrapy.shell import inspect_response


class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin-jobs"
    SPACE_SYMBOL = "%20"
    COMMA_SYMBOL = "%2C"
    EXPIRENCE_LEVELS = {
        "Internship": 1,
        "Entry level": 2,
        "Associate": 3,
        "Mid-Senior level": 4,
        "Director": 5,
        "Executive": 6,
    }
    API_BASE_URL = (
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?"
    )

    def __init__(
        self,
        search_terms: str = "Python",
        expirience_levels: Union[str, List[str], None] = None,
        location: str = "United States",
        period: Union[Dict[str, int], None] = None,
        *args,
        **kwargs,
    ):
        super(LinkedJobsSpider, self).__init__(*args, **kwargs)
        self.API_URL = self.API_BASE_URL
        self.parse_search_terms(search_terms)
        self.parse_location(location)
        self.parse_period(period)
        self.parse_expirence_levels(expirience_levels)

    def check_expirence_levels_are_valid(self) -> None:
        if not all(value in self.EXPIRENCE_LEVELS for value in self.expirience_levels):
            raise ValueError("Invalid experience level(s) provided")

    def parse_expirence_levels(self, expirience_levels):
        if expirience_levels:
            if isinstance(expirience_levels, list):
                self.expirience_levels = [
                    exp for exp in expirience_levels if exp in self.EXPIRENCE_LEVELS
                ]
            elif (
                isinstance(expirience_levels, str)
                and expirience_levels in self.EXPIRENCE_LEVELS
            ):
                self.expirience_levels = [expirience_levels]
            self.check_expirence_levels_are_valid()
            self.expirience_levels = [
                str(self.EXPIRENCE_LEVELS[k]) for k in self.expirience_levels
            ]
            self.expirience_levels = self.COMMA_SYMBOL.join(self.expirience_levels)
        else:
            self.expirience_levels = None
        if self.expirience_levels:
            self.API_URL += f"&f_E={self.expirience_levels}"

    def parse_search_terms(self, search_terms):
        self.search_terms = search_terms.replace(" ", self.SPACE_SYMBOL)
        self.API_URL += f"&keywords=(({self.search_terms}))"

    def parse_location(self, location):
        self.location = location.replace(" ", self.SPACE_SYMBOL)
        self.API_URL += f"&location={self.location}"

    def create_time_delta(self, days=0, hours=0, minutes=0):
        time_interval = timedelta(days=days, hours=hours, minutes=minutes)
        return time_interval

    def parse_period(self, period):
        if period == None:
            return
        self.period = int(self.create_time_delta(**period).total_seconds())
        self.API_URL += f"&f_TPR={self.period}"

    def start_requests(self):
        url = self.API_URL + "&start=0"
        yield scrapy.Request(
            url=url,
            callback=self.parse_next_job_page,
            meta={"page_job_idx": 0},
        )

    def parse_next_job_page(self, response):
        page_job_idx = response.meta["page_job_idx"]

        jobs = response.css("li")

        num_jobs_returned = len(jobs)

        for job in jobs:
            job_detail_url = (
                job.css(".base-card__full-link::attr(href)")
                .get(default="not-found")
                .strip()
                .split("?")[0]
            )
            print(job_detail_url)
            yield scrapy.Request(
                url=job_detail_url,
                callback=self.parse_job_details,
            )

        if num_jobs_returned > 0:
            page_job_idx = int(page_job_idx) + num_jobs_returned
            next_url = self.API_URL + f"&start={page_job_idx}"
            print(f"{100*'='}\n{next_url}\n{100*'='}")
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_next_job_page,
                meta={"page_job_idx": page_job_idx},
            )

    def parse_job_details(self, response):
        job_item = JobItem()
        data = {}
        print(response.url)
        # Process Detail Job
        json_ld_data = response.css('script[type="application/ld+json"]::text').get()
        if json_ld_data:
            # Clean up the extracted data by removing extra spaces and newline characters
            json_ld_data = json_ld_data.strip()
            # Parse the JSON-LD data
            data = json.loads(json_ld_data)

        job_item["title"] = data.pop("title", None)
        job_item["dateScraped"] = datetime.now()
        job_item["datePosted"] = data.pop("datePosted", None)
        job_item["validThrough"] = data.pop("skills", None)
        job_item["job_detail_url"] = response.url
        job_item["description"] = data.pop("description", None)
        job_item["employmentType"] = data.pop("employmentType", None)
        job_item["industry"] = data.pop("industry", None)
        job_item["skills"] = data.pop("skills", None)
        job_item["hiringOrganization"] = data.pop("hiringOrganization", None)
        job_item["industry"] = data.pop("industry", None)
        job_item["jobLocation"] = data.pop("jobLocation", None)
        job_item["jobLocationType"] = data.pop("jobLocationType", None)
        job_item["applicantLocationRequirements"] = data.pop(
            "applicantLocationRequirements", None
        )
        job_item["educationRequirements"] = data.pop("educationRequirements", None)
        job_item["identifier"] = data.pop("identifier", None)

        job_item["dynamicData"] = data
        return job_item

        # # Check if response status is 429 (Too Many Requests)
        # if response.status == 429:
        #     # Log the error and retry the request after a delay
        #     self.logger.error(f'Received a 429 error. Retrying in 5 seconds.')
        #     yield scrapy.Request(response.url, callback=self.parse, dont_filter=True, meta={'retry': True},
        #                          priority=1, headers={'User-Agent': 'Your User Agent'})
        #     return
