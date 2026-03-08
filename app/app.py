import os
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "devopsdb")
DB_USER = os.getenv("DB_USER", "devopsuser")
DB_PASS = os.getenv("DB_PASS", "devopspass")

def get_conn():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

@app.get("/")
def home():
    return "✅ Auto-deployed by GitHub Actions CI/CD!"

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/db-check")
def db_check():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits(id SERIAL PRIMARY KEY, created_at TIMESTAMP DEFAULT NOW());")
    cur.execute("INSERT INTO visits DEFAULT VALUES;")
    cur.execute("SELECT COUNT(*) FROM visits;")
    count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(message="DB connected ✅", total_visits=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
