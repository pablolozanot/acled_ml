# ACLED ML Project

This repository contains a full pipeline for acquiring, processing, and modeling data from the ACLED (Armed Conflict Location & Event Data) dataset. The goal is to classify conflict events into their respective event types using both structured data and natural language processing (NLP) methods.

---

## Project Structure

```
acled_ml/
├── data/                  # (ignored) Optional local datasets or exports from BigQuery
├── notebooks/             # Jupyter notebooks for exploration and modeling
├── models/                # (ignored) Trained models (.pkl, etc.)
├── src/                   # Python modules for preprocessing, training, evaluation
│   ├── preprocessing.py
│   ├── train.py
│   ├── evaluate.py
│   └── utils.py
├── main.py                # Data ingestion script to pull from ACLED API and upload to BigQuery
├── Dockerfile             # Containerized environment to run ingestion pipeline
├── requirements.txt       # Project dependencies
├── .env                   # (ignored) Local environment variables (API keys, project ID)
├── .env.example           # Example .env file for reuse
└── README.md              # Project documentation
```

---

## What Has Been Done So Far

### Data Ingestion
- Implemented a Python script (`main.py`) that uses ACLED's API with pagination to retrieve data in batches of 20,000 rows.
- Uploaded event data to Google BigQuery using the `google-cloud-bigquery` package.
- Managed pagination with the `page` parameter as recommended by ACLED's documentation.

### Cloud Infrastructure
- Used Google Cloud Shell to build and test the data pipeline.
- Deployed data ingestion via Cloud Run jobs using a custom Docker container.
- Configured BigQuery to store all ACLED records.

### Dockerization
- Created a Dockerfile to ensure consistent environments.
- Docker image includes dependencies and runs `main.py` when executed.
- Successfully tested Docker locally and in the cloud.

---

## .gitignore / Secrets Management
Sensitive or environment-specific files are excluded from Git:

```bash
.env
*.csv
models/
data/
service_account.json
__pycache__/
*.pyc
```

If you're cloning or forking this repo:
- Copy `.env.example` to `.env`
- Fill in your configuration values like this:

```
# .env.example
ACLED_API_URL=https://api.acleddata.com/acled/read?terms=accept&key=your_key&email=your_email
PROJECT_ID=your-google-cloud-project-id
DATASET_ID=your_bigquery_dataset_name
TABLE_ID=your_bigquery_table_name
```

The `service_account.json` file is your Google Cloud service account key. It can be generated from the Google Cloud Console by:
1. Going to IAM & Admin > Service Accounts
2. Creating a new service account or selecting an existing one
3. Generating a new key (JSON format)
4. Downloading and saving the key file as `service_account.json`

This file should not be committed to Git. It is used to authenticate BigQuery uploads when running outside the Google Cloud environment.

---

