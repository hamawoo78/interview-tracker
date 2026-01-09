# InterviewTracker - Complete Setup Guide

## Project Overview

InterviewTracker is a Django-based web application for tracking job applications, interview progress, and storing interview preparation notes. It's designed as a single-user personal tool with built-in authentication.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser

## Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd interview-tracker
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install django pillow python-dateutil
```

### Step 4: Run Database Migrations

```bash
python manage.py migrate
```

This creates the SQLite database and all necessary tables.

### Step 5: Create Superuser Account

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account:
- Username: (choose your username)
- Email: (your email)
- Password: (choose a strong password)

### Step 6: (Optional) Load Sample Data

```bash
python manage.py seed_data
```

This creates 5 sample companies, 3 interview events, and 2 prep notes to explore the app.

### Step 7: Start Development Server

```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Step 8: Access the Application

Open your browser and visit: `http://localhost:8000`

You'll be redirected to the login page. Use the superuser credentials you created in Step 5.

## Project Structure

```
interview-tracker/
├── interview_tracker/          # Main Django project settings
│   ├── settings.py            # Configuration
│   ├── urls.py                # URL routing
│   ├── wsgi.py                # WSGI application
│   └── asgi.py                # ASGI application
│
├── core/                       # Core app (dashboard, calendar, messages)
│   ├── views.py               # Dashboard, calendar views
│   ├── urls.py                # Core URL patterns
│   ├── context_processors.py  # Template context
│   └── admin.py               # Admin configuration
│
├── companies/                  # Company management app
│   ├── models.py              # Company model
│   ├── views.py               # Company CRUD views
│   ├── forms.py               # Company form
│   ├── urls.py                # Company URL patterns
│   ├── admin.py               # Admin configuration
│   └── management/
│       └── commands/
│           └── seed_data.py   # Sample data command
│
├── interviews/                # Interview tracking app
│   ├── models.py              # InterviewEvent model
│   ├── views.py               # Interview CRUD views
│   ├── forms.py               # Interview form
│   ├── urls.py                # Interview URL patterns
│   └── admin.py               # Admin configuration
│
├── prep/                       # Interview prep app
│   ├── models.py              # InterviewPrep model
│   ├── views.py               # Prep edit view
│   ├── forms.py               # Prep form
│   ├── urls.py                # Prep URL patterns
│   └── admin.py               # Admin configuration
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with sidebar
│   ├── auth/
│   │   └── login.html         # Login page
│   ├── core/
│   │   ├── dashboard.html     # Dashboard
│   │   ├── calendar.html      # Calendar view
│   │   └── messages.html      # Messages placeholder
│   ├── companies/
│   │   ├── company_list.html  # Company list
│   │   ├── company_detail.html # Company detail
│   │   └── company_form.html  # Company form
│   ├── interviews/
│   │   ├── interview_form.html # Interview form
│   │   └── interview_confirm_delete.html
│   └── prep/
│       └── prep_form.html     # Prep form
│
├── media/                      # Uploaded files (logos, PDFs)
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── QUICKSTART.md              # Quick start guide
└── SETUP.md                   # This file
```

## Database Models

### Company
Stores information about job applications.

**Fields:**
- `name` - Company name (required)
- `logo` - Company logo image
- `website_url` - Company website
- `location` - Job location
- `status` - Applied, Interview, Offer, or Rejected
- `salary_min`, `salary_max` - Salary range
- `position_title` - Job title
- `job_description_url` - Link to job posting
- `job_description_file` - Uploaded PDF
- `created_at`, `updated_at` - Timestamps

### InterviewEvent
Tracks individual interview events.

**Fields:**
- `company` - Foreign key to Company
- `start_datetime` - Interview start time (required)
- `end_datetime` - Interview end time
- `interviewer_name` - Name of interviewer
- `interview_type` - Phone, Technical, Onsite, HR, Other
- `meeting_link` - Zoom/Google Meet link
- `notes` - Interview notes
- `created_at`, `updated_at` - Timestamps

### InterviewPrep
Stores preparation notes per company.

**Fields:**
- `company` - One-to-one relationship with Company
- `self_intro` - Self-introduction text
- `why_apply` - Why you applied
- `questions_to_ask` - Questions for interviewer
- `additional_notes` - Other notes
- `updated_at` - Last update timestamp

## URL Routes

| Route | Purpose |
|-------|---------|
| `/` | Dashboard |
| `/calendar/` | Calendar view |
| `/messages/` | Messages (placeholder) |
| `/companies/` | Company list |
| `/companies/create/` | Add new company |
| `/companies/<id>/` | Company detail |
| `/companies/<id>/edit/` | Edit company |
| `/interviews/add/<company_id>/` | Add interview |
| `/interviews/<id>/edit/` | Edit interview |
| `/interviews/<id>/delete/` | Delete interview |
| `/prep/<company_id>/edit/` | Edit prep notes |
| `/admin/` | Django admin |
| `/login/` | Login page |
| `/logout/` | Logout |

## Features

### Dashboard
- Search companies by name, position, or location
- View all companies as cards with status badges
- See salary ranges
- Track time since last interview
- Weekly calendar widget showing next 7 days of interviews

### Calendar
- Full-week view of upcoming interviews
- Grouped by day
- Shows interview type, interviewer, and meeting links
- Click to view company details

### Company Management
- Create, read, update, delete companies
- Track application status
- Store job description (URL or PDF)
- Upload company logo
- Filter by status and location

### Interview Tracking
- Log interview events with date/time
- Record interviewer name and type
- Store meeting links
- Add interview notes
- Edit or delete past interviews

### Interview Preparation
- Store self-introduction
- Document why you applied
- List questions to ask
- Add additional notes
- Edit anytime before interview

### Admin Panel
- Full CRUD for all models
- User management
- Data filtering and search
- Bulk operations

## Configuration

### Timezone
Default: `America/New_York`

To change, edit `interview_tracker/settings.py`:
```python
TIME_ZONE = 'Your/Timezone'
```

### Database
Default: SQLite (`db.sqlite3`)

To use PostgreSQL or MySQL, update `DATABASES` in `settings.py`.

### Media Files
Uploaded files are stored in `media/` directory.

To change, edit `MEDIA_ROOT` in `settings.py`.

## Common Tasks

### Reset Database
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
```

### Create New Superuser
```bash
python manage.py createsuperuser
```

### Change Port
```bash
python manage.py runserver 8001
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

### Run Tests
```bash
python manage.py test
```

### Access Django Shell
```bash
python manage.py shell
```

## Troubleshooting

### "Port 8000 already in use"
```bash
python manage.py runserver 8001
```

### "ModuleNotFoundError: No module named 'django'"
Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### "No such table" error
Run migrations:
```bash
python manage.py migrate
```

### "Permission denied" on media files
Ensure `media/` directory exists and is writable:
```bash
mkdir media
```

### Can't login
- Verify superuser was created: `python manage.py createsuperuser`
- Check username and password are correct
- Try resetting password: `python manage.py changepassword username`

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL recommended)
4. Use a production web server (Gunicorn, uWSGI)
5. Set up HTTPS with SSL certificate
6. Use environment variables for sensitive settings
7. Collect static files: `python manage.py collectstatic`

## Support

For issues or questions:
1. Check the README.md
2. Review Django documentation: https://docs.djangoproject.com/
3. Check Django admin for data integrity

## License

Personal project - modify and use as needed.
