from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .models import init_db, SalesAnalyzer, get_db_connection
import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

app = FastAPI(title="E-Commerce Analysis Cloud API")

@app.on_event("startup")
def startup_event():
    # 1. Jadvallarni yaratish
    init_db()
    
    # 2. Namunaviy ma'lumotlarni qo'shish (faqat agar bo'sh bo'lsa)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        # Mahsulotlar
        cursor.execute("INSERT INTO products VALUES (1, 'Laptop', 'Elektronika', 1200)")
        cursor.execute("INSERT INTO products VALUES (2, 'Phone', 'Elektronika', 800)")
        cursor.execute("INSERT INTO products VALUES (3, 'T-Shirt', 'Kiyim', 25)")
        # Sotuvlar
        cursor.execute("INSERT INTO sales (product_id, quantity, sale_date, total_amount) VALUES (1, 2, '2023-01-15', 2400)")
        cursor.execute("INSERT INTO sales (product_id, quantity, sale_date, total_amount) VALUES (2, 5, '2023-06-20', 4000)")
        cursor.execute("INSERT INTO sales (product_id, quantity, sale_date, total_amount) VALUES (3, 10, '2023-11-10', 250)")
        conn.commit()
    conn.close()

@app.get("/api/analysis/monthly")
def get_monthly():
    analyzer = SalesAnalyzer()
    return analyzer.get_monthly_report()

@app.get("/api/analysis/seasonal")
def get_seasonal():
    analyzer = SalesAnalyzer()
    return analyzer.get_seasonal_report()

# Frontendni ulash
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
