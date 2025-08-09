# Solsphere System Monitor

This project provides a FastAPI backend for collecting and monitoring system status data from multiple machines. It accepts system data via HTTP, stores machine ID, timestamps, and check results, and provides APIs for querying and exporting the data.

## Features

- Accepts system data from the utility (via secure HTTP)
- Stores machine ID, timestamps, and check results
- APIs for:
  - Listing all machines and their latest status
  - Filtering based on OS, issues, etc.
  - Exporting all data as CSV

## Folder Structure

```
solsphere/
│
├── app.py           # FastAPI backend
├── model.py         # SQLAlchemy models
├── database.py      # Database connection setup
├── schemas.py       # Pydantic schemas
├── Utility.py       # Client utility for system checks
└── ...
```

## Requirements

- Python 3.8+
- pip

## Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd solsphere
   ```

2. **Install dependencies:**
   ```sh
   pip install fastapi uvicorn sqlalchemy pydantic requests
   ```

## Running the Backend

1. **(Optional) Remove old SQLite database if you change models:**
   - Delete the `.db` file if present (e.g., `solsphere.db`).

2. **Start the FastAPI server:**
   ```sh
   python app.py
   ```
   In sperate power shell / terminal
   ```sh
   python Utility.py
   ```

3. **API Documentation:**
   - Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API docs.

## API Endpoints

- `POST /api/system-status`  
  Submit system status data.

- `GET /api/system-status`  
  List all statuses (supports filtering by OS and issue).

- `GET /api/system-status/latest`  
  Get the latest status for each machine.

- `GET /api/system-status/{machine_id}`  
  Get all statuses for a specific machine.

- `GET /api/system-status/export/csv`  
  Download all statuses as a CSV file.

## Running the Utility

- Edit and run `Utility.py` on client machines to collect and send system data to the backend.

## Notes

- If you change your models, delete the old database file to avoid schema mismatch errors.
- For production, consider using a more robust database and HTTPS.
- Check System_data file for records, It records every 18 sec

---
