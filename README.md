# Arab Invest Intranet — Master Django Package

A database-driven corporate intranet + custom enterprise CMS dashboard.

## Fast start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Windows activation: `venv\\Scripts\\activate`

Website: `http://127.0.0.1:8000/`
CMS: `http://127.0.0.1:8000/dashboard/`
Emergency Django admin: `http://127.0.0.1:8000/admin/`

Optional database sample records:

```bash
python manage.py seed_demo
```

## Architecture

The single source of truth is the Django database. Content is not stored in browser storage. Django authentication sessions are used only for login state.

Navigation uses one self-referencing `NavigationItem.parent`, so the hierarchy is not hard-limited to Parent/Child/SubChild models.

Core content models:

- Navbar
- NavigationItem
- NavigationPage
- PageDocument
- PageLink
- PageImage
- NavigationDocument
- NavigationLink
- NavigationImage
- Banner
- BannerButton
- News
- ActivityLog (supporting audit model)

## Live workflow

Navbar → NavigationItem hierarchy → Page/Document/Link/Image → Page resources → Banner → Banner Buttons → News.

Uploaded files are served from Django `MEDIA_ROOT` in development and referenced through `MEDIA_URL`.

## Security

No client credentials are included. Put real secrets in `.env` or your production secret manager. Before production set `DEBUG=False`, production `ALLOWED_HOSTS`, HTTPS/CSRF trusted origins, secure cookies and a production database.
# baji-mamu-website_office
