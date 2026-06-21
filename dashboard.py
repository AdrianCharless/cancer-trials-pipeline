import streamlit as st
from google.cloud import bigquery
import pandas as pd
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/google_credentials.json"

client = bigquery.Client()

st.title("Cancer Clinical Trials Dashboard")
st.markdown("Data sourced from ClinicalTrials.gov via an automated Airflow pipeline")

@st.cache_data
def load_trial_summary():
    query = """
        SELECT * FROM `cancer-trials-pipeline.clinical_trials.trial_summary`
        ORDER BY trial_count DESC
    """
    return client.query(query).to_dataframe()

@st.cache_data
def load_raw_studies():
    query = """
        SELECT * FROM `cancer-trials-pipeline.clinical_trials.stg_clinical_trials`
    """
    return client.query(query).to_dataframe()

summary_df = load_trial_summary()
studies_df = load_raw_studies()

st.subheader("Trials by Status")
st.bar_chart(summary_df.set_index("overall_status")["trial_count"])

st.subheader("Unique Sponsors by Status")
st.bar_chart(summary_df.set_index("overall_status")["unique_sponsors"])

st.subheader("Trial Summary Table")
st.dataframe(summary_df)

st.subheader("All Trials")
st.dataframe(studies_df)