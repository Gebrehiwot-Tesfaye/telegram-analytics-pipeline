# INTERIM REPORT

## Introduction

This project aims to build a robust, end-to-end data pipeline for extracting, transforming, and analyzing Telegram channel data for Ethiopian medical businesses. The pipeline leverages Python, PostgreSQL, and dbt to ensure scalable, trustworthy analytics, and is designed to support downstream machine learning and business intelligence use cases. The ultimate goal is to create a reliable data foundation for advanced analytics, including image-based object detection and API-driven insights.

---

## Methodology

### Task 0: Environment Setup

- **Repository Initialization:** Set up a structured project repository with clear folder organization for raw data, preprocessed data, ETL scripts, dbt models, and documentation.
- **Environment Management:** Used `.env` files for secure credential management and Python virtual environments for dependency isolation.
- **Database Setup:** Installed and configured PostgreSQL, created the `telegram_analytics` database, and established user roles and permissions.

### Task 1: Data Scraping and Collection (Extract & Load)

- **Telegram Scraper:** Developed a Python script using Telethon to scrape messages and images from target Telegram channels. The scraper supports incremental updates by tracking the last scraped message ID for each channel, ensuring no duplicates and efficient daily updates.
- **Data Lake Structure:** Raw and preprocessed data are stored in a partitioned directory structure by date and channel, facilitating easy management and reproducibility.
- **Preprocessing:** Cleaned and filtered messages to remove those with null/empty text or missing channel information. Downloaded and organized images for future enrichment.

**Sample Data Structure:**

| id    | date                | text        | media | media_path       | channel_id         | channel_name         | channel_url                    | sender_id   | is_reply |
|-------|---------------------|-------------|-------|------------------|--------------------|----------------------|-------------------------------|-------------|----------|
| 18517 | 2025-07-10 14:50:22 | ...         | true  | media/...        | lobelia4cosmetics  | lobelia4cosmetics    | https://t.me/lobelia4cosmetics | 123456789   | false    |

### Task 2: Data Modeling and Transformation (Transform)

- **Database Loading:** Automated loading of preprocessed JSON data into PostgreSQL, ensuring all relevant fields are present and mapped to the database schema.
- **dbt Project:** Initialized and configured a dbt project for modular, testable, and documented data transformations.
- **Star Schema Modeling:** Built a star schema with:
  - **Fact Table:** `fct_messages` (one row per message, with all relevant fields and foreign keys)
  - **Dimension Tables:** `dim_channels` (channel metadata), `dim_dates` (date breakdown)
  - **Staging Layer:** Cleans, deduplicates, and prepares raw data for analytics
- **Testing & Documentation:** Implemented dbt tests for uniqueness, not-null constraints, and custom business rules. Generated dbt docs for transparency and maintainability.

**Sample dbt Model Diagram:**

```
+----------------+        +-------------------+
|  dim_channels  |        |    dim_dates      |
+----------------+        +-------------------+
| channel_id     |        | date_id           |
| channel_name   |        | year              |
| channel_url    |        | month             |
+----------------+        | day               |
                          +-------------------+
         \                      /
          \                    /
           \                  /
            \                /
             \              /
              \            /
               \          /
                \        /
                 \      /
                  \    /
                   \  /
                +-------------------+
                |   fct_messages    |
                +-------------------+
                | message_id        |
                | date              |
                | text              |
                | media             |
                | media_path        |
                | channel_id (FK)   |
                | channel_name      |
                | channel_url       |
                | sender_id         |
                | is_reply          |
                | message_length    |
                | has_image         |
                +-------------------+
```

---

## Challenges & Solutions

- **Incremental Scraping:** Ensuring no duplicate messages and efficient updates required tracking the last scraped message ID per channel. Solution: Implemented a `last_scraped` tracker and used Telethon’s `min_id` parameter.
- **Schema Drift:** Early data files had missing or inconsistent fields, causing database load errors. Solution: Standardized the scraping and preprocessing scripts to always include all required fields.
- **Data Quality:** Nulls and duplicates in source data led to dbt test failures. Solution: Added deduplication and not-null filtering in the staging layer.
- **Database Mismatches:** Loader errors occurred when JSON fields didn’t match the database schema. Solution: Synchronized the schema and loader, and added missing columns as needed.

---

## Future Plan

### Task 3: Data Enrichment with Object Detection (YOLO)

- Integrate YOLO-based object detection to analyze images scraped from Telegram channels.
- Store detected objects and their metadata in a new dimension table (`dim_objects`) and link them to messages in the fact table.
- Visualize sample detections and enrich analytics with object-level insights.

### Task 4: Build an Analytical API (FastAPI)

- Develop a FastAPI-based REST API to serve analytical queries and insights from the data warehouse.
- Endpoints will support channel-level summaries, message trends, and object detection results.
- Secure and document the API for easy integration with dashboards or external apps.

### Task 5: Pipeline Orchestration

- Automate the entire pipeline using orchestration tools (e.g., Prefect, Airflow, or custom scripts).
- Schedule regular scraping, enrichment, loading, and dbt runs.
- Implement monitoring, logging, and alerting for reliability.

---

## Conclusion

Significant progress has been made in building a scalable, analytics-ready pipeline for Telegram channel data. The project now features robust data extraction, cleaning, and modeling, with a tested and documented star schema in place. The foundation is set for advanced enrichment, API development, and orchestration in the coming days. Confidence is high that the remaining tasks will be completed on schedule, delivering a powerful platform