import Alpine from "alpinejs";

import './main.scss';
import checklist from './ts/checklist';
import { renderStatsCharts } from "./ts/chart";

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
    const dataElement = document.getElementById('stats-data') as HTMLScriptElement;
    if (!dataElement) return;

    let rawText = dataElement.textContent || '[]';

    // Replace single quotes with double quotes for valid JSON
    const fixedText = rawText.replace(/'/g, '"');

    const statsList = JSON.parse(fixedText);
    renderStatsCharts(statsList);
});

