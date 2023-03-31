# <u>AutoScraper - FastAPI - BOI</u>

Welcome to the code of the AutoScraper developed in the BOI.

The AutoScraper offers a few services as follows (more may be added in the future):
 
  <u>User Services:</u>
      - Download from an API call
      - Scraping raw data form a given website based on familirity example
      - Downloading reports form the Maya website as follows:
         - HTML:
            - HTML
            - JSON
            - CSV
         - PDF
      - Scraping data based on given queries
      - Scrapy - Based on queries
      - BS4 - Based on commands
      - Downloading / Giving the insides of a PDF file/s
   <u>Scheduling & Timing Services:</u>
      - There are functions in order to create and activate an airflow DAG based on critiria from the datalake located in the Azure Tables
   <u>Managing Services:</u>
      - There are function to manage requests from users as follows:
         - List all of the requests in the datalake (based on table name, there are 5 tables)
         - Create a request
         - Update a request
         - Approve a request
         - Disable request
         - Delete request
         - Reboot system - Will return all of the tables to the init phase
         - Delete all of the tables

<hr>

### <u>Company:</u> Bank of Israel
### <u>Developer:</u> Lidor E.S
