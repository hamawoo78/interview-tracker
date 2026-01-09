# InterviewTracker

A personal web app to track job applications, interview progress, and store interview preparation notes.

## Features

- **Dashboard**: View all companies and upcoming interviews at a glance
- **Company Management**: Track companies with status (Applied → Interview → Offer → Rejected)
- **Interview Calendar**: Weekly calendar view of upcoming interviews
- **Interview Events**: Log interview details (date/time, interviewer, meeting links, notes)
- **Interview Prep**: Store preparation notes per company (self-intro, why you applied, questions to ask)
- **Search**: Quickly search companies by name, position, or location
- **Admin Panel**: Manage all data through Django admin

## Tech Stack

- **Backend**: Django 6.0 (Python)
- **Database**: SQLite (default)
- **Frontend**: Bootstrap 5 + Django Templates
- **Authentication**: Django Auth (single-user with login)

## Setup Instructions

### 1. Clone and Navigate to Project

```bash
cd interview-tracker
```

### 2. Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install django pillow python-dateutil
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

### 7. Login

Use the superuser credentials you created to log in.

## Project Structure

```
interview-tracker/
├── interview_tracker/      # Main project settings
├── core/                   # Dashboard and core views
├── companies/              # Company management
├── interviews/             # Interview event tracking
├── prep/                   # Interview preparation notes
├── templates/              # HTML templates
├── media/                  # Uploaded files (logos, PDFs)
├── manage.py
└── README.md
```

## URL Routes

- `/` - Dashboard
- `/calendar/` - Calendar view
- `/messages/` - Messages (placeholder)
- `/companies/` - Company list
- `/companies/create/` - Add new company
- `/companies/<id>/` - Company detail
- `/companies/<id>/edit/` - Edit company
- `/interviews/add/<company_id>/` - Add interview event
- `/interviews/<id>/edit/` - Edit interview event
- `/interviews/<id>/delete/` - Delete interview event
- `/prep/<company_id>/edit/` - Edit interview prep notes
- `/admin/` - Django admin panel
- `/login/` - Login page
- `/logout/` - Logout

## Models

### Company
- name, logo, website_url, location
- status (Applied, Interview, Offer, Rejected)
- salary_min, salary_max
- position_title
- job_description_url, job_description_file
- created_at, updated_at

### InterviewEvent
- company (ForeignKey)
- start_datetime, end_datetime
- interviewer_name
- interview_type (Phone, Technical, Onsite, HR, Other)
- meeting_link
- notes
- created_at, updated_at

### InterviewPrep
- company (OneToOneField)
- self_intro, why_apply, questions_to_ask, additional_notes
- updated_at

## Features Implemented

✅ User authentication (login/logout)
✅ Dashboard with company cards and weekly calendar
✅ Company CRUD operations
✅ Interview event tracking
✅ Interview preparation notes
✅ Search functionality
✅ File upload for job descriptions
✅ Status tracking
✅ Timezone-aware datetimes
✅ Django admin integration
✅ Responsive Bootstrap UI

## Future Enhancements

- Messages feature (currently placeholder)
- Company logo fetching from website
- Email notifications for upcoming interviews
- Interview notes history
- Salary negotiation tracker
- Export data to CSV/PDF
- Dark mode
- Mobile app

## Notes

- The app uses Django's built-in authentication for single-user access
- All datetimes are timezone-aware (default: America/New_York)
- Media files are stored in the `media/` directory
- Use Django admin (`/admin/`) for quick data management

## Troubleshooting

**Port already in use?**
```bash
python manage.py runserver 8001
```

**Database issues?**
```bash
python manage.py migrate --run-syncdb
```

**Static files not loading?**
```bash
python manage.py collectstatic
```

## License

Personal project - feel free to modify and use as needed.
