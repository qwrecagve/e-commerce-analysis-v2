from collections import defaultdict

class SalesAnalyzer:
    def __init__(self, sales_list):
        self.sales = sales_list

    def analyze_monthly_sales(self):
        """Oylik savdo tahlili"""
        monthly_data = defaultdict(float)
        month_names = {
            1: "Yanvar", 2: "Fevral", 3: "Mart", 4: "Aprel",
            5: "May", 6: "Iyun", 7: "Iyul", 8: "Avgust",
            9: "Sentabr", 10: "Oktabr", 11: "Noyabr", 12: "Dekabr"
        }
        
        for sale in self.sales:
            month = sale.get_month()
            monthly_data[month_names[month]] += sale.total_amount
            
        return dict(monthly_data)

    def analyze_seasonal_sales(self):
        """Mavsumiy savdo tahlili"""
        seasonal_data = defaultdict(float)
        season_names = {
            "Winter": "Qish",
            "Spring": "Bahor",
            "Summer": "Yoz",
            "Autumn": "Kuz"
        }
        
        for sale in self.sales:
            season = sale.get_season()
            seasonal_data[season_names[season]] += sale.total_amount
            
        return dict(seasonal_data)

    def get_top_products(self, n=5):
        """Eng ko'p sotilgan n ta mahsulot"""
        product_sales = defaultdict(float)
        for sale in self.sales:
            product_sales[sale.product.name] += sale.total_amount
            
        # Saralash
        sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
        return sorted_products[:n]
