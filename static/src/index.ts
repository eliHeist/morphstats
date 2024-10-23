import Alpine from "alpinejs";

import './main.scss';
import checklist from './ts/checklist';

Alpine.data('checklist', checklist)

Alpine.start()
