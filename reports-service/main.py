from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # ← добавьте этот импорт
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from clickhouse_driver import Client
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

KEYCLOAK_URL = "http://keycloak:8080"
REALM = "reports-realm"

def get_user_id(token: str) -> str:
    """Извлекает user_id (sub) из JWT токена БЕЗ вызова Keycloak"""
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload["sub"]
    except Exception as e:
        logger.error(f"Token decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/reports")
def get_report(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = get_user_id(token)

    client = Client(host='clickhouse')
    try:
        rows = client.execute(
            """
            SELECT user_id, report_date, total_actions, avg_latency_ms
            FROM reports.user_reports
            WHERE user_id = %(user_id)s
            ORDER BY report_date DESC
            LIMIT 1
            """,
            {"user_id": user_id}
        )
        if not rows:
            raise HTTPException(status_code=404, detail="Report not found")

        row = rows[0]
        return {
            "user_id": row[0],
            "report_date": row[1].isoformat(),
            "total_actions": row[2],
            "avg_latency_ms": float(row[3])
        }
    except Exception as e:
        logger.error(f"ClickHouse error: {e}")
        raise HTTPException(status_code=500, detail="Report service unavailable")