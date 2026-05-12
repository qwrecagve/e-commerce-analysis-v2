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

@app.get("/api/summary")
def get_summary():
    try:
        analyzer = SalesAnalyzer()
        monthly = analyzer.get_monthly_report()
        seasonal = analyzer.get_seasonal_report()
        
        # Umumiy tushum
        total_revenue = sum(monthly.values())
        
        # Eng yaxshi mavsum
        top_season = max(seasonal, key=seasonal.get) if seasonal else "Noma'lum"
        
        return {
            "total_revenue": total_revenue,
            "total_sales": len(analyzer.sales),
            "top_season": top_season,
            "monthly_data": monthly,
            "seasonal_data": seasonal
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
