# Books Data Pipeline

An end-to-end data engineering pipeline that scrapes book data from the web,
transforms it using dbt, stores it in DuckDB, and visualizes it with a Dash dashboard.

# Architecture
Web Scraping → Apache Airflow → dbt → DuckDB → Dash Dashboard

# Tech Stack

- Python - Web scraping & scripting
- BeautifulSoup - HTML parsing
- Apache Airflow(Astro) - Pipeline orchestration
- dbt - Data transformation
- DuckDB - Data warehouse
- Dash & Plotly - Interactive dashboard
- Docker - Containerization

# Project Structure
books-data-pipeline/
├── dags/
│   └── bookspipeline.py        # Airflow DAG
├── include/
│   └── scrape_books.py         # Scraping script
│   └── books.duckdb            # DuckDB database
├── books_project/
│   ├── models/
│   │   ├── stg_books.sql       # Staging model
│   │   └── fct_books.sql       # Warehouse model
│   └── seeds/
│       └── books.csv           # Raw scraped data
├── dashboard.py                # Dash dashboard
├── requirements.txt
└── Dockerfile

# Pipeline Steps

1. Web Scraping — scrapes 1,000 books from [books.toscrape.com](https://books.toscrape.com) extracting title, price, and rating

2. Airflow DAG — orchestrates the pipeline daily in this order:
   - `scrape_books` → `dbt_seed` → `dbt_run`

3. dbt Transformation — cleans and transforms raw data:
   - `stg_books` — staging layer, converts rating to number
   - `fct_books` — warehouse layer, cleans price column

4. DuckDB — stores the final transformed data

5. Dash Dashboard — interactive visualization with filters and charts

# How to Run

# Prerequisites
- Docker Desktop
- Astro CLI
- Python 3.10+

### 1. Clone the repo
```bash
git clone https://github.com/Omasuuuu16/books-data-pipeline.git
cd books-data-pipeline
```

### 2. Start Airflow
```bash
astro dev start
```
Open [http://localhost:8080](http://localhost:8080) and trigger the `books_pipeline` DAG.

### 3. Run dbt locally
```bash
cd books_project
dbt seed
dbt run
```

### 4. Launch the dashboard
```bash
cd ..
python dashboard.py
```
Open [http://localhost:8050](http://localhost:8050)


# Dashboard Features

- Filter books by rating
- Bar chart showing number of books per rating
- Interactive table with title, price, and rating

# Links

- [books.toscrape.com](https://books.toscrape.com) — data source
- [dbt docs](https://docs.getdbt.com)
- [Airflow docs](https://airflow.apache.org)