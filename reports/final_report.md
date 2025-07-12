# FINAL REPORT

Prepared by :Gebrehiwot Tesfaye

## Introduction

This report documents the complete development of a robust, end-to-end analytics pipeline for Ethiopian medical Telegram channels. The project covers all stages from environment setup to orchestration, integrating Python, PostgreSQL, dbt, YOLO object detection, FastAPI, and Dagster. The pipeline is designed for scalability, reliability, and extensibility, supporting advanced analytics and business intelligence.

## Project Overview

### Task 0: Environment Setup

- **Repository Structure:** Organized folders for raw data, processed data, ETL scripts, dbt models, enrichment, and documentation.
- **Environment Management:** Used `.env` files for secrets and Python virtual environments for dependency isolation.
- **Database Initialization:** Installed PostgreSQL, created the `telegram_analytics` database, and configured user roles.
- **Tool Justification:** PostgreSQL was chosen for its reliability and compatibility with analytics workflows; Python for its rich ecosystem and flexibility.

### Task 1: Data Scraping and Collection

- **Telegram Scraper:** Built with Telethon, the scraper collects messages and images from target channels. Incremental scraping is achieved by tracking the last message ID, ensuring efficient updates and no duplicates.
- **Data Lake Structure:** Data is partitioned by date and channel, supporting reproducibility and easy management.
- **Preprocessing:** Messages are cleaned to remove nulls and duplicates; images are downloaded and organized for enrichment.
- **Technical Justification:** Telethon provides robust access to Telegram APIs, supporting both message and media extraction.

**Sample Data Table:**

| id    | date                | text | media | media_path | channel_id        | channel_name      | channel_url                    | sender_id | is_reply |
| ----- | ------------------- | ---- | ----- | ---------- | ----------------- | ----------------- | ------------------------------ | --------- | -------- |
| 18517 | 2025-07-10 14:50:22 | ...  | true  | media/...  | lobelia4cosmetics | lobelia4cosmetics | https://t.me/lobelia4cosmetics | 123456789 | false    |

### Task 2: Data Modeling and Transformation

- **Database Loading:** Automated ETL scripts load preprocessed JSON into PostgreSQL, ensuring schema consistency.
- **dbt Project:** Modular transformations, tests, and documentation are managed in dbt. The star schema includes:
  - **Fact Table:** `fct_messages` (one row per message)
  - **Dimension Tables:** `dim_channels`, `dim_dates`
  - **Staging Layer:** Cleans and prepares raw data
- **Testing & Documentation:** dbt tests enforce data quality; dbt docs provide transparency.
- **Technical Justification:** dbt enables versioned, testable, and documented SQL transformations, critical for analytics reliability.

**Star Schema Diagram:**

+----------------+ +-------------------+
| dim_channels | | dim_dates |
+----------------+ +-------------------+
| channel_id | | date_id |
| channel_name | | year |
| channel_url | | month |
+----------------+ | day |
+-------------------+
\ /
\ /
\ /
\ /
\ /
\ /
\ /
\ /
\ /
\ /
\ /
+-------------------+
| fct_messages |
+-------------------+
| message_id |
| date |
| text |
| media |
| media_path |
| channel_id (FK) |
| channel_name |
| channel_url |
| sender_id |
| is_reply |
| message_length |
| has_image |
+-------------------+

### Task 3: Data Enrichment with Object Detection

- **YOLO Integration:** YOLOv8 is used to detect objects in images scraped from Telegram. Detected objects and metadata are stored in a new dimension table (`dim_objects`) and linked to messages.
- **Enrichment Pipeline:** Images are processed, and results are appended to the analytics database for further analysis.
- **Technical Justification:** YOLO is state-of-the-art for real-time object detection, enabling rich visual analytics.

**Sample Detection Output:**

| image_path | detected_objects     | confidence_scores |
| ---------- | -------------------- | ----------------- |
| ...jpg     | ["bottle", "person"] | [0.98, 0.87]      |

### Task 4: Analytical API Development

- **FastAPI Implementation:** A REST API exposes analytical endpoints for channel summaries, message trends, and object detection results.
- **Endpoints:** `/api/channels`, `/api/messages`, `/api/posts`, etc.
- **Security & Documentation:** API uses environment variables for secrets and includes OpenAPI docs.
- **Technical Justification:** FastAPI is chosen for its speed, automatic docs, and async support.

### Task 5: Pipeline Orchestration

- **Dagster Orchestration:** The entire workflow is automated and observable using Dagster. Each stage (scraping, loading, transformation, enrichment) is an op in a Dagster job.
- **Scheduling:** The pipeline is scheduled to run daily at 2am, with monitoring and logging.
- **Integration:** Dagster UI provides visibility into jobs, assets, sensors, and resources.
- **Technical Justification:** Dagster offers local development, scheduling, and observability, making it ideal for production-grade pipelines.

## Technical Analysis & Findings

- **Comprehensiveness:** The pipeline covers extraction, transformation, enrichment, API serving, and orchestration, supporting both technical and business analytics.
- **Data Quality:** Automated tests and schema enforcement ensure high-quality, trustworthy data.
- **Scalability:** Modular design and orchestration allow for easy scaling and future feature additions.
- **Integration:** All tools (Python, PostgreSQL, dbt, YOLO, FastAPI, Dagster) are integrated seamlessly, with clear handoffs between stages.

## Visuals

- **Star Schema Diagram:** (see above)
- **Sample Detection Table:** (see above)
- **Dagster UI Screenshot:** Shows jobs, assets, sensors, and schedules for full observability.

## Technical Justification of Tools and Methods

- **Python:** Flexible scripting and rich libraries for ETL, scraping, and ML.
- **PostgreSQL:** Reliable, scalable, and well-supported for analytics.
- **dbt:** Modular, testable, and documented SQL transformations.
- **YOLO:** Industry-standard for object detection.
- **FastAPI:** Modern, fast, and well-documented API framework.
- **Dagster:** Robust orchestration, scheduling, and monitoring.

## Reflection on Challenges and Key Takeaways

- **Incremental Scraping:** Required careful tracking of message IDs to avoid duplicates.
- **Schema Drift:** Early inconsistencies were resolved by standardizing preprocessing.
- **Package Management:** Ensured all dependencies were installed in the correct environment for Dagster subprocesses.
- **Orchestration:** Dagster’s local development experience made debugging and scheduling straightforward.
- **Key Takeaway:** Building a production-grade pipeline requires attention to data quality, modularity, and observability. Integrating best-in-class tools at each stage ensures reliability and scalability.

## Conclusion

This project successfully delivers a comprehensive analytics pipeline for Telegram channel data, supporting advanced enrichment and API-driven insights. The integration of robust tools and careful attention to data quality and orchestration lays a strong foundation for future analytics and business intelligence applications.
