from fastapi import FastAPI, Depends, Query, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from database import Base, engine, SessionLocal
from model import SystemStatus
from schemas import SystemStatusCreate, SystemStatusOut
from datetime import datetime
import csv
from io import StringIO

Base.metadata.create_all(bind=engine)

app = FastAPI(title="System Monitor API")

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/system-status", response_model=SystemStatusOut)
def create_status(status: SystemStatusCreate, db: Session = Depends(get_db)):
    db_status = SystemStatus(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

@app.get("/api/system-status", response_model=List[SystemStatusOut])
def get_all_statuses(
    os: Optional[str] = Query(None),
    issue: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(SystemStatus)
    if os:
        query = query.filter(SystemStatus.os == os)
    if issue:
        if issue == "disk_encryption":
            query = query.filter(SystemStatus.disk_encryption == False)
        elif issue == "antivirus":
            query = query.filter(SystemStatus.antivirus == False)
        elif issue == "sleep_ok":
            query = query.filter(SystemStatus.sleep_ok == False)
        elif issue == "os_update":
            query = query.filter(SystemStatus.os_update["update_needed"].as_boolean() == True)
    return query.all()

@app.get("/api/system-status/latest", response_model=List[SystemStatusOut])
def get_latest_statuses(db: Session = Depends(get_db)):
    # Get latest status for each machine_id
    subq = (
        db.query(
            SystemStatus.machine_id,
            func.max(SystemStatus.timestamp).label("max_ts")
        ).group_by(SystemStatus.machine_id).subquery()
    )
    latest = (
        db.query(SystemStatus)
        .join(subq, (SystemStatus.machine_id == subq.c.machine_id) & (SystemStatus.timestamp == subq.c.max_ts))
        .all()
    )
    return latest

@app.get("/api/system-status/{machine_id}", response_model=List[SystemStatusOut])
def get_machine_status(machine_id: str, db: Session = Depends(get_db)):
    return db.query(SystemStatus).filter(SystemStatus.machine_id == machine_id).all()

@app.get("/api/system-status/export/csv")
def export_csv(db: Session = Depends(get_db)):
    statuses = db.query(SystemStatus).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "machine_id", "os", "disk_encryption", "os_update", "antivirus", "sleep_ok", "timestamp"])
    for s in statuses:
        writer.writerow([
            s.id, s.machine_id, s.os, s.disk_encryption, s.os_update, s.antivirus, s.sleep_ok, s.timestamp
        ])
    output.seek(0)
    return Response(
        content=output.read(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=system_status.csv"}
    )

# Install command (to be run in terminal, not in the script):
# pip install fastapi uvicorn

# To run the app with auto-reload, use the following command in the terminal:
# python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

