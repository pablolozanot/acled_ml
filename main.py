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

    offset = 0
    limit = 30000  # Fetch 30,000 records per API call
    total_uploaded = 0
    batch_number = 0

    while True:
        batch_number += 1
        print(f"Batch {batch_number}: Fetching data from ACLED API with offset {offset}...")
        response = requests.get(f"{ACLED_API_URL}&limit={limit}&offset={offset}")

        if response.status_code != 200:
            print(f"Error fetching data: {response.text}")
            break

        data = response.json().get("data", [])
        
        if not data:
            print("No more data received from API.")
            break

        # Convert to DataFrame
        df = pd.DataFrame(data).astype(str)
        print(f"Batch {batch_number}: DataFrame created with shape: {df.shape}")

        # Define BigQuery table reference
        table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            write_disposition="WRITE_APPEND",  # Append data to existing table
        )

        print(f"Batch {batch_number}: Uploading {len(df)} records to BigQuery...")
        try:
            job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
            job.result()  # Wait for the job to complete
            total_uploaded += len(df)
            print(f"Batch {batch_number}: Uploaded {len(df)} records. Total uploaded: {total_uploaded}")
        except Exception as e:
            print(f"Failed to upload data to BigQuery: {e}")
            break

        offset += limit

    print(f"********** MAIN.PY SCRIPT COMPLETED. Total records uploaded: {total_uploaded} **********")

if __name__ == "__main__":
    main()
