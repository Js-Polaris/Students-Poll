# Campus Notices — Presentation Outline (10–12 slides)

Use this as a guide for the required group presentation and live demo.

1. **Title & group**
   - Project: Campus Notices (Django), course, group members, date.
2. **Introduction to Django**
   - What Django is, key features (batteries-included, ORM, admin, security), example apps/sites.
3. **MVT architecture**
   - Model, View, Template roles; compare briefly to MVC.
4. **Request/response flow in this app**
   - Browser → `config/urls.py` → `notices/urls.py` → view → model/query → template → HTML response.
5. **Development environment & setup**
   - Python, virtual environment, `pip install -r requirements.txt`, `django-admin`/project creation, `runserver`.
6. **Project structure**
   - Purpose of `manage.py`, `config/settings.py`, `config/urls.py`, `notices/models.py`, `notices/views.py`, `notices/urls.py`, `notices/templates/`.
7. **URLs, views, and templates demo**
   - Login-required access, notice list and notice detail pages; show template rendering.
8. **Models, database, and migrations**
   - `Notice` fields (`title`, `content`, `created_at`, `expires_at`), SQLite, `makemigrations`/`migrate`, admin/sample records.
9. **Time-based “late” notices**
   - How `expires_at` and status logic mark notices Current/Late automatically.
10. **OOP concepts in Django/this project**
    - Classes/objects/instances, inheritance (`models.Model`), encapsulation (fields + methods/properties like `is_late`/`status`), ORM abstraction.
11. **Live practical demonstration**
    - Run server, log in (`MATILDA`/`123` or `matilda_user`/`123`), show 3+ sample notices (current & late), open a detail page, show admin and records in SQLite/admin.
12. **Conclusion & Q&A**
    - What was learned, challenges, and how Python/OOP connects to web development.
