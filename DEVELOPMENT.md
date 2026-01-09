# Development Guide

## Project Architecture

InterviewTracker follows Django's MVT (Model-View-Template) architecture with a modular app structure.

### App Organization

**core/** - Dashboard and main navigation
- Dashboard view with search and calendar widget
- Calendar view for upcoming interviews
- Messages placeholder
- Context processors for sidebar data

**companies/** - Company management
- Company model with all job application details
- CRUD views using class-based views
- Company list with filtering
- Company detail with related interviews and prep notes

**interviews/** - Interview event tracking
- InterviewEvent model for logging interviews
- Create, update, delete views
- Form for interview details

**prep/** - Interview preparation
- InterviewPrep model (one-to-one with Company)
- Edit view for prep notes
- Form for all prep fields

## Models Relationships

```
Company (1) ──── (Many) InterviewEvent
   │
   └──── (1) InterviewPrep
```

## Key Design Decisions

### 1. Single User
- Uses Django's built-in User model
- Login required for all views
- Superuser acts as the single user

### 2. Timezone Awareness
- All datetimes are timezone-aware
- Default timezone: America/New_York
- Easily configurable in settings

### 3. Class-Based Views
- Used for CRUD operations (ListView, DetailView, CreateView, UpdateView)
- Cleaner code and less repetition
- Function-based views for custom logic

### 4. Bootstrap 5 Styling
- Responsive design
- Consistent UI across all pages
- Easy to customize

### 5. SQLite Database
- Default for development
- Easy to switch to PostgreSQL/MySQL for production
- Migrations handle schema changes

## Common Development Tasks

### Add a New Field to Company

1. Edit `companies/models.py`:
```python
class Company(models.Model):
    # ... existing fields ...
    new_field = models.CharField(max_length=255, blank=True, null=True)
```

2. Create migration:
```bash
python manage.py makemigrations
```

3. Apply migration:
```bash
python manage.py migrate
```

4. Update `companies/forms.py` to include new field:
```python
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [..., 'new_field']
```

5. Update templates to display/edit the field

### Add a New View

1. Create view in appropriate `views.py`:
```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    # Your logic here
    return render(request, 'template.html', context)
```

2. Add URL in `urls.py`:
```python
path('my-route/', views.my_view, name='my_view_name'),
```

3. Create template in `templates/` directory

4. Add navigation link in `templates/base.html` if needed

### Add a New App

1. Create app:
```bash
python manage.py startapp myapp
```

2. Create models in `myapp/models.py`

3. Create views in `myapp/views.py`

4. Create forms in `myapp/forms.py`

5. Create URLs in `myapp/urls.py`

6. Register in `interview_tracker/urls.py`:
```python
path('myapp/', include('myapp.urls')),
```

7. Add to `INSTALLED_APPS` in `settings.py`

8. Create migrations and migrate:
```bash
python manage.py makemigrations
python manage.py migrate
```

9. Register models in `myapp/admin.py`

## Testing

### Run Tests
```bash
python manage.py test
```

### Run Specific Test
```bash
python manage.py test companies.tests.CompanyModelTest
```

### Test with Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Debugging

### Django Shell
```bash
python manage.py shell
```

Example queries:
```python
from companies.models import Company
companies = Company.objects.all()
company = Company.objects.get(id=1)
company.name = "New Name"
company.save()
```

### Print Queries
Add to `settings.py`:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Debug Toolbar
```bash
pip install django-debug-toolbar
```

Add to `INSTALLED_APPS` and `MIDDLEWARE` in settings.

## Performance Optimization

### Database Queries
Use `select_related()` and `prefetch_related()`:
```python
# Instead of:
companies = Company.objects.all()

# Use:
companies = Company.objects.prefetch_related('interviews', 'prep')
```

### Caching
Add caching for frequently accessed data:
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def my_view(request):
    # ...
```

### Database Indexing
Add indexes to frequently queried fields:
```python
class Company(models.Model):
    name = models.CharField(max_length=255, db_index=True)
```

## Security Considerations

### CSRF Protection
- All forms include `{% csrf_token %}`
- Enabled by default in Django

### SQL Injection
- Use ORM queries (not raw SQL)
- Use parameterized queries if needed

### XSS Protection
- Django templates auto-escape by default
- Use `|safe` filter only for trusted content

### Authentication
- All views use `@login_required` decorator
- Class-based views use `LoginRequiredMixin`

### File Upload Security
- Validate file types
- Store uploads outside web root
- Use `FileField` with validators

## Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Use production database
- [ ] Set `SECRET_KEY` from environment
- [ ] Use HTTPS
- [ ] Set up static files collection
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Use production web server (Gunicorn)
- [ ] Set up database backups
- [ ] Configure CORS if needed
- [ ] Set up monitoring/alerts

## Code Style

### Follow PEP 8
```bash
pip install flake8
flake8 .
```

### Format Code
```bash
pip install black
black .
```

### Type Hints (Optional)
```python
from typing import Optional

def get_company(company_id: int) -> Optional[Company]:
    return Company.objects.filter(id=company_id).first()
```

## Git Workflow

### Commit Messages
```
[feature] Add interview prep notes
[bugfix] Fix calendar display issue
[docs] Update README
[refactor] Simplify company views
```

### Branch Naming
```
feature/add-notifications
bugfix/fix-timezone-issue
docs/update-setup-guide
```

## Useful Django Commands

```bash
# Create app
python manage.py startapp appname

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Change password
python manage.py changepassword username

# Run shell
python manage.py shell

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Run server
python manage.py runserver

# Check for issues
python manage.py check

# Flush database
python manage.py flush

# Load data
python manage.py loaddata fixture.json

# Dump data
python manage.py dumpdata > backup.json
```

## Troubleshooting Development Issues

### "No such table" error
```bash
python manage.py migrate
```

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Port already in use
```bash
python manage.py runserver 8001
```

### Static files not loading
```bash
python manage.py collectstatic
```

### Database locked
```bash
rm db.sqlite3
python manage.py migrate
```

### Template not found
- Check template path in `TEMPLATES['DIRS']`
- Verify template file exists
- Check app is in `INSTALLED_APPS`

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/design-philosophies/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)

## Contributing

When adding new features:
1. Create a new branch
2. Write tests
3. Update documentation
4. Follow code style guidelines
5. Submit for review

## Future Development Ideas

- [ ] Add email notifications
- [ ] Implement interview notes versioning
- [ ] Add salary negotiation tracker
- [ ] Create export to PDF/CSV
- [ ] Implement dark mode
- [ ] Add mobile app
- [ ] Complete messages feature
- [ ] Auto-fetch company logos
- [ ] Add interview performance tracking
- [ ] Create offer comparison tool
- [ ] Add calendar sync (Google Calendar, Outlook)
- [ ] Implement analytics dashboard
