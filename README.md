# Campus Notices (Django)

A simple Django web application for sharing campus information/notices. Notices are time-based: each notice has an expiry date/time and is automatically shown as **Current** or **Late** once it expires. Access to notices requires login.

## Features
- Django project (`config`) and app (`notices`)
- URL routing, views, and templates (login, notice list, notice detail)
- `Notice` model with time-based status (`Current` / `Late`)
- SQLite database with migrations and sample records
- Django admin for managing notices

## Requirements
- Python 3.10+ (developed/tested with Python 3.13)
- pip
- Dependencies listed in `requirements.txt`

## Installation and execution
1. **Open a terminal in the project folder**
   ```bash
   cd StudentPolls
   ```

2. **Create and activate a virtual environment** (if not already active)
   - Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (Command Prompt):
     ```cmd
     python -m venv venv
     venv\Scripts\activate.bat
     ```
   - macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **(Optional) Load/create sample data and users**
   This repository may already include a seeded `db.sqlite3`. If you start with a fresh database, create sample users/notices via the Django admin (`python manage.py createsuperuser`) or the Django shell. Sample accounts expected for demo:
   - Admin (superuser): **`MATILDA` / `123`**
   - Regular user: **`matilda_user` / `123`**

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open the app**
   - App/login: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Sample data
The database is seeded with at least three sample notices, including both **Current** and **Late** examples, to demonstrate time-based status changes.

## Project structure (key files)
- `manage.py` — Django command-line utility
- `config/settings.py` — project settings (apps, database, auth, templates)
- `config/urls.py` — project URL configuration
- `notices/models.py` — `Notice` model and time-based late/current logic
- `notices/views.py` — login-protected list/detail views
- `notices/urls.py` — app URL routes
- `notices/admin.py` — admin registration
- `notices/templates/` — HTML templates (notices and login)
- `notices/migrations/` — database migrations

## OOP concepts in this project
- **Classes & objects:** `Notice` is a Python class; each database row is a model instance/object.
- **Inheritance:** `Notice` inherits from `django.db.models.Model`; views/forms/admin components also build on Django base classes/patterns.
- **Encapsulation:** data (fields like `title`, `content`, `expires_at`) and behavior (`is_late`, `status`, `__str__`) are grouped within the model class.
- **Abstraction/reuse:** Django’s ORM, auth, URL routing, and template rendering provide reusable abstractions used by the app.
