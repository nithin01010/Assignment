from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class SystemStatusBase(BaseModel):
    machine_id: str
    os: str
    disk_encryption: bool
    os_update: Dict
    antivirus: bool
    sleep_ok: bool
    timestamp: datetime

class SystemStatusCreate(SystemStatusBase):
    pass

class SystemStatusOut(BaseModel):
    machine_id: str
    os: str
    disk_encryption: bool
    os_update: Dict
    antivirus: bool
    sleep_ok: bool
    timestamp: datetime

    class Config:
        from_attributes = True
