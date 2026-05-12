import pyodbc
import os
import sqlite3
from datetime import datetime
from typing import List, Dict

# Muhitni aniqlash
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

def get_db_connection():
    """Ma'lumotlar bazasiga ulanishni ta'minlaydi"""
    if ENVIRONMENT == "production":
        conn_str = os.getenv("AZURE_SQL_CONNECTIONSTRING")
        if not conn_str:
            raise Exception("Azure SQL Connection String topilmadi!")
        # pyodbc uchun parametrlarni moslashtirish
        conn_str = conn_str.replace("Encrypt=True", "Encrypt=yes")
        return pyodbc.connect(conn_str)
    
    # Mahalliy uchun SQLite
    conn = sqlite3.connect("local_sales.db")
    conn.row_factory = sqlite3.Row
    return conn

class Product:
    def __init__(self, product_id: int, name: str, category: str, price: float):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price

class Sale:
    def __init__(self, product: Product, quantity: int, sale_date: str):
        self.product = product
        self.quantity = quantity
        self.sale_date = datetime.strptime(sale_date, "%Y-%m-%d")
        self.total_amount = product.price * quantity

def init_db():
    """Jadvallarni yaratish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if ENVIRONMENT == "production":
        # Azure SQL uchun
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'products')
            CREATE TABLE products (
                product_id INT PRIMARY KEY,
                name NVARCHAR(200),
                category NVARCHAR(100),
                price FLOAT
            )
        ''')
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'sales')
            CREATE TABLE sales (
                sale_id INT PRIMARY KEY IDENTITY(1,1),
                product_id INT,
                quantity INT,
                sale_date NVARCHAR(50),
                total_amount FLOAT
            )
        ''')
    else:
        # SQLite uchun
        cursor.execute('CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)')
        cursor.execute('CREATE TABLE IF NOT EXISTS sales (sale_id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, quantity INTEGER, sale_date TEXT, total_amount REAL)')
    
    conn.commit()
    conn.close()

class SalesAnalyzer:
    """Ma'lumotlarni bazadan olib tahlil qiluvchi klass"""
    def __init__(self):
        self.init_data()

    def init_data(self):
        """Bazadan barcha sotuvlarni yuklab oladi"""
        self.sales: List[Sale] = []
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT s.quantity, s.sale_date, p.product_id, p.name, p.category, p.price 
            FROM sales s 
            JOIN products p ON s.product_id = p.product_id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for row in rows:
            prod = Product(row[2], row[3], row[4], row[5])
            self.sales.append(Sale(prod, row[0], row[1]))
        
        conn.close()

    def get_monthly_report(self) -> Dict[str, float]:
        report = {}
        for sale in self.sales:
            month = sale.sale_date.strftime("%Y-%m")
            report[month] = report.get(month, 0) + sale.total_amount
        return report

    def get_seasonal_report(self) -> Dict[str, float]:
        seasons = {"Qish": [12, 1, 2], "Bahor": [3, 4, 5], "Yoz": [6, 7, 8], "Kuz": [9, 10, 11]}
        report = {"Qish": 0, "Bahor": 0, "Yoz": 0, "Kuz": 0}
        for sale in self.sales:
            m = sale.sale_date.month
            for s_name, months in seasons.items():
                if m in months: report[s_name] += sale.total_amount
        return report
