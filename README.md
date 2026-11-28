# Insurance Data Reconciliation and Quality Pipeline

## About the Project 🌷

I'm building this project to explore how data engineers work with messy data coming from different sources and turn it into something reliable and useful.

The idea is to simulate two insurance agencies sending policy data that doesn't always match. One agency might have a different policy ID format, a different premium amount, missing customer information, duplicate records, or inconsistent policy statuses.

I wanted to build a project that goes beyond simply cleaning data. The goal is to create a pipeline that can ingest data, standardize it, check its quality, compare records between agencies, identify discrepancies, track exceptions, and eventually make the data available for analysis.

I'm building it step by step, starting with synthetic data generation and gradually adding different parts of the data pipeline.

## Tech Stack

- Python
- Pandas
- NumPy
- PyArrow
- Parquet
- PostgreSQL
- SQL
- SQLAlchemy
- Pytest
- Git and GitHub
- Databricks

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
│   ├── exceptions/
│   ├── reporting/
│   ├── marts/
│   └── warehouse/
│
├── sql/
├── tests/
├── docs/
│   ├── DAILY_PROGRESS.md
│   └── images/
│
├── generate_synthetic_data.py
├── requirements.txt
└── README.md
```

## What I've Built So Far

### 1. Synthetic Data Generation

I created two synthetic insurance datasets to simulate data coming from different agencies.

- Agency A: 1,000 records
- Agency B: 1,100 records

I intentionally introduced some data issues into Agency B to make the reconciliation process more realistic:

- 100 premium mismatches
- 50 duplicate records
- 30 unique policies with missing customer names
- 50 unmatched policies
- Inconsistent policy ID formats
- Inconsistent policy status values

I also made the data generator reproducible using a fixed random seed, so I can generate the same data again when needed.

### 2. Bronze Layer Ingestion

I built a Python ingestion script that reads the agency CSV files and stores them in Parquet format.

Along with the data, I added metadata to track:

- Source system
- Original filename
- Ingestion timestamp
- Ingestion batch ID

I also implemented file hashing to avoid re-ingesting files that haven't changed.

**Validation results:**

| Source | Records |
|---|---:|
| Agency A | 1,000 |
| Agency B | 1,100 |

Both datasets contain 11 columns after adding ingestion metadata. The original missing values and duplicate records are preserved in the Bronze layer so they can be handled in later stages.

### 3. Silver Layer Transformations

I built a Silver transformation pipeline to standardize the data from both agencies.

The transformations include:

- Standardizing policy IDs into a consistent format.
- Normalizing insurance status values, such as `In Force` to `Active`.
- Preserving the original DataFrames and other data columns.

The standardized datasets are saved as Parquet files under their respective agency directories.

### 4. Silver Data Quality Checks

I added a data quality module to check the standardized Silver datasets before reconciliation.

The checks cover:

- Missing required columns
- Missing policy IDs
- Duplicate policy IDs
- Missing customer names
- Missing premium values

The quality report assigns a status to each dataset:

- **PASS:** No issues detected by the implemented checks.
- **WARNING:** One or more data quality issues were detected.
- **FAILED:** Required columns are missing.

**Current validation results:**

| Source | Records | Duplicate Policy IDs | Missing Customer Names | Quality Status |
|---|---:|---:|---:|---|
| Agency A | 1,000 | 0 | 0 | PASS |
| Agency B | 1,100 | 50 | 33 | WARNING |

These checks help identify data issues without automatically removing or modifying records.

### 5. Insurance Data Reconciliation

I built a reconciliation engine to compare standardized insurance policy records between Agency A and Agency B.

The reconciliation process includes:

- Removing exact duplicate records before reconciliation.
- Identifying repeated policy IDs that require investigation.
- Performing a full outer join using standardized policy IDs.
- Comparing customer names, carriers, premiums, statuses, effective dates, and expiration dates.
- Classifying discrepancies based on the affected fields.
- Exporting exception records to CSV and Parquet formats.

**Reconciliation results:**

| Metric | Result |
|---|---:|
| Agency A records | 1,000 |
| Agency B records after exact duplicate removal | 1,050 |
| Matched policies | 1,000 |
| Unmatched Agency B policies | 50 |
| Premium discrepancies | 100 |
| Customer name discrepancies | 30 |
| Unique exception records | 127 |
| Conflicting records requiring investigation | 0 |

Three policies had both premium and customer name discrepancies, which resulted in 127 unique field-level exception records.

The exception outputs are saved as:

- `data/exceptions/reconciliation_exceptions.csv`
- `data/exceptions/reconciliation_exceptions.parquet`

The 50 unmatched Agency B policies are identified separately from field-level exceptions and will be handled in a later stage.

### 6. Exception Management

I built an exception management workflow to make reconciliation discrepancies easier to track and review.

Instead of just identifying differences and leaving them in a file, the workflow creates records that can be followed through the review and resolution process.

It includes:

- Generating unique exception IDs.
- Assigning exception priorities.
- Tracking review statuses.
- Assigning reviewers.
- Recording resolution notes.
- Tracking resolution timestamps.
- Updating exceptions as they move through the workflow.

Exceptions can progress through the following statuses:

- Open
- In Review
- Resolved

The workflow supports assigning reviewers, recording resolution notes, and tracking when exceptions are resolved.

The exception management dataset is saved under `data/exceptions/`.

### 7. Exception Reporting

I built a reporting module to summarize exceptions and monitor their resolution progress.

The report tracks:

- Total field-level exceptions.
- Open exceptions.
- Exceptions under review.
- Resolved exceptions.
- Unresolved exceptions.
- Exception priority distribution.
- Resolution rate.

**Current exception report:**

| Metric | Result |
|---|---:|
| Total field exceptions | 127 |
| Open exceptions | 126 |
| In Review | 0 |
| Resolved exceptions | 1 |
| Unresolved exceptions | 126 |
| High priority | 100 |
| Medium priority | 27 |
| Low priority | 0 |
| Resolution rate | 0.79% |

The exception summary is saved as:

- `data/exceptions/exception_summary.csv`

### 8. Fact Policy Analytics Layer

I built a Fact Policy dataset that brings together reconciled insurance policy records from both agencies into a single analytical dataset.

The dataset makes it easier to analyze policy matching results and identify where discrepancies exist.

It includes:

- Consolidation of both agency datasets using a full outer join.
- Identification of matched and unmatched policies.
- Field-level discrepancy indicators.
- Premium mismatch flags.
- Customer name mismatch flags, including missing values for matched policies.
- Premium difference calculations between agencies.
- Export of the analytical dataset to CSV and Parquet formats.

**Fact Policy dataset results:**

| Metric | Result |
|---|---:|
| Total policy records | 1,050 |
| Matched policies | 1,000 |
| Missing from Agency A | 50 |
| Missing from Agency B | 0 |
| Field discrepancy records | 127 |
| Premium mismatches | 100 |
| Customer name mismatch flags | 80 |

The customer name mismatch flag in the analytical dataset also captures missing-versus-present customer names, which is why it differs from the earlier reconciliation count of 30 name discrepancies.

The Fact Policy dataset is saved as:

- `data/processed/fact_policy.csv`
- `data/processed/fact_policy.parquet`

This dataset provides a foundation for downstream analytics, reconciliation reporting, exception monitoring, and warehouse integration.

### 9. Automated Testing

I created automated tests using Pytest to validate the different modules of the pipeline.

The tests cover:

- CSV-to-Parquet ingestion.
- Preventing duplicate ingestion.
- Creating a new batch when the source file changes.
- Policy ID standardization.
- Status normalization.
- DataFrame preservation.
- Silver data quality checks.
- Quality report generation and validation.
- Duplicate preparation for reconciliation.
- Cross-agency matching.
- Field-level comparisons.
- Discrepancy classification.
- Reconciliation runner execution.
- Exception management dataset generation.
- Exception reporting summary generation.
- Fact Policy dataset generation and mismatch flag validation.

**Current test results: 33 tests passed.**

I run the full test suite using:

```bash
python -m pytest -v
```

### 10. Databricks Reconciliation Dashboard

I also explored the reconciliation workflow using Databricks Free Edition.

I loaded and standardized the agency datasets in Databricks, performed cross-agency reconciliation, and created analytical tables to support dashboard reporting.

I created tables for reconciliation results, exceptions, and summary metrics.

The dashboard visualizes key metrics such as:

- Total exceptions
- Matched policies
- Unmatched policies
- Premium discrepancies
- Customer name discrepancies

![Insurance Reconciliation Dashboard](docs/images/databricks_reconciliation_dashboard.png)

### 11. PostgreSQL Warehouse Integration

I added PostgreSQL to the project to store the analytical data and work with it using SQL.

I connected the Python pipeline to PostgreSQL using SQLAlchemy and loaded the Fact Policy dataset into a warehouse table.

I also loaded the exception management dataset so I could query policy-level analytics alongside exception priority and review status.

**Warehouse tables:**

- `fact_policy`: Stores policy-level reconciliation results, matching status, discrepancy flags, and premium differences.
- `exception_management`: Stores exception records, priorities, review statuses, and supporting reconciliation data.

**Warehouse validation results:**

| Metric | Result |
|---|---:|
| Total policy records | 1,050 |
| Matched policies | 1,000 |
| Missing from Agency A | 50 |
| Missing from Agency B | 0 |
| Premium mismatches | 100 |
| Customer name mismatch flags | 80 |
| Policies with discrepancies | 127 |

### 12. SQL Analytics

I started building reusable SQL queries to analyze the data stored in PostgreSQL.

The queries cover:

- Policy reconciliation KPIs.
- Matched and unmatched policy counts.
- Premium and customer name mismatch counts.
- Total and average premium differences.
- Exception backlog by priority and review status.
- Exception resolution rates.
- Joining policy analytics with exception management records.

**Financial discrepancy analysis:**

| Metric | Result |
|---|---:|
| Premium mismatch count | 100 |
| Total premium difference | $50,000 |
| Average premium difference | $500 |

**Exception workflow analysis:**

| Priority | Total Exceptions | Open | Resolved | Resolution Rate |
|---|---:|---:|---:|---:|
| High | 100 | 99 | 1 | 1.00% |
| Medium | 27 | 27 | 0 | 0.00% |
| Total | 127 | 126 | 1 | 0.79% |

I also tested joining the Fact Policy and exception management tables using `policy_id` to connect analytical results with exception tracking information.

My SQL scripts are saved under the `sql/` directory so they can be reused and version controlled.

## 🗺️ What's Next?

- [x] Generate synthetic insurance data
- [x] Build Bronze ingestion
- [x] Validate Bronze Parquet files
- [x] Test Bronze ingestion
- [x] Set up GitHub repository
- [x] Build Silver layer transformations
- [x] Standardize policy IDs and statuses
- [x] Add data quality checks
- [x] Build cross-agency reconciliation
- [x] Identify and classify field-level discrepancies
- [x] Export reconciliation exceptions
- [x] Test reconciliation runner
- [x] Build exception management workflow
- [x] Build exception reporting
- [x] Build Fact Policy analytics dataset
- [x] Add automated tests for Fact Policy
- [x] Validate full test suite
- [x] Explore Databricks reconciliation
- [x] Build Databricks reconciliation dashboard
- [x] Integrate PostgreSQL
- [x] Load Fact Policy and exception datasets into PostgreSQL
- [x] Build SQL analytics and reporting
- [ ] Investigate and handle unmatched policies
- [ ] Orchestrate the pipeline using Airflow
- [ ] Expand the pipeline with additional data sources