# Insurance Data Reconciliation and Quality Pipeline

## About the Project 🌷

I'm building this project to explore how data engineers handle messy data coming from different sources.

The idea is to simulate two insurance agencies sending policy data that doesn't always match. One agency might have a different policy ID format, a different premium amount, missing customer information, or even duplicate records.

I want to build a pipeline that can identify these differences, clean up the data, and eventually bring everything together into a reliable dataset.

I'm building this step by step, starting with synthetic data generation and moving through the different stages of a data pipeline.

## Tech Stack

- Python
- Pandas
- NumPy
- PyArrow
- Parquet
- Pytest
- Git and GitHub

## Project Structure

```text
insurance-data-reconciliation-pipeline/
│
├── data/
│   ├── raw/
│   │   ├── agency_a/
│   │   ├── agency_b/
│   │   └── generation_metadata.json
│   ├── bronze/
│   │   ├── agency_a/
│   │   └── agency_b/
│   ├── silver/
│   │   ├── agency_a/
│   │   └── agency_b/
│   ├── processed/
│   └── exceptions/
│
├── src/
│   ├── ingestion/
│   ├── transformations/
│   ├── reconciliation/
│   ├── quality/
│   └── warehouse/
│
├── tests/
├── docs/
│   └── DAILY_PROGRESS.md
│
├── generate_synthetic_data.py
├── requirements.txt
└── README.md
```

## What I've Built So Far

### 1. Synthetic Data Generation

Created two synthetic insurance datasets:

- Agency A: 1,000 records
- Agency B: 1,100 records

I intentionally introduced some data issues into Agency B:

- 100 premium mismatches
- 50 duplicate records
- 30 unique policies with missing customer names
- 50 unmatched policies
- Inconsistent policy ID formats and status values

I also checked that the data generator produces the same output when run again using a fixed random seed.

### 2. Bronze Layer Ingestion

Built a Python ingestion script that reads both agency CSV files and saves them in Parquet format.

Added metadata to track:

- Source system
- Original filename
- Ingestion timestamp
- Ingestion batch ID

I also implemented file hashing to prevent unchanged files from being ingested repeatedly.

**Validation results:**

- Agency A: 1,000 rows
- Agency B: 1,100 rows
- Both datasets contain 11 columns after adding metadata.
- Original missing values and duplicate records are preserved.

### 3. Silver Layer Transformations

Built a Silver transformation pipeline to standardize insurance data from both agencies.

Implemented transformations for:

- Standardizing policy IDs into a consistent format.
- Normalizing insurance status values, such as `In Force` to `Active`.

The transformations preserve the original DataFrame and other data columns.

Silver data is saved as Parquet files under the respective agency directories.

### 4. Silver Data Quality Checks

Built a data quality module to validate the standardized Silver datasets.

Implemented checks for:

- Missing required columns
- Missing policy IDs
- Duplicate policy IDs
- Missing customer names
- Missing premium values

The quality report assigns a status to each dataset:

- **PASS:** No issues detected by the implemented checks.
- **WARNING:** One or more data quality issues detected.
- **FAILED:** Required columns are missing.

**Current validation results:**

| Source | Records | Duplicate Policy IDs | Missing Customer Names | Quality Status |
|---|---:|---:|---:|---|
| Agency A | 1,000 | 0 | 0 | PASS |
| Agency B | 1,100 | 50 | 33 | WARNING |

These checks identify data issues without automatically removing or modifying records.

### 5. Automated Testing

Created automated tests using Pytest for:

- Successful CSV-to-Parquet ingestion
- Preventing duplicate ingestion
- Creating a new batch when the source file changes
- Policy ID standardization
- Status normalization
- DataFrame preservation
- Silver data quality checks
- Quality report generation and validation

**Current test results: 25 tests passed.**

## 🗺️ What's Next?

- [x] Generate synthetic insurance data
- [x] Build Bronze ingestion
- [x] Validate Bronze Parquet files
- [x] Test Bronze ingestion
- [x] Set up GitHub repository
- [x] Build Silver layer transformations
- [x] Standardize policy IDs and statuses
- [x] Add data quality checks
- [ ] Build cross-agency reconciliation
- [ ] Handle exceptions
- [ ] Build reporting tables
```
