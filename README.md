# Cancer Clinical Trials Data Pipeline

An end to end data engineering pipeline that ingests cancer clinical trial data from the ClinicalTrials.gov API, transforms it using dbt, and visualizes insights through a Streamlit dashboard.

## Architecture

## Tech Stack

| Tool | Purpose |
|---|---|
| Apache Airflow | Pipeline orchestration and scheduling |
| Docker Compose | Local Airflow infrastructure |
| ClinicalTrials.gov API | Data source |
| Google BigQuery | Cloud data warehouse |
| dbt | Data transformation and quality testing |
| Streamlit | Analytics dashboard |
| Python | Core programming language |

## Pipeline Overview

1. **Ingest** — Airflow DAG runs daily, fetching cancer trial records from the ClinicalTrials.gov REST API and landing raw JSON to disk
2. **Load** — Raw JSON is flattened and loaded into BigQuery using a truncate-and-reload pattern
3. **Transform** — dbt staging model cleans and types the raw data; mart model aggregates trials by status, sponsor count, and date range
4. **Test** — dbt data quality tests validate uniqueness and null constraints on critical fields
5. **Visualize** — Streamlit dashboard surfaces trial counts, sponsor activity, and enrollment trends

## dbt Models
models/

├── staging/

│   ├── sources.yml

│   ├── schema.yml

│   └── stg_clinical_trials.sql

└── marts/

└── trial_summary.sql

## Project Structure
cancer-trials-pipeline/
├── dags/
│   └── clinical_trials_fetch.py
├── clinical_trials_dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── dbt_project.yml
├── dashboard.py
├── docker-compose.yaml
└── .gitignore

