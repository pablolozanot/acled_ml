import os
import requests
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get ACLED API Base URL from environment variable
ACLED_API_URL = os.getenv("ACLED_API_URL")

# BigQuery settings from environment variables
PROJECT_ID = os.getenv("PROJECT_ID", "my-acled-events")
DATASET_ID = os.getenv("DATASET_ID", "acled_events")
TABLE_ID = os.getenv("TABLE_ID", "acled_events")

# Initialize BigQuery client
client = bigquery.Client()

def main():
    print("********** MAIN.PY SCRIPT STARTED **********")

    # Fetch only 10 records
    limit = 10
    offset = 0

    print(f"Fetching {limit} records from ACLED API with offset {offset}...")
    response = requests.get(f"{ACLED_API_URL}&limit={limit}&offset={offset}")

    if response.status_code != 200:
        print(f"Error fetching data: {response.text}")
        return

    data = response.json().get("data", [])
    
    if not data:
        print("No data received from API.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(data).astype(str)
    print(f"DataFrame created with shape: {df.shape}")

    # Display the first few records for verification
    print(df.head())

    # Define BigQuery table reference
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        write_disposition="WRITE_TRUNCATE",  # Overwrite existing data
    )

    print(f"Uploading {len(df)} records to BigQuery...")
    try:
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  # Wait for the job to complete
        print(f"Uploaded {len(df)} records to BigQuery successfully.")
    except Exception as e:
        print(f"Failed to upload data to BigQuery: {e}")

    print(f"********** MAIN.PY SCRIPT COMPLETED **********")

if __name__ == "__main__":
    main()
