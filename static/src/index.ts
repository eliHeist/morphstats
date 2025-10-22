import Alpine from "alpinejs";

import './main.scss';
import checklist from './ts/checklist';
import { renderStatsCharts } from "./ts/chart";
import { renderMonthlyAvailabilityChart } from "./ts/facilitator-charts";

Alpine.data('checklist', checklist)

Alpine.start()

// buttons ===================
const loaderButtons = document.querySelectorAll('.load-btn') as NodeListOf<HTMLButtonElement>

loaderButtons.forEach((button: HTMLElement) => {
    const loader = document.createElement('div') as HTMLDivElement
    loader.classList.add('button--loader')
    loader.innerHTML = `<div></div><div></div><div></div>`
    button.appendChild(loader)
});

document.addEventListener('DOMContentLoaded', () => {
    // stats dashboard
    const dataElement = document.getElementById('stats-data') as HTMLScriptElement;
    if (!dataElement) return;
    
    let rawText = dataElement.textContent || '[]';
    
    // Replace single quotes with double quotes for valid JSON
    const fixedText = rawText.replace(/'/g, '"');
    
    const statsList = JSON.parse(fixedText);
    renderStatsCharts(statsList);
});

document.addEventListener('DOMContentLoaded', () => {
    // facilitator detail
    const dataEl = document.getElementById('facilitator-data');
    if (dataEl) {
        
        let fac_data_text = dataEl.textContent || '[]'
        const parsed_data = fac_data_text.replace(/'/g, '"')
        
        const jsonData = JSON.parse(parsed_data || '{}');
        
        const dailyData = jsonData.daily ?? [];
        const monthlyData = jsonData.monthly ?? [];
        
        console.log(dailyData, monthlyData);

        renderMonthlyAvailabilityChart('monthlyAvailabilityChart', monthlyData);
        renderHeatMap(dailyData)
    }
});


function renderHeatMap(dailyData: [{ date: string; status: boolean }]) {
    // Group dates by month
    type MonthMap = Record<string, { date: string; status: boolean }[]>;
    const months: MonthMap = {};

    dailyData.forEach(d => {
        const dateObj = new Date(d.date);
        const monthKey = dateObj.toLocaleString('default', { month: 'short', year: 'numeric' });
        if (!months[monthKey]) months[monthKey] = [];
        months[monthKey].push(d);
    });

    // Sort months chronologically
    const sortedMonthKeys = Object.keys(months).sort((a, b) => {
        const [aMonth, aYear] = a.split(' ');
        const [bMonth, bYear] = b.split(' ');
        const aDate = new Date(`${aMonth} 1, ${aYear}`);
        const bDate = new Date(`${bMonth} 1, ${bYear}`);
        return aDate.getTime() - bDate.getTime();
    });

    const container = document.getElementById('availabilityHeatmap');
    if (!container) throw new Error('Heatmap container not found');

    // Render each month as a column
    sortedMonthKeys.forEach(monthKey => {
        // const monthDiv = document.createElement('div');
        // monthDiv.classList.add('grid', 'gap-1');

        // Month label
        // const monthLabel = document.createElement('div');
        // monthLabel.textContent = monthKey;
        // monthLabel.classList.add('text-center', 'text-xs', 'font-semibold', 'mb-1');
        // monthDiv.appendChild(monthLabel);

        // const cellsDiv = document.createElement('div');
        // cellsDiv.classList.add('grid', 'gap-1');

        // Day cells
        months[monthKey].forEach(d => {
            const cell = document.createElement('div');
            cell.classList.add('aspect-square', 'p-4', 'rounded', 'border', 'border-light');
            cell.title = `${d.date}: ${d.status ? 'Present' : 'Absent'}`;
            cell.style.backgroundColor = d.status ? '#006fff' : '#1a2b3d';
            container.appendChild(cell);
        });

        // monthDiv.appendChild(cellsDiv);

        // container.appendChild(monthDiv);
    });
}

