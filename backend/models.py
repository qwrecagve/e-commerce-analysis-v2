from datetime import datetime
from typing import List, Dict

class Product:
    """Mahsulot modeli"""
    def __init__(self, product_id: int, name: str, category: str, price: float):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price

class Sale:
    """Sotuv tranzaksiyasi modeli"""
    def __init__(self, product: Product, quantity: int, sale_date: str):
        self.product = product
        self.quantity = quantity
        self.sale_date = datetime.strptime(sale_date, "%Y-%m-%d")
        self.total_amount = product.price * quantity

class SalesAnalyzer:
    """Savdo ma'lumotlarini tahlil qiluvchi OOP klassi"""
    def __init__(self):
        self.sales: List[Sale] = []

    def add_sale(self, sale: Sale):
        self.sales.append(sale)

    def get_monthly_report(self) -> Dict[str, float]:
        """Oylik tushum tahlili"""
        report = {}
        for sale in self.sales:
            month = sale.sale_date.strftime("%Y-%m")
            report[month] = report.get(month, 0) + sale.total_amount
        return report

    def get_seasonal_report(self) -> Dict[str, float]:
        """Mavsumiy tushum tahlili"""
        seasons = {
            "Qish": [12, 1, 2],
            "Bahor": [3, 4, 5],
            "Yoz": [6, 7, 8],
            "Kuz": [9, 10, 11]
        }
        report = {"Qish": 0, "Bahor": 0, "Yoz": 0, "Kuz": 0}
        
        for sale in self.sales:
            month = sale.sale_date.month
            for season_name, months in seasons.items():
                if month in months:
                    report[season_name] += sale.total_amount
        return report

    def get_category_report(self) -> Dict[str, float]:
        """Kategoriyalar bo'yicha tahlil"""
        report = {}
        for sale in self.sales:
            cat = sale.product.category
            report[cat] = report.get(cat, 0) + sale.total_amount
        return report
