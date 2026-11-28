
import os

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    """Create a SQLAlchemy engine for the project PostgreSQL database."""

    db_name = os.getenv("DB_NAME", "insurance_reconciliation")
    db_user = os.getenv("DB_USER", "deekshithareddykalluru")
    db_host = os.getenv("DB_HOST", "/tmp")
    db_port = os.getenv("DB_PORT", "5432")

    connection_url = (
        f"postgresql+psycopg2://{db_user}@/{db_name}"
        f"?host={db_host}&port={db_port}"
    )

    return create_engine(connection_url)


def test_connection() -> bool:
    """Test connectivity to the PostgreSQL database."""

    engine = get_engine()

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"PostgreSQL connection successful: {result.scalar()}")
            return True
    except Exception as exc:
        print(f"PostgreSQL connection failed: {exc}")
        return False
    finally:
        engine.dispose()
