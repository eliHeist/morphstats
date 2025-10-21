import Chart from 'chart.js/auto';

export function renderStatsCharts(statsList: [string, number, number][]) {
    // Extract labels and data
    const labels = statsList.slice(1).map(item => item[0]);
    const attendanceData = statsList.slice(1).map(item => item[1]);
    const facilitatorsData = statsList.slice(1).map(item => item[2]);

    // Common chart options
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

    // Attendance Area Chart
    const attendanceCanvas = document.getElementById('attendanceAreaChart') as HTMLCanvasElement;
    if (attendanceCanvas) {
        new Chart(attendanceCanvas, {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'Attendance',
                    data: attendanceData,
                    borderColor: '#006FFF',
                    backgroundColor: 'rgba(0, 111, 255, 0.3)',
                    pointRadius: 3,
                    pointBackgroundColor: '#006FFF'
                }]
            },
            options: commonOptions
        });
    }

    // Facilitators Area Chart
    const facilitatorsCanvas = document.getElementById('facilitatorsAreaChart') as HTMLCanvasElement;
    if (facilitatorsCanvas) {
        new Chart(facilitatorsCanvas, {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'Facilitators',
                    data: facilitatorsData,
                    borderColor: '#FFB300',
                    backgroundColor: 'rgba(255, 179, 0, 0.3)',
                    pointRadius: 3,
                    pointBackgroundColor: '#FFB300'
                }]
            },
            options: commonOptions
        });
    }
}
