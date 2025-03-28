import time
from sqlmodel import create_engine, SQLModel, OperationalError


def initialize_db_schema(rds_endpoint: str, rds_user: str, rds_pass: str, rds_name: str):
    db_url = f"postgresql+psycopg2://{rds_user}:{rds_pass}@{rds_endpoint}/{rds_name}"
    print(f"Attempting connection to: {db_url}")

    max_retries = 5
    for attempt in range(max_retries):
        try:
            engine = create_engine(db_url)
            
            # Test connection
            with engine.connect() as conn:
                print("Successfully connected to database!")
            
            # Create tables
            SQLModel.metadata.create_all(engine)
            print("Shipment tables created successfully!")
            return
        except OperationalError as e:
            if attempt < max_retries - 1:
                wait_time = 10 * (attempt + 1)
                print(f"Connection failed ({e}), retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise RuntimeError(f"Failed to connect after {max_retries} attempts") from e


    