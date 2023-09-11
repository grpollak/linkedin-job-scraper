import logging
import sys
from typing import Any

import hydra
from omegaconf import OmegaConf
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from linkedin.spiders.linkedin_jobs import LinkedJobsSpider


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: Any) -> None:
    print(OmegaConf.to_yaml(cfg))
    # TODO: figure out why setings logs do not work here
    logging.getLogger("scrapy").propagate = False
    ####
    cfg = OmegaConf.to_container(cfg, resolve=True)
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(LinkedJobsSpider, **cfg)
    process.start()


if __name__ == "__main__":
    main()
