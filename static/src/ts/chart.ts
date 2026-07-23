import Chart from 'chart.js/auto';

document.addEventListener('DOMContentLoaded', () => {
    // 1. Parse Attendance & Facilitator Timeline Data
    const statsDataElem = document.getElementById('stats-data') as HTMLScriptElement;
    if (statsDataElem) {
        try {
            const rawText = statsDataElem.textContent || '[]';
            const statsList = JSON.parse(rawText.replace(/'/g, '"'));
            renderLineCharts(statsList);
        } catch (e) {
            console.error('Error parsing stats-data:', e);
        }
    }

    // 2. Parse Gender Demographics Data
    const demoDataElem = document.getElementById('demographics-data') as HTMLScriptElement;
    if (demoDataElem && demoDataElem.textContent) {
        try {
            const demoData = JSON.parse(demoDataElem.textContent);
            renderGenderChart(demoData);
        } catch (e) {
            console.error('Error parsing demographics-data:', e);
        }
    }

    // 3. Parse Tag Distribution Data
    const tagsDataElem = document.getElementById('tags-data') as HTMLScriptElement;
    if (tagsDataElem && tagsDataElem.textContent) {
        try {
            const tagsData = JSON.parse(tagsDataElem.textContent);
            renderTagsChart(tagsData);
        } catch (e) {
            console.error('Error parsing tags-data:', e);
        }
    }
});

function renderLineCharts(statsList: [string, number, number][]) {
    const labels = statsList.slice(1).map(item => item[0]);
    const attendanceData = statsList.slice(1).map(item => item[1]);
    const facilitatorsData = statsList.slice(1).map(item => item[2]);

    const commonOptions = {
        responsive: true,
        tension: 0.4,
        fill: true,
        aspectRatio: 3,
        plugins: {
            legend: { labels: { color: '#C0D6F2', font: { size: 11 } } }
        },
        scales: {
            x: { ticks: { color: '#C0D6F2' }, grid: { color: 'rgba(255,255,255,0.1)' } },
            y: { ticks: { color: '#C0D6F2' }, grid: { color: 'rgba(255,255,255,0.1)' } }
        }
    };

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
                }]
            },
            options: commonOptions
        });
    }

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
                }]
            },
            options: commonOptions
        });
    }
}

function renderGenderChart(demoData: { male: number; female: number; unspecified: number }) {
    const canvas = document.getElementById('genderPieChart') as HTMLCanvasElement;
    if (!canvas) return;

    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: ['Male', 'Female', 'Unspecified'],
            datasets: [{
                data: [demoData.male, demoData.female, demoData.unspecified],
                backgroundColor: ['#3B82F6', '#EC4899', '#6B7280'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: '#C0D6F2' } }
            }
        }
    });
}

function renderTagsChart(tagsData: Record<string, number>) {
    const canvas = document.getElementById('tagsBarChart') as HTMLCanvasElement;
    if (!canvas) return;

    const labels = Object.keys(tagsData);
    const dataValues = Object.values(tagsData);

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Serving Instances',
                data: dataValues,
                backgroundColor: 'rgba(168, 85, 247, 0.6)',
                borderColor: '#A855F7',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: '#C0D6F2' } }
            },
            scales: {
                x: { ticks: { color: '#C0D6F2' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                y: { ticks: { color: '#C0D6F2' }, grid: { color: 'rgba(255,255,255,0.1)' } }
            }
        }
    });
}