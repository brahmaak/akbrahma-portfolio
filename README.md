# A K Brahma — Developer Portfolio

A full-stack portfolio website with a secure, custom-built admin dashboard for managing projects, skills, experience and contact messages.

**Live site:** _coming soon_

## Features

**Public website**

- Responsive dark-theme design (mobile, tablet, desktop) built with Bootstrap 5 and custom CSS
- Home, About, Skills, Projects (with technology filters), Project detail and Contact pages
- All content loaded from PostgreSQL and editable without touching code
- Contact form with server-side validation, CSRF protection and a honeypot spam trap
- SEO-friendly URLs (slugs), per-page titles and meta descriptions, custom 404 page
- Accessibility: semantic HTML, skip link, ARIA labels, reduced-motion support

**Private dashboard**

- Staff-only login with brute-force protection (lockout after 5 failed attempts)
- Full CRUD for projects (with image uploads), skills and experience
- Messages inbox with unread badge, pagination and read/unread status
- Profile editing (bio, photo, resume PDF, social links)

**Security**

- Secrets kept in environment variables, never in code
- HTTPS redirect, secure cookies and HSTS in production
- Configurable private admin URL
- Upload validation (file type and size limits)

## Tech Stack

| Layer    | Technology                                 |
| -------- | ------------------------------------------ |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5       |
| Backend  | Python 3.14, Django 5.2 (LTS)              |
| Database | PostgreSQL 18                              |
| Security | django-axes, django-environ                |
| Testing  | Django test framework (29 automated tests) |

## Run Locally

1. Clone the repository and create a virtual environment:
   ```bash
   git clone https://github.com/YOUR-USERNAME/akbrahma-portfolio.git
   cd akbrahma-portfolio
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Create a PostgreSQL database, then copy `.env.example` to `.env` and fill in your own values.
3. Set up the database and an admin account:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Start the server and open http://127.0.0.1:8000/
   ```bash
   python manage.py runserver
   ```

## Run the Tests

```bash
python manage.py test
```

## Author

**A K Brahma** — Full Stack Web Developer
