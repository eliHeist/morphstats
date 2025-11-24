# Morphstats

Morphstats tracks stats for Morph teams and events. You view activity, record data, and monitor performance from one dashboard.

## Features

- Track events and attendance.
- Record facilitator activity.
- View totals and trends in the dashboard.
- Access data through API endpoints.
- Manage data through a clean UI.

## Tech Stack

- Python for the backend.
- TypeScript for the frontend.
- HTML templates.
- SCSS for styling.

## Structure

- `api` contains endpoints for data.
- `dashboard` contains pages for summaries.
- `events` manages event data.
- `facilitators` manages facilitator data.
- `stat` contains logic for stats.
- `static` contains assets.
- `templates` contains HTML.

## Setup

1. Clone the repo.
2. Create a virtual environment.
3. Install dependencies.
4. Set environment variables.
5. Run the server.

Example:

```bash
git clone https://github.com/eliHeist/morphstats
cd morphstats
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

## Development
The app runs 2 servers when developing, the main Django server and a webpack server for static files.

### Apps
1. The App app has all the views apart from the dashboard view
1. Dashboard view is in the dashboard app

### Static Files
1. Static files are in the `/static` dir.
1. They are compiled to the `public` folder using webpack.
1. Uses TypeScript for scripts and SCSS with tailwind for styles

## License
MIT License.