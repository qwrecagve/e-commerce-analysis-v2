from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import SalesAnalyzer, init_db
import uvicorn

app = FastAPI(title="E-commerce Analysis API")

# CORS sozlamalari (Frontend ulanishi uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    # Jadvallarni tekshirish/yaratish
    init_db()
    print("Backend muvaffaqiyatli ishga tushdi.")

@app.get("/api/summary")
def get_summary():
    try:
        analyzer = SalesAnalyzer()
        # Agar baza bo'sh bo'lsa, namunaviy ma'lumotlar qo'shish (ixtiyoriy)
        if not analyzer.sales:
            print("Ma'lumotlar topilmadi. Bazaga test ma'lumotlari kiritilmoqda...")
            seed_db()
            analyzer.init_data()

        monthly = analyzer.get_monthly_report()
        seasonal = analyzer.get_seasonal_report()
        
        return {
            "total_revenue": sum(monthly.values()),
            "total_sales": len(analyzer.sales),
            "top_season": max(seasonal, key=seasonal.get) if seasonal else "Noma'lum",
            "monthly_data": monthly,
            "seasonal_data": seasonal
        }
    except Exception as e:
        print(f"Xatolik: {str(e)}")
        raise HTTPException(status_code=500, detail="Ma'lumotlar bazasi bilan ulanishda xatolik yuz berdi.")

def seed_db():
    """Bazani test ma'lumotlari bilan to'ldirish"""
    from models import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Test mahsulotlar
    products = [
        (1, 'Laptop Pro', 'Electronics', 1200.0),
        (2, 'Smartphone X', 'Electronics', 800.0),
        (3, 'Wireless Headphones', 'Accessories', 150.0)
    ]
    
    for p in products:
        try:
            cursor.execute("INSERT INTO products (product_id, name, category, price) VALUES (?, ?, ?, ?)", p)
        except: pass # Allaqachon bo'lsa o'tkazib yuboramiz

    # Test sotuvlar (turli oylar uchun)
    sales = [
        (1, 2, '2024-01-15', 2400.0),
        (2, 5, '2024-03-20', 4000.0),
        (3, 10, '2024-06-10', 1500.0),
        (1, 1, '2024-12-25', 1200.0)
    ]
    
    for s in sales:
        cursor.execute("INSERT INTO sales (product_id, quantity, sale_date, total_amount) VALUES (?, ?, ?, ?)", s)
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
