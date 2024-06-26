from django.templatetags.static import static

UNFOLD = {
    "SITE_TITLE": 'Stats App Admin',
    "SITE_HEADER": 'Stats App',
    "SITE_ICON": lambda request: static("assets/logo.png"),
    # "SITE_LOGO": lambda request: static("assets/app icon@.5x.png"),
    "COLORS": {
        'primary': {
            '50': '#edf9ff',
            '100': '#d6f0ff',
            '200': '#b5e7ff',
            '300': '#83d9ff',
            '400': '#48c3ff',
            '500': '#1ea2ff',
            '600': '#0683ff',
            '700': '#006fff',
            '800': '#0855c5',
            '900': '#0d4b9b',
            '950': '#0e2e5d',
        },
    },
    "STYLES": [
        lambda request: static("css/style.css"),
    ],
    
}
