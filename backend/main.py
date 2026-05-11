from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .models import Product, Sale, SalesAnalyzer
import os

app = FastAPI(title="E-Commerce Analysis API")

# Tahlilchini namunaviy ma'lumotlar bilan to'ldiramiz
analyzer = SalesAnalyzer()

# Namunaviy mahsulotlar
p1 = Product(1, "Laptop", "Elektronika", 1000)
p2 = Product(2, "Smartphone", "Elektronika", 700)
p3 = Product(3, "T-shirt", "Kiyim", 20)
p4 = Product(4, "Jacket", "Kiyim", 80)

# Sotuvlar (Yil davomida)
analyzer.add_sale(Sale(p1, 5, "2023-01-10")) # Qish
analyzer.add_sale(Sale(p3, 50, "2023-04-15")) # Bahor
analyzer.add_sale(Sale(p2, 10, "2023-07-20")) # Yoz
analyzer.add_sale(Sale(p4, 15, "2023-10-05")) # Kuz
analyzer.add_sale(Sale(p1, 2, "2023-12-25")) # Qish

@app.get("/api/analysis/monthly")
def get_monthly():
    return analyzer.get_monthly_report()

@app.get("/api/analysis/seasonal")
def get_seasonal():
    return analyzer.get_seasonal_report()

@app.get("/api/analysis/category")
def get_category():
    return analyzer.get_category_report()

# Frontendni ulash
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
