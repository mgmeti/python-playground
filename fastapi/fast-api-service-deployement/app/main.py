from fastapi import FastAPI
import os
import psycopg2

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/dbtest")
def db_test():
    try:
        conn = psycopg2.connect(
            host = os.getenv("DB_HOST", "db"),
            database = os.getenv("DB_NAME", "dbtest"),
            user = os.getenv("DB_USER", "postgres"),
            password = os.getenv("DB_PASSWORD", "postgres")
        )
        conn.close()
        return {"status": "ok", "db": "connected"}
    
    except Exception as e:
        return {"status": "error", "message": str(e), "db": "not connected"}
