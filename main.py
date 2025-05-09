from fastapi import FastAPI, Request
from pydantic import BaseModel
from database import engine
import sqlalchemy
import time
from datetime import datetime
import os
import logging
# Setup file logger
os.makedirs("logs", exist_ok=True)
log_file = "logs/query.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

app = FastAPI()

class QueryRequest(BaseModel):
    sql: str

@app.post("/query")
async def run_query(request: QueryRequest):
    DANGEROUS_KEYWORDS = ["DROP", "DELETE", "TRUNCATE", "ALTER", "UPDATE", "RENAME", "CREATE"]

    sql_upper = request.sql.upper().strip()
    if any(keyword in sql_upper for keyword in DANGEROUS_KEYWORDS):
        logging.warning(f"❌ BLOCKED: Dangerous query attempted → {request.sql}")
        return {
            "status": "blocked",
            "message": "This query contains restricted keywords and was blocked for safety."
        }

    try:
        start = time.time()
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text(request.sql))
            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result]
        end = time.time()
        duration_ms = round((end - start) * 1000, 2)
        logging.info(f"SQL: {request.sql} | Duration: {duration_ms}ms")
        return {
            "status": "success",
            "execution_time_ms": duration_ms,
            "data": rows
        }

    except Exception as e:
        logging.error(f"❌ ERROR: {request.sql} → {e}")
        return {"status": "error", "message": str(e)}



