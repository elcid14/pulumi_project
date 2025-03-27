import time
from models import create_engine, create_tables

def initalize_db_schema(rds_endpoint: str, rds_user:str, rds_pass:str, rds_name:str ):
    
    db_url = f"postgresql://{rds_user}:{rds_pass}@{rds_endpoint}/{rds_name}"
    print(f"Waiting for RDS: {db_url}...")

    # Allow time for DB to be fully available
    time.sleep(60)

    # Connect and create tables
    engine = create_engine(db_url)
    create_tables()
    print("Shipment Tables Created in RDS!")
    