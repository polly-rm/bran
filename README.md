# Bran
 
A Django website for a UK same-day courier and logistics business (Bran Logistics). Visitors can read about the services and fleet, estimate a delivery price from two postcodes, and send a detailed quote request. The business receives every request by email and each customer gets an automatic reply.
 
## Features
 
- **Marketing site** - home page with services, fleet, FAQ, gallery and contact form, plus a dedicated *Same Day Delivery* page.
- **Price calculator** - the visitor enters a collection and a delivery postcode. The driving distance is fetched from the Google Distance Matrix API, and a price (net and with 20% VAT) is shown for each vehicle type.
- **Quote request** - a form with collection/delivery details, preferred time windows and a dynamic list of parcels (count, weight, dimensions). The selected vehicle and price from the calculator are carried over through the session.
- **Email notifications** - contact messages, quote requests and calculator searches are emailed to the admin, customers get an automatic answer, and sent messages are logged in the database (`SendEmail` model).
- **User accounts** - custom user model with email login, registration with email activation, password reset and password change.
- **Spam protection** - Google reCAPTCHA v2, a hidden honeypot field, a minimum-time-to-submit check and per-IP rate limiting (`django-ratelimit`).
- **Google Places autocomplete** proxy endpoint for address/postcode fields.
- **SEO and compliance** - `sitemap.xml`, `robots.txt`, cookie consent banner and a cookies policy page (Django flatpages).
- **Error monitoring** with Sentry.

## Tech stack
 
| Area | Technology |
| --- | --- |
| Backend | Python, Django 4.2 |
| Database | PostgreSQL (`psycopg2`) |
| Frontend | Django templates, Bootstrap 5, Bootstrap Icons, AOS, Tempus Dominus date picker, Cookie Consent |
| Integrations | Google Maps (Distance Matrix and Places), reCAPTCHA, SMTP email, Sentry |
| Other libraries | `django-ckeditor`, `django-recaptcha`, `django-ratelimit`, `python-dotenv`, `qrcode`, `Pillow`, `requests` |
 
## Project structure
 
```
bran/
├── manage.py
├── requirements.txt        # Python dependencies
├── package.json            # Frontend dependencies (npm / yarn)
├── sample.env              # Template for environment variables
├── robots.txt
├── assets/                 # CSS, JS, images and vendor libraries
├── templates/              # Pages, partials, email and user templates
└── bran/                   # Django project package
    ├── settings.py
    ├── urls.py
    ├── base/               # Home, calculator, emails, forms, price template tags
    ├── quotes/             # Quote request form and parcel formset
    ├── users/              # Custom user, authentication, activation, password reset
    └── pages/              # Placeholder app for static pages
```
 
## Getting started
 
### Prerequisites
 
- Python 3.10 or newer
- PostgreSQL
- Node.js with npm or yarn (the frontend libraries are served from `node_modules`)
- A Google Maps API key (Distance Matrix and Places) and reCAPTCHA v2 keys
### Installation
 
```bash
git clone https://github.com/polly-rm/bran.git
cd bran
 
# Python environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
 
# Frontend dependencies
npm install                      # or: yarn install
 
# Configuration
cp sample.env .env
```
 
### Configuration
 
Fill in `.env`. The variables below are read by `bran/settings.py`.
 
| Variable | Description |
| --- | --- |
| `SECRET_KEY` | Django secret key |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | PostgreSQL connection |
| `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_PORT`, `EMAIL_USE_TLS` | Outgoing email (SMTP) |
| `DEFAULT_FROM_EMAIL` | Sender and admin recipient address (defaults to `EMAIL_HOST_USER`) |
| `RECAPTCHA_PUBLIC_KEY`, `RECAPTCHA_PRIVATE_KEY` | Google reCAPTCHA v2 keys |
| `CURRENT_DOMAIN` | Public base URL, used in activation emails and the QR code |
| `GOOGLE_MAPS_API_KEY` | Places autocomplete (and the Maps script on the front end) |
| `GOOGLE_MAPS_DISTANCE_API_KEY` | Distance Matrix API used by the calculator |
| `SENTRY_DSN` | Sentry project DSN |
 
`GOOGLE_MAPS_API_KEY`, `GOOGLE_MAPS_DISTANCE_API_KEY`, `DEFAULT_FROM_EMAIL` and `SENTRY_DSN` are used by the code but are not listed in `sample.env` yet.
 
### Database and run
 
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
 
Then open <http://127.0.0.1:8000/>.
 
### Development notes
 
- `DEBUG` is hard-coded to `False` in `settings.py`, so the `DEBUG` entry in `sample.env` has no effect. Change it locally while developing; otherwise static files will not be served by `runserver`.
- `ALLOWED_HOSTS` is `['*']`, `CSRF_COOKIE_SECURE` is `True` and `CSRF_TRUSTED_ORIGINS` lists the production domain. Adjust these for your own environment.
- Before deploying, run `python manage.py collectstatic` (static files are collected into `static/`).

## Pages and endpoints
 
| URL | Description |
| --- | --- |
| `/` | Home page with contact form and calculator form |
| `/same-day-delivery/` | Same-day delivery information page |
| `/calculator/` | Vehicle options with prices for the entered route |
| `/quote/` | Quote request form |
| `/users/register/`, `/users/login/`, `/users/logout/` | Registration and authentication (in progress) |
| `/users/password-reset/`, `/users/password-update/` | Password reset and change (in progress) |
| `/users/activate/<uidb64>/<token>/` | Email account activation (in progress) |
| `/cookies-policy/` | Cookies policy (flatpage) |
| `/api/autocomplete/` | Google Places autocomplete proxy |
| `/qr-code/` | QR code that links to the site |
| `/sitemap.xml`, `/robots.txt` | SEO files |
| `/admin/` | Django admin |
 
## How pricing works
 
Prices are defined in `bran/base/templatetags/calculate_price.py` for six vehicle types: small van, SWB, MWB, LWB, XLWB and Luton van.
 
- Routes up to 60 miles use a fixed price that increases in steps (20, 30, 40, 50 and 60 mile bands).
- Routes over 60 miles are charged per mile, with a lower rate per mile for longer distances.
- The VAT price is the net price plus 20%.
To change prices, edit the `VEHICLE_PRICING` dictionary in that file.
