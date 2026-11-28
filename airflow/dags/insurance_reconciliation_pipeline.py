from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT = "/opt/insurance-pipeline"

with DAG(
    dag_id="insurance_reconciliation_pipeline",
    description="End-to-end insurance data ingestion, quality, reconciliation and reporting",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["insurance", "data-quality", "reconciliation"],
) as dag:

    generate_data = BashOperator(
        task_id="generate_synthetic_data",
        bash_command=f"cd {PROJECT} && export PYTHONPATH={PROJECT} && python generate_synthetic_data.py",
    )

    bronze = BashOperator(
        task_id="bronze_ingestion",
        bash_command=f"cd {PROJECT} && export PYTHONPATH={PROJECT} && python src/ingestion/bronze_ingestion.py",
    )

    silver = BashOperator(
        task_id="silver_transformation",
        bash_command=f"cd {PROJECT} && export PYTHONPATH={PROJECT} && python src/transformations/silver_pipeline.py",
    )

    quality = BashOperator(
        task_id="silver_quality_checks",
        bash_command=f"cd {PROJECT} && export PYTHONPATH={PROJECT} && python src/quality/silver_quality.py",
    )

    reconciliation = BashOperator(
        task_id="reconciliation",
        bash_command=f"cd {PROJECT} && export PYTHONPATH={PROJECT} && python src/reconciliation/run_reconciliation.py",
    )

    exception_management = BashOperator(
        task_id="exception_management",
        bash_command=f"cd {PROJECT} && export PYTHONPATH={PROJECT} && python src/exceptions/run_exception_management.py",
    )

    exception_reporting = BashOperator(
        task_id="exception_reporting",
        bash_command=f"cd {PROJECT} && export PYTHONPATH={PROJECT} && python src/reporting/run_exception_report.py",
    )

    fact_policy = BashOperator(
        task_id="build_fact_policy",
        bash_command=f"cd {PROJECT} && export PYTHONPATH={PROJECT} && python src/marts/run_fact_policy.py",
    )

    generate_data >> bronze >> silver >> quality >> reconciliation
    reconciliation >> exception_management >> exception_reporting
    reconciliation >> fact_policy
