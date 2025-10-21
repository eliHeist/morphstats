import Alpine from "alpinejs";

import './main.scss';
import checklist from './ts/checklist';

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
