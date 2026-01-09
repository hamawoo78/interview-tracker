from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from companies.models import Company
from interviews.models import InterviewEvent
from prep.models import InterviewPrep


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        # Clear existing data
        Company.objects.all().delete()
        InterviewEvent.objects.all().delete()
        InterviewPrep.objects.all().delete()

        # Create sample companies
        companies_data = [
            {
                'name': 'Tech Corp',
                'position_title': 'Senior Software Engineer',
                'location': 'San Francisco, CA',
                'status': 'interview',
                'website_url': 'https://techcorp.com',
                'salary_min': 150000,
                'salary_max': 200000,
            },
            {
                'name': 'StartUp Inc',
                'position_title': 'Full Stack Developer',
                'location': 'New York, NY',
                'status': 'applied',
                'website_url': 'https://startupinc.com',
                'salary_min': 120000,
                'salary_max': 160000,
            },
            {
                'name': 'Big Finance',
                'position_title': 'Backend Engineer',
                'location': 'Chicago, IL',
                'status': 'interview',
                'website_url': 'https://bigfinance.com',
                'salary_min': 140000,
                'salary_max': 180000,
            },
            {
                'name': 'Cloud Systems',
                'position_title': 'DevOps Engineer',
                'location': 'Seattle, WA',
                'status': 'offer',
                'website_url': 'https://cloudsystems.com',
                'salary_min': 130000,
                'salary_max': 170000,
            },
            {
                'name': 'Data Analytics Co',
                'position_title': 'Data Engineer',
                'location': 'Boston, MA',
                'status': 'rejected',
                'website_url': 'https://dataanalytics.com',
                'salary_min': 110000,
                'salary_max': 150000,
            },
        ]

        companies = []
        for data in companies_data:
            company = Company.objects.create(**data)
            companies.append(company)
            self.stdout.write(f'Created company: {company.name}')

        # Create sample interview events
        now = timezone.now()
        interview_data = [
            {
                'company': companies[0],
                'start_datetime': now + timedelta(days=2, hours=10),
                'end_datetime': now + timedelta(days=2, hours=11),
                'interviewer_name': 'John Smith',
                'interview_type': 'technical',
                'meeting_link': 'https://zoom.us/j/123456789',
                'notes': 'Prepare for system design questions',
            },
            {
                'company': companies[0],
                'start_datetime': now + timedelta(days=5, hours=14),
                'end_datetime': now + timedelta(days=5, hours=15),
                'interviewer_name': 'Sarah Johnson',
                'interview_type': 'hr',
                'meeting_link': 'https://zoom.us/j/987654321',
                'notes': 'Final round - discuss compensation',
            },
            {
                'company': companies[2],
                'start_datetime': now + timedelta(days=3, hours=9),
                'end_datetime': now + timedelta(days=3, hours=10),
                'interviewer_name': 'Mike Chen',
                'interview_type': 'phone',
                'meeting_link': 'https://meet.google.com/abc-defg-hij',
                'notes': 'Initial screening call',
            },
        ]

        for data in interview_data:
            interview = InterviewEvent.objects.create(**data)
            self.stdout.write(f'Created interview: {interview.company.name} on {interview.start_datetime}')

        # Create sample prep notes
        prep_data = [
            {
                'company': companies[0],
                'self_intro': 'I am a software engineer with 5 years of experience in full-stack development. I specialize in Python and JavaScript.',
                'why_apply': 'Tech Corp is a leader in cloud infrastructure, and I am excited about the opportunity to work on scalable systems.',
                'questions_to_ask': '1. What is the team structure?\n2. What are the main challenges the team is facing?\n3. What is the career growth path?',
                'additional_notes': 'Review system design patterns before the technical interview.',
            },
            {
                'company': companies[1],
                'self_intro': 'Full-stack developer with expertise in React and Django.',
                'why_apply': 'StartUp Inc is building innovative solutions in the fintech space.',
                'questions_to_ask': '1. What is the tech stack?\n2. How is the team organized?\n3. What are the main priorities for the next quarter?',
                'additional_notes': 'Prepare portfolio projects.',
            },
        ]

        for data in prep_data:
            prep = InterviewPrep.objects.create(**data)
            self.stdout.write(f'Created prep notes for: {prep.company.name}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with sample data'))
