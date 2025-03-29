import os
import requests
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ACLED API Base URL
ACLED_API_URL = os.getenv("ACLED_API_URL")

# BigQuery settings
PROJECT_ID = os.getenv("PROJECT_ID", "my-acled-events")
DATASET_ID = os.getenv("DATASET_ID", "acled_events")
TABLE_ID = os.getenv("TABLE_ID", "acled_events")

# Initialize BigQuery client
client = bigquery.Client()

def fetch_data():
    page = 1
    limit = 5000  # Updated batch size per request
    total_uploaded = 0

    while True:
        response = requests.get(f"{ACLED_API_URL}&limit={limit}&page={page}")

        if response.status_code != 200:
            print(f"Error fetching page {page}: {response.text}")
            break

        data = response.json().get("data", [])

        if not data:
            print(f"Completed fetching all pages. Total records uploaded: {total_uploaded}.")
            break

        # Convert to DataFrame
        df = pd.DataFrame(data).astype(str)

        # Upload to BigQuery
        table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            write_disposition="WRITE_APPEND",  # Append data instead of overwriting
        )

        try:
            job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
            job.result()
            total_uploaded += len(df)
            print(f"Page {page}: Uploaded {len(df)} records. Total so far: {total_uploaded}")
        except Exception as e:
            print(f"Failed to upload data on page {page}: {e}")
            break

        page += 1  # Move to the next page

def main():
    print("********** Fetching ACLED Data Started **********")
    fetch_data()
    print("********** Fetching ACLED Data Completed **********")

if __name__ == "__main__":
    main()
