# telegram-analytics-pipeline

A robust, analytics-ready data pipeline for extracting, transforming, and modeling Telegram channel data for Ethiopian medical businesses. Built with Python, PostgreSQL, and dbt, this project enables scalable, trustworthy analytics for business intelligence and machine learning.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Folder Structure](#folder-structure)
- [Task 0: Environment Setup](#task-0-environment-setup)
- [Task 1: Data Scraping and Collection (Extract & Load)](#task-1-data-scraping-and-collection-extract--load)
- [Task 2: Data Modeling and Transformation (Transform)](#task-2-data-modeling-and-transformation-transform)
- [How to Run](#how-to-run)
- [DBT Analytics & Documentation](#dbt-analytics--documentation)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

This pipeline:
- Scrapes messages and images from public Telegram channels.
- Stores raw and preprocessed data in a structured data lake.
- Loads data into a PostgreSQL database.
- Uses dbt to transform raw data into a clean, star-schema warehouse for analytics.
- Provides robust testing, documentation, and modularity for scalable analytics.

---

## Folder Structure

```
telegram-analytics-pipeline/
│
├── analyses/           # dbt ad-hoc analysis queries
├── data/               # Raw and preprocessed data lake
│   ├── preprocessed/
│   └── raw/
├── macros/             # dbt custom macros
├── models/             # dbt models (staging, marts, schema.yml)
│   ├── marts/
│   └── staging/
├── seeds/              # dbt seed data (channels.csv)
├── src/                # Python ETL scripts
├── tests/              # dbt custom tests
├── .env                # Environment variables (not committed)
├── dbt_project.yml     # dbt project config
└── requirements.txt    # Python dependencies
```

---

## Task 0: Environment Setup

1. **Clone the repository**
2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install dbt and PostgreSQL adapter**
   ```bash
   pip install dbt-postgres
   ```
4. **Set up your `.env` file** (see `.env.example` for template):
   ```
   TELEGRAM_API_ID=...
   TELEGRAM_API_HASH=...
   POSTGRES_USER=telegram_analytics
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database name here
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

---

## Task 1: Data Scraping and Collection (Extract & Load)

- **Scrape messages and images** from target Telegram channels using `src/scrape_telegram.py`.
- **Store raw data** as JSON in `data/raw/telegram_messages/YYYY-MM-DD/channel_name.json`.
- **Download images** to `media/YYYY-MM-DD/channel_name/`.
- **Preprocess data** to remove messages with null/empty text or missing channel info, saving results in `data/preprocessed/YYYY-MM-DD/channel_name_preprocessed.json`.
- **Log scraping activity** for traceability.

**Example run:**
```bash
python src/scrape_telegram.py
```

---

## Task 2: Data Modeling and Transformation (Transform)

### 1. **Load Data into PostgreSQL**

- **Load preprocessed messages** into the `raw_telegram_messages` table:
  ```bash
  python src/load_to_postgres.py
  ```
- **Load channel metadata** into the `channels` table:
  ```bash
  python src/load_channels.py
  ```

### 2. **DBT Project Setup**

- **Initialize dbt project** (already done):
  ```bash
  dbt init telegram_analytics
  ```
- **Configure your profile** in `~/.dbt/profiles.yml` to match your `.env` credentials.

### 3. **DBT Workflow**

- **Seed channel dimension:**
  ```bash
  dbt seed
  ```
- **Run all models (staging, marts/star schema):**
  ```bash
  dbt run
  ```
- **Run tests:**
  ```bash
  dbt test
  ```
- **Generate and serve documentation:**
  ```bash
  dbt docs generate
  dbt docs serve
  ```

### 4. **Star Schema**

- **Fact Table:** `fct_messages` (one row per message, with channel_id as foreign key, message text, media path, etc.)
- **Dimension Tables:** `dim_channels` (channel info), `dim_dates` (date breakdown)
- **Staging Layer:** Cleans and deduplicates raw data before loading into marts.

---

## How to Run

1. Scrape and preprocess data:  
   `python src/scrape_telegram.py`
2. Load data to PostgreSQL:  
   `python src/load_channels.py`  
   `python src/load_to_postgres.py`
3. Run dbt pipeline:  
   `dbt seed`  
   `dbt run`  
   `dbt test`
   `dbt docs generate`
4. Explore analytics:  
   `dbt docs serve`

---

## DBT Analytics & Documentation

- Use the dbt dashboard to explore your star schema, run ad-hoc queries (see `analyses/`), and view model documentation and test results.
- Example analysis:  
  `analyses/top_channels.sql` shows the most active channels by message count.

---

## Troubleshooting

- **Database connection errors:** Check your `.env` and `profiles.yml` for correct credentials.
- **Missing columns:** Ensure your data and tables include all required fields (`id`, `channel_id`, `media_path`, etc.).
- **Test failures:** Clean your data to ensure unique, non-null IDs and valid foreign keys.

---

**This pipeline is now ready for robust, scalable analytics and can be extended for further machine learning or business intelligence use cases.**