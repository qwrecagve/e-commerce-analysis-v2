'use client';
import { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface DashboardData {
  total_revenue: number;
  total_sales: number;
  top_season: string;
  monthly_data: Record<string, number>;
  seasonal_data: Record<string, number>;
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/summary')
      .then(res => res.json())
      .then(setData)
      .catch(err => console.error('API Error:', err));
  }, []);

  if (!data) return <div className="loading">Ma'lumotlar yuklanmoqda...</div>;

  const monthlyChartData = {
    labels: Object.keys(data.monthly_data),
    datasets: [
      {
        label: 'Oylik Savdo ($)',
        data: Object.values(data.monthly_data),
        backgroundColor: '#3b82f6',
        borderRadius: 8,
      },
    ],
  };

  const seasonalChartData = {
    labels: Object.keys(data.seasonal_data),
    datasets: [
      {
        label: 'Mavsumiy Savdo',
        data: Object.values(data.seasonal_data),
        backgroundColor: ['#f87171', '#4ade80', '#fbbf24', '#60a5fa'],
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 2,
      },
    ],
  };

  return (
    <div className="glass-container">
      <header className="dashboard-header">
        <div>
          <h1>📊 E-Commerce Analytics</h1>
          <p>Azure SQL ma'lumotlar bazasi asosida</p>
        </div>
        <div className="status-badge">Online</div>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Umumiy Tushum</h3>
          <p className="stat-value">${data.total_revenue.toLocaleString()}</p>
        </div>
        <div className="stat-card">
          <h3>Sotilgan Mahsulotlar</h3>
          <p className="stat-value">{data.total_sales}</p>
        </div>
        <div className="stat-card">
          <h3>Eng Faol Mavsum</h3>
          <p className="stat-value">{data.top_season}</p>
        </div>
      </div>

      <div className="charts-container">
        <div className="chart-box">
          <h3>📅 Oylik Savdo Dinamikasi</h3>
          <Bar data={monthlyChartData} options={{ responsive: true, plugins: { legend: { display: false } } }} />
        </div>
        <div className="chart-box">
          <h3>🍂 Mavsumiy Tahlil</h3>
          <Pie data={seasonalChartData} />
        </div>
      </div>
    </div>
  );
}
