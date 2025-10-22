import Chart from "chart.js/auto";

interface DailyStat {
    date: string;
    status: boolean;
}

interface MonthlyStat {
    month: string;
    days_present: number;
    total_days: number;
}

const commonOptions = {
    responsive: true,
    tension: 0.4,
    fill: true,
    aspectRatio: 3,
    plugins: {
        legend: {
            labels: {
                color: '#C0D6F2',
                font: { size: 11 }
            }
        }
    },
    scales: {
        x: {
            ticks: { color: '#C0D6F2' },
            grid: { color: 'rgba(255,255,255,0.1)' }
        },
        y: {
            ticks: { color: '#C0D6F2' },
            grid: { color: 'rgba(255,255,255,0.1)' }
        }
    }
};


// Monthly Availability Area Chart
export function renderMonthlyAvailabilityChart(containerId: string, data: Record<string, { month: string; days_present: number }>) {
    // Convert object to sorted array (Jan to Dec)
    const monthsOrder = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const monthArray = monthsOrder.map(month => data[month]);

    const labels = monthArray.map(d => d.month);
    const attendanceData = monthArray.map(d => d.days_present);

    new Chart(document.getElementById(containerId) as HTMLCanvasElement, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Monthly Presence',
                data: attendanceData,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.3)',
                pointRadius: 3,
                pointBackgroundColor: '#3b82f6',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            aspectRatio: 3,
            plugins: {
                legend: { labels: { color: '#C0D6F2', font: { size: 11 } } },
            },
            scales: {
                x: {
                    ticks: { color: '#C0D6F2' },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                },
                y: {
                    ticks: {
                        color: '#C0D6F2',
                        stepSize: 1,
                        callback: (value) => Number.isInteger(value) ? value : null
                    },
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    beginAtZero: true
                }
            }
        }
    });
}


