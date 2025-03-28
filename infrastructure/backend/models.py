import datetime
import os
from sqlmodel import Field,SQLModel, create_engine, Session

class Shipment(SQLModel, tabel=True):
    """
    Defines model for a shipment data
    """
    id: str = Field(default=None, primary_key=True)
    container_number: str
    customer_id: str
    msl: str
    status: str
    shipping_line: str
    vessel: str
    port_of_deaprture: str
    port_of_arrival: str
    ship_date: str
    arrival_date: str
    notes: str
    current_location:str
    weight: float
    

    
DATABASE_URL = os.getenv("DATABASE_URL")

# Create Engine
engine = create_engine(DATABASE_URL)

# Function to create tables
def create_tables():
    SQLModel.metadata.create_all(engine)

# Create Session factory
def get_session():
    return Session(engine)