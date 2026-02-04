web: gunicorn Blog_site.wsgi --chdir Blog_site --log-file -
release: cd Blog_site && python manage.py migrate && python manage.py create_default_superuser
