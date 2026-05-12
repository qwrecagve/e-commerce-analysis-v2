async function initDashboard() {
    try {
        // 1. Oylik ma'lumotlarni olish
        const monthlyRes = await fetch('/api/analysis/monthly');
        const monthlyData = await monthlyRes.json();

        // 2. Mavsumiy ma'lumotlarni olish
        const seasonalRes = await fetch('/api/analysis/seasonal');
        const seasonalData = await seasonalRes.json();

        // --- Statistikalarni yangilash ---
        const totalRev = Object.values(monthlyData).reduce((a, b) => a + b, 0);
        document.getElementById('total-revenue').innerText = `$${totalRev.toLocaleString()}`;
        
        const topSeason = Object.entries(seasonalData).reduce((a, b) => a[1] > b[1] ? a : b)[0];
        document.getElementById('top-season').innerText = topSeason;

        // --- Oylik Grafik ---
        const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
        new Chart(monthlyCtx, {
            type: 'line',
            data: {
                labels: Object.keys(monthlyData),
                datasets: [{
                    label: 'Tushum ($)',
                    data: Object.values(monthlyData),
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.2)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#fff',
                    pointBorderWidth: 3
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { grid: { display: false } }
                }
            }
        });

        // --- Mavsumiy Grafik ---
        const seasonalCtx = document.getElementById('seasonalChart').getContext('2d');
        new Chart(seasonalCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(seasonalData),
                datasets: [{
                    label: 'Mavsumiy Sotuv ($)',
                    data: Object.values(seasonalData),
                    backgroundColor: [
                        '#60a5fa', // Qish
                        '#4ade80', // Bahor
                        '#facc15', // Yoz
                        '#fb923c'  // Kuz
                    ],
                    borderRadius: 10
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } }
            }
        });

    } catch (e) {
        console.error("Dashboard yuklashda xatolik:", e);
    }
}

// Sahifa yuklanganda ishga tushadi
window.onload = initDashboard;
