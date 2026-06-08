# 📈 Market ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql) ![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)

An automated, containerized **Extract, Transform, Load (ETL)** pipeline designed to harvest financial time-series data and build a robust data lake for quantitative research and algorithmic trading models. 

## 🏗️ Architecture & Core Technologies
This project is built with a microservices-oriented architecture, emphasizing *Separation of Concerns* and reproducible environments:
* **Python (Data Worker):** Handles the extraction of OHLCV (Open, High, Low, Close, Volume) data via Yahoo Finance API (`yfinance`), transforms complex multi-index DataFrames, and ensures data integrity.
* **PostgreSQL (Data Storage):** Serves as the robust, persistent relational database holding historical market data, optimized for high-speed quantitative querying.
* **SQLAlchemy (ORM):** Bridges the Python worker and the database, defining rigorous data schemas and managing connection pools and safe transactions (commit/rollback).
* **Docker & Docker Compose:** Encapsulates the entire infrastructure into isolated containers with a custom network and persistent volume storage (`Named Volumes`).

## 🚀 Current Status (v1.0 - Core Pipeline Completed)
As of the current iteration, the foundational pipeline is fully operational.
* ✅ **Extract:** Successfully pulls historical daily market data for specified assets (e.g., AAPL, NVDA) using `yfinance`.
* ✅ **Transform:** Flattens MultiIndex Pandas DataFrames and casts financial metrics into strict database-compatible formats (Double Precision/Float for prices, BigInteger for volumes).
* ✅ **Load:** Safely inserts the transformed objects into the PostgreSQL database using SQLAlchemy sessions.
* ✅ **Infrastructure:** The system runs flawlessly via `docker compose up`, with database persistence preventing data loss between container restarts.

## 🛠️ Quick Start

**Prerequisites:** You must have [Docker](https://www.docker.com/) and Docker Compose installed on your system.

1. Clone the repository:
```bash
git clone [https://github.com/erenkasap/market-etl-pipeline.git](https://github.com/erenkasap/market-etl-pipeline.git)
cd market-etl-pipeline
```

2. Start the pipeline in detached mode:
```bash
docker compose up -d --build
```

3. To view the data inside the database, open a terminal tunnel to the Postgres container:
```bash
docker compose exec postgres psql -U eren -d market-data
```

4. Query the data:
```sql
SELECT * FROM market_data;
```

## 🗺️ Future Roadmap & Quantitative Goals

This pipeline is the foundational layer for advanced quantitative financial modeling. Future development phases include:

### Phase 1: Data Integrity & Automation
* **Idempotency (Upserts):** Implement `ON CONFLICT DO UPDATE` constraints at the database level to prevent duplicate row insertions when the script is run multiple times.
* **Workflow Orchestration:** Integrate **Apache Airflow** or `cron` to schedule the pipeline to run automatically at market close every day.
* **Dynamic Extraction:** Refactor the extraction logic to pull data for a dynamic basket of assets (e.g., S&P 500 constituents) rather than hardcoded tickers.

### Phase 2: Quantitative Modeling & AI Integration
* **Statistical Analysis:** Connect the database to Jupyter environments to run Time-Series models like **ARIMA** (AutoRegressive Integrated Moving Average) and **GARCH** (for volatility clustering).
* **Machine Learning:** Utilize the structured OHLCV data to train predictive classification models using **XGBoost** and **Random Forests**.
* **Graph-Based Correlation:** Apply Graph Neural Networks (GNNs) to analyze the complex correlation matrix between different equities.

## 👨‍💻 Author
**Eren Hasan Kasap** B.E. Mathematical Engineering Student | Aspiring Quantitative Researcher  
[LinkedIn](https://www.linkedin.com/in/erenkasap) | [Portfolio](https://erenhasankasap.tech)
