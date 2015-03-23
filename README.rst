=============
ddah-promises
=============

Django's promises egg.

Quick start
-----------

1. Add "ddah-promises" to INSTALLED_APPS:
  INSTALLED_APPS = {
    ...
    'ddah-promises'
  }

2. Include the ddah-promises URLconf in urls.py:
  url(r'^ddah-promises/', include('ddah-promises.urls'))

3. Run `python manage.py syncdb` to create ddah-promises's models.

4. Run the development server and access http://127.0.0.1:8000/admin/ to
    manage blog posts.

5. Access http://127.0.0.1:8000/ddah-promises/ to view a list of most recent posts.