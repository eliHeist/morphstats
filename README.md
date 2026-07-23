```markdown
# MorphStats

[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4+-06B6D4?style=flat&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Django Cotton](https://img.shields.io/badge/Django_Cotton-UI-5865F2?style=flat)](https://django-cotton.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**MorphStats** is a specialized service analytics and team management platform built for **Morph**. It provides real-time tracking of attendance metrics, service demographic trends, facilitator involvement, and team engagement ratios through interactive visual dashboards.

---

## 🚀 Key Features

* **Attendance & Demographic Analytics:**
  * Track weekly attendance segmented across multiple demographics (*Junior, Senior, First-Time Visitors, and Salvations*).
  * Automatically calculates daily averages, peak dates, and lowest-performing services.
* **Facilitator & Shift Tracking:**
  * Monitor individual volunteer participation, active pool ratios, and team shift totals over time.
  * Tag/Role attribution (*Band, Worship, Host*) for granular service breakdown.
  * Volunteer engagement rate tracking to ensure balanced workloads across teams.
* **Interactive Visualizations:**
  * Responsive area charts for attendance trends over time using **Chart.js**.
  * Doughnut charts for gender breakdowns and bar charts for role distribution.
* **Modern UI Component Architecture:**
  * Clean, modular design built using **Django Cotton (`c-ui`)** components.
  * Fluid container-query layout built with **Tailwind CSS** and **Alpine.js**.

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Component Architecture:** Django Cotton (`django-cotton`)
* **Frontend Reactivity:** Alpine.js, TypeScript
* **Styling:** Tailwind CSS (with `@container` query plugin)
* **Data Visualization:** Chart.js
* **Database:** SQLite / PostgreSQL

---

## 🚦 Getting Started

### Prerequisites

* Python 3.10+
* Node.js & npm (for compiling TypeScript and Tailwind CSS assets)

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/eliHeist/morphstats.git](https://github.com/eliHeist/morphstats.git)
   cd morphstats

```

2. **Set up a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```


3. **Install Python dependencies:**
```bash
pip install -r requirements.txt

```


4. **Install Node dependencies:**
```bash
npm install

```


5. **Run migrations and build assets:**
```bash
python manage.py migrate
npm run build  # or your respective frontend build script

```


6. **Create a superuser and launch the dev server:**
```bash
python manage.py createsuperuser
python manage.py runserver

```



Visit `http://127.0.0.1:8000/` in your browser.

---

## 👨‍💻 Developer & Author

**Elijah Triumph Angengeun** (`@eliHeist`)

*Full-stack developer & system architect building modular backends and modern web applications.*

*Founder & Developer at [Dakdot](https://dakdot.com).*

* **Website:** [dakdot.com](https://dakdot.com)
* **GitHub:** [@eliHeist](https://github.com/eliHeist)
* **LinkedIn:** [Elijah Triumph Angengeun](https://www.linkedin.com/in/eliheist/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```

```