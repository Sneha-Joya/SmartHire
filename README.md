# QuickLance - Freelancing Platform

A comprehensive freelancing platform built with Django that connects clients with skilled freelancers. Clients can post jobs and hire freelancers, while freelancers can showcase their profiles, browse jobs, and apply for opportunities.

## Features

### For Clients
- Post jobs with detailed descriptions, budgets, and required skills
- Browse and manage applications from freelancers
- Accept or reject applications
- View freelancer profiles and ratings
- Manage posted jobs

### For Freelancers
- Create detailed profiles with skills, hourly rates, and portfolios
- Browse available jobs with search and filter functionality
- Apply for jobs with proposals and rate estimates
- Track application status
- Showcase ratings and project history

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5.3.0, HTML5
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Image Handling**: Pillow

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd free
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Create some initial categories (optional)**
   You can create categories through the Django admin panel or by running:
   ```bash
   python manage.py shell
   ```
   Then in the shell:
   ```python
   from jobs.models import Category
   Category.objects.create(name="Web Development", description="Web development projects")
   Category.objects.create(name="Graphic Design", description="Graphic design projects")
   Category.objects.create(name="Writing", description="Content writing projects")
   Category.objects.create(name="Marketing", description="Marketing projects")
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Project Structure

```
quicklance/
├── accounts/          # User authentication and profiles
│   ├── models.py      # User, FreelancerProfile, ClientProfile models
│   ├── views.py       # Registration, login, profile views
│   ├── forms.py       # User registration and profile forms
│   └── urls.py        # Account-related URLs
│
├── jobs/              # Job posting and applications
│   ├── models.py      # Job, Application, Category models
│   ├── views.py       # Job browsing, posting, application views
│   ├── forms.py       # Job posting and application forms
│   └── urls.py        # Job-related URLs
│
├── templates/         # HTML templates
│   ├── base.html      # Base template with navigation
│   ├── accounts/      # Account-related templates
│   └── jobs/          # Job-related templates
│
├── static/            # Static files (CSS, JS, images)
├── media/             # User-uploaded files (profile pictures)
└── quicklance/        # Project settings
    ├── settings.py    # Django settings
    └── urls.py        # Main URL configuration
```

## Usage Guide

### For Clients

1. **Register as a Client**
   - Go to Register page
   - Select "Client" as account type
   - Fill in your details and create account

2. **Post a Job**
   - Click "Post Job" in navigation
   - Fill in job details (title, description, budget, skills, etc.)
   - Submit the job

3. **Manage Applications**
   - Go to "My Jobs"
   - Click on a job to view details
   - Click "Manage Applications" to see all applications
   - Accept or reject applications

### For Freelancers

1. **Register as a Freelancer**
   - Go to Register page
   - Select "Freelancer" as account type
   - Fill in your details and create account

2. **Complete Your Profile**
   - Go to Profile page
   - Click "Edit Profile"
   - Add your bio, skills, hourly rate, portfolio, etc.

3. **Browse and Apply for Jobs**
   - Browse jobs on the home page
   - Use search and category filters
   - Click on a job to view details
   - Click "Apply for this Job" to submit an application
   - Track your applications in "My Applications"

## Admin Panel

Access the Django admin panel at `/admin/` to:
- Manage users, jobs, and applications
- Create and manage categories
- View and edit all data

## Development Notes

- The project uses SQLite by default for easy setup
- For production, consider switching to PostgreSQL or MySQL
- Update `SECRET_KEY` in `settings.py` for production
- Set `DEBUG = False` in production
- Configure proper static file serving for production

## Future Enhancements

Potential features to add:
- Messaging system between clients and freelancers
- Payment integration
- Rating and review system
- File uploads for job deliverables
- Advanced search with multiple filters
- Email notifications
- Job completion workflow
- Dispute resolution system

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please refer to the Django documentation or create an issue in the project repository.

