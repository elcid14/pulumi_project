import os
import json
import psycopg2
from redis import Redis
from celery import Celery, states
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Shipment  # SQLAlchemy model

BROKER_URL = os.getenv("CELERY_BROKER_URL")  
BACKEND_URL = os.getenv("CELERY_BACKEND_URL")  
DATABASE_URL = os.getenv("DATABASE_URL") 

# Initialize Celery with Redis backend to track state
app = Celery(
    "tasks",
    broker=BROKER_URL,
    backend=BACKEND_URL
)

# Redis Client for storing task states
redis_client = Redis.from_url(BACKEND_URL)

# PostgreSQL Connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@app.task(bind=True)
def process_shipment(self, data):
    """
    Process shipment data:
    1. Store task state in Redis.
    2. Persist shipment status in PostgreSQL (RDS).
    """
    shipment_id = data["shipment_id"]
    task_id = self.request.id  #this is the task id

    # Store task state in Redis, first status is pending
    redis_client.set(f"task:{task_id}", json.dumps({"state": states.PENDING, "shipment_id": shipment_id}))
    print(f" Task {task_id} pending for shipment {shipment_id}")

    try:
        # store for caching
        redis_client.set(f"shipment:{shipment_id}", json.dumps(data))
        print(f"Stored in Redis: shipment:{shipment_id}")

        # Step 2: Persist final shipment status in PostgreSQL (RDS)
        session = SessionLocal()
        shipment = session.query(Shipment).filter_by(shipment_id=shipment_id).first()
        
        if shipment:
            # Update existing shipment record
            shipment.status = data["status"]
            shipment.location = data["location"]
        else:
            # Create new shipment record
            shipment = Shipment(
                shipment_id=shipment_id,
                status=data["status"],
                location=data["location"]
            )
            session.add(shipment)

        session.commit()
        print(f"Saved to RDS: shipment {shipment_id}")

        # Update task state in Redis to SUCCESS
        redis_client.set(f"task:{task_id}", json.dumps({"state": states.SUCCESS, "shipment_id": shipment_id}))

    except Exception as e:
        session.rollback()
        print(f" Error saving to RDS: {e}")

        # Update task state in Redis to FAILURE
        redis_client.set(f"task:{task_id}", json.dumps({"state": states.FAILURE, "error": str(e)}))

    finally:
        session.close()

    return {"status": "processed", "shipment_id": shipment_id, "task_id": task_id}

