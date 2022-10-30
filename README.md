# AutoScraper
Currently hold 2 version of this project:

 ### <u>Streamlit version</u>
  Services are:
   - Raw Scraping: similarities based
   - API downloading
   - Maya website reports downloder
   - Queries based: using Scrapy
 
 ### <u>FastAPI version</u>
  Services are:
   - Raw Scraping: similarities based (POST)
   - API downloading (GET / POST)
   - Maya website reports downloder (GET / POST)
   - Queries based: using Scrapy (POST)
   - PDF pasing: return full PDF as string / All the text alone / All the tables alone (POST)
   - Scrape predefined specific content from the [https://apis.cbs.gov.il](https://apis.cbs.gov.il) website (GET)
 
 Managment Services:
   - Sending an email (POST)
   - Inserting entities to specific tables in Azure datalake (POST)
   - Handeling azure entities and based on them create / disable / delete DAGs from the airflow system (GET)
