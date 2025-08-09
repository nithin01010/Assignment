from sqlalchemy import Column, String, Boolean, DateTime, JSON
from datetime import datetime
from database import Base
import uuid  # Import uuid module

# Define the SystemStatus model
# This model represents the system status data to be stored in the database
# I am storing every POS data in the database
# The id field is a unique identifier for each record, generated as a UUID

class SystemStatus(Base):
    __tablename__ = "system_status"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    machine_id = Column(String, index=True)  # No unique=True here
    os = Column(String)
    disk_encryption = Column(Boolean)
    os_update = Column(JSON)
    antivirus = Column(Boolean)
    sleep_ok = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)