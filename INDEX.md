# InterviewTracker - Complete Index

## 📚 Documentation (Start Here!)

### For First-Time Users
1. **[README.md](README.md)** - Project overview, features, and tech stack
2. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
3. **[SETUP.md](SETUP.md)** - Detailed installation and configuration

### For Developers
1. **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development guide and best practices
2. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project summary
3. **[FILES_CREATED.md](FILES_CREATED.md)** - List of all files created

## 🚀 Quick Start

```bash
# 1. Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 2. Run migrations (if needed)
python manage.py migrate

# 3. Create superuser (if needed)
python manage.py createsuperuser

# 4. Load sample data (optional)
python manage.py seed_data

# 5. Start server
python manage.py runserver

# 6. Visit http://localhost:8000
```

## 📁 Project Structure

```
interview-tracker/
├── interview_tracker/      # Django project settings
├── core/                   # Dashboard, calendar, messages
├── companies/              # Company management
├── interviews/             # Interview tracking
├── prep/                   # Interview preparation
├── templates/              # HTML templates
├── media/                  # Uploaded files
├── venv/                   # Virtual environment
├── manage.py              # Django CLI
├── db.sqlite3             # Database
└── requirements.txt       # Dependencies
```

## 🎯 Features

### ✅ Implemented
- User authentication (login/logout)
- Dashboard with company cards and calendar widget
- Company CRUD operations
- Interview event tracking
- Interview preparation notes
- Search functionality
- File upload for job descriptions
- Status tracking (Applied → Interview → Offer → Rejected)
- Timezone-aware datetimes
- Django admin integration
- Responsive Bootstrap UI
- Sample data seeding

### 📋 Placeholder
- Messages feature (coming soon)

## 🗂️ App Organization

### core/
- Dashboard view with search and calendar
- Calendar view for upcoming interviews
- Messages placeholder
- Context processors for sidebar

**Key Files:**
- `views.py` - Dashboard, calendar, messages views
- `urls.py` - Core URL patterns
- `context_processors.py` - Template context

### companies/
- Company model and CRUD operations
- Company list with filtering
- Company detail page

**Key Files:**
- `models.py` - Company model
- `views.py` - Company views (ListView, DetailView, CreateView, UpdateView)
- `forms.py` - Company form
- `urls.py` - Company URL patterns
- `admin.py` - Admin configuration
- `management/commands/seed_data.py` - Sample data

### interviews/
- Interview event model and CRUD operations
- Interview form and views

**Key Files:**
- `models.py` - InterviewEvent model
- `views.py` - Interview views (CreateView, UpdateView, DeleteView)
- `forms.py` - Interview form
- `urls.py` - Interview URL patterns
- `admin.py` - Admin configuration

### prep/
- Interview preparation notes model
- Prep form and edit view

**Key Files:**
- `models.py` - InterviewPrep model
- `views.py` - Prep edit view
- `forms.py` - Prep form
- `urls.py` - Prep URL patterns
- `admin.py` - Admin configuration

## 📄 Templates

### Base Layout
- `templates/base.html` - Main layout with sidebar navigation

### Authentication
- `templates/auth/login.html` - Login page

### Core Pages
- `templates/core/dashboard.html` - Dashboard
- `templates/core/calendar.html` - Calendar view
- `templates/core/messages.html` - Messages placeholder

### Company Pages
- `templates/companies/company_list.html` - Company list
- `templates/companies/company_detail.html` - Company detail
- `templates/companies/company_form.html` - Company form

### Interview Pages
- `templates/interviews/interview_form.html` - Interview form
- `templates/interviews/interview_confirm_delete.html` - Delete confirmation

### Prep Pages
- `templates/prep/prep_form.html` - Prep form

## 🔗 URL Routes

| Route | View | Purpose |
|-------|------|---------|
| `/` | dashboard | Dashboard |
| `/calendar/` | calendar | Calendar view |
| `/messages/` | messages | Messages |
| `/companies/` | CompanyListView | Company list |
| `/companies/create/` | CompanyCreateView | Add company |
| `/companies/<id>/` | CompanyDetailView | Company detail |
| `/companies/<id>/edit/` | CompanyUpdateView | Edit company |
| `/interviews/add/<company_id>/` | InterviewEventCreateView | Add interview |
| `/interviews/<id>/edit/` | InterviewEventUpdateView | Edit interview |
| `/interviews/<id>/delete/` | InterviewEventDeleteView | Delete interview |
| `/prep/<company_id>/edit/` | prep_edit | Edit prep notes |
| `/admin/` | Django admin | Admin panel |
| `/login/` | LoginView | Login |
| `/logout/` | LogoutView | Logout |

## 💾 Database Models

### Company
```python
- name (CharField)
- logo (ImageField)
- website_url (URLField)
- location (CharField)
- status (ChoiceField: Applied, Interview, Offer, Rejected)
- salary_min, salary_max (IntegerField)
- position_title (CharField)
- job_description_url (URLField)
- job_description_file (FileField)
- created_at, updated_at (DateTimeField)
```

### InterviewEvent
```python
- company (ForeignKey to Company)
- start_datetime (DateTimeField)
- end_datetime (DateTimeField)
- interviewer_name (CharField)
- interview_type (ChoiceField: Phone, Technical, Onsite, HR, Other)
- meeting_link (URLField)
- notes (TextField)
- created_at, updated_at (DateTimeField)
```

### InterviewPrep
```python
- company (OneToOneField to Company)
- self_intro (TextField)
- why_apply (TextField)
- questions_to_ask (TextField)
- additional_notes (TextField)
- updated_at (DateTimeField)
```

## 🛠️ Common Commands

```bash
# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py seed_data

# Start server
python manage.py runserver

# Access shell
python manage.py shell

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check
```

## 📊 Sample Data

The `seed_data` command creates:
- 5 companies (Tech Corp, StartUp Inc, Big Finance, Cloud Systems, Data Analytics Co)
- 3 interview events
- 2 prep notes

## 🔐 Authentication

- Single-user setup with Django auth
- Superuser acts as the main user
- Login required for all views
- Session-based authentication

## 🎨 UI/UX

- Bootstrap 5 responsive design
- Sidebar navigation
- Color-coded status badges
- Responsive grid layout
- Mobile-friendly design

## ⚙️ Configuration

### Timezone
Default: `America/New_York`
Edit in `interview_tracker/settings.py`

### Database
Default: SQLite (`db.sqlite3`)
Can be switched to PostgreSQL, MySQL, etc.

### Media Files
Uploaded files stored in `media/` directory

## 📦 Dependencies

- Django 6.0.1
- Pillow 12.1.0 (image processing)
- python-dateutil 2.9.0 (date utilities)

## 🚀 Deployment

For production:
1. Set `DEBUG = False`
2. Update `ALLOWED_HOSTS`
3. Use production database
4. Use production web server (Gunicorn)
5. Set up HTTPS
6. Use environment variables for secrets

## 🐛 Troubleshooting

### Port already in use
```bash
python manage.py runserver 8001
```

### Database issues
```bash
python manage.py migrate
```

### Can't login
```bash
python manage.py createsuperuser
```

### Reset database
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
```

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Python Documentation](https://docs.python.org/)

## 🎓 Learning Path

1. **Understand the Project**
   - Read README.md
   - Review PROJECT_SUMMARY.md

2. **Get It Running**
   - Follow QUICKSTART.md
   - Run the server
   - Explore the app

3. **Understand the Code**
   - Read DEVELOPMENT.md
   - Review models in `*/models.py`
   - Review views in `*/views.py`
   - Review templates in `templates/`

4. **Make Changes**
   - Edit models
   - Create migrations
   - Update views
   - Update templates

5. **Deploy**
   - Follow deployment checklist in DEVELOPMENT.md
   - Set up production environment

## 📝 File Checklist

### Documentation
- ✅ README.md
- ✅ QUICKSTART.md
- ✅ SETUP.md
- ✅ DEVELOPMENT.md
- ✅ PROJECT_SUMMARY.md
- ✅ FILES_CREATED.md
- ✅ INDEX.md (this file)

### Configuration
- ✅ requirements.txt
- ✅ .gitignore
- ✅ manage.py
- ✅ db.sqlite3

### Django Project
- ✅ interview_tracker/settings.py
- ✅ interview_tracker/urls.py
- ✅ interview_tracker/wsgi.py
- ✅ interview_tracker/asgi.py

### Apps (core, companies, interviews, prep)
- ✅ models.py
- ✅ views.py
- ✅ forms.py
- ✅ urls.py
- ✅ admin.py
- ✅ apps.py
- ✅ tests.py
- ✅ migrations/

### Templates
- ✅ base.html
- ✅ auth/login.html
- ✅ core/* (3 files)
- ✅ companies/* (4 files)
- ✅ interviews/* (2 files)
- ✅ prep/* (1 file)

### Management Commands
- ✅ seed_data.py

## 🎯 Next Steps

1. **Read Documentation**
   - Start with README.md
   - Follow QUICKSTART.md

2. **Run the App**
   - Activate virtual environment
   - Run `python manage.py runserver`
   - Visit http://localhost:8000

3. **Explore Features**
   - Login with superuser
   - Add a company
   - Schedule an interview
   - Add prep notes
   - View calendar

4. **Customize**
   - Read DEVELOPMENT.md
   - Modify models, views, templates
   - Add new features

5. **Deploy**
   - Follow deployment guide
   - Set up production environment

## 📞 Support

For issues:
1. Check README.md
2. Check SETUP.md
3. Check DEVELOPMENT.md
4. Review Django documentation
5. Check Django admin for data

---

**InterviewTracker** - Track your job applications and interviews with ease!

Version: 1.0
Created: January 2026
