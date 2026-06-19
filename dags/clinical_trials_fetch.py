from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def fetch_trials():
    import requests
    import json
    import os
    from datetime import datetime

    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.cond": "cancer",
        "pageSize": 100,
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    studies = data.get("studies", [])

    output_dir = "/opt/airflow/logs/raw"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"{output_dir}/trials_{timestamp}.json"

    with open(output_path, "w") as f:
        json.dump(studies, f, indent=2)

    print(f"Fetched {len(studies)} studies")
    print(f"Saved to {output_path}")

def load_to_bigquery():
    from google.cloud import bigquery
    import json
    import os
    import glob

    client = bigquery.Client()
    table_id = "cancer-trials-pipeline.clinical_trials.raw_studies"

    raw_files = glob.glob("/opt/airflow/logs/raw/trials_*.json")
    if not raw_files:
        raise Exception("No raw files found to load")

    latest_file = max(raw_files, key=os.path.getctime)
    print(f"Loading file: {latest_file}")

    with open(latest_file, "r") as f:
        studies = json.load(f)
    
    rows = []
    for study in studies:
        protocol = study.get("protocolSection", {})
        identification = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        sponsors = protocol.get("sponsorCollaboratorsModule", {})
        conditions = protocol.get("conditionsModule", {})

        rows.append({
            "nct_id": identification.get("nctId"),
            "brief_title": identification.get("briefTitle"),
            "overall_status": status.get("overallStatus"),
            "start_date": status.get("startDateStruct", {}).get("date"),
            "sponsor_name": sponsors.get("leadSponsor", {}).get("name"),
            "conditions": str(conditions.get("conditions", [])),
        })

    errors = client.insert_rows_json(table_id, rows)
    if errors:
        raise Exception(f"BigQuery insert errors: {errors}")
    
    print(f"Loaded {len(rows)} rows to BigQuery")


with DAG(
    dag_id="clinical_trials_fetch",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    fetch_task = PythonOperator(
        task_id="fetch_trials",
        python_callable=fetch_trials,
    )

    load_task = PythonOperator(
        task_id="load_to_bigquery",
        python_callable=load_to_bigquery,
    )

    fetch_task >> load_task
