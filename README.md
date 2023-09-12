# Scrapy LinkedIn Job Scraper

![GitHub last commit](https://img.shields.io/github/last-commit/grpollak/linkedin-job-scraper)
![GitHub license](https://img.shields.io/github/license/grpollak/linkedin-job-scraper)

Scrapy LinkedIn Job Scraper is a powerful tool for scraping LinkedIn job listings and their details.  
It allows you to easily configure your scraping parameters and store the data in a MongoDB database.  
This project also leverages `Scrapeops` as a proxy server and uses Hydra for managing configuration.

## Getting Started

These instructions will help you set up and run the scraper on your local machine.

### Prerequisites

- Python 3.x
- Poetry (for managing dependencies)
- MongoDB (for storing scraped data)
- Scrapeops API Key
- LinkedIn account

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Install project dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Create a `.env` file in the `linkedin/` directory with the following variables:

   ```env
   SCRAPEOPS_API_KEY="Your Scrapeops API Key"
   MONGODB_URI="Your MongoDB URI"
   MONGO_DATABASE="Your Database Name"
   MONGODB_COLLECTION="Your Collection Name"
   ```

4. Configure your scraping parameters either by editing `conf/config.yaml` or using the Scrapy command line with `-a` flags.

## Usage

You can run the scraper using either Poetry or Python directly.

### Using Poetry:

```bash
poetry run scrapy crawl linkedin-job
```

### Using Python:

```bash
python main.py
```

### Scraping Parameters

You can customize your scraping parameters in `conf/config.yaml` like this:

```yaml
search_terms: "Python OR C++"
location: "United States"
period:
  days: 30
experience_levels:
  - "Internship"
  - "Entry level"
  - "Associate"
  - "Mid-Senior level"
```

Alternatively, you can pass parameters via the Scrapy command line using `-a` flags:

```bash
poetry run scrapy crawl linkedin-job -a search_terms="Python OR C++"
```

## Built With

- [Scrapy](https://scrapy.org/) - A fast and powerful web crawling and web scraping framework.
- [MongoDB](https://www.mongodb.com/) - A NoSQL database used for storing scraped data.
- [Scrapeops](https://www.scrapeops.io/) - A proxy server service for web scraping.
- [Hydra](https://hydra.cc/) - A configuration management tool.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  
**Sidenote**: Scrapy LinkedIn Job Scraper is a personal project, not intended for any commercial use

## Acknowledgments

- Thanks to the following excellent tutorials

