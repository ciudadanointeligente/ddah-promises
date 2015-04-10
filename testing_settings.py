DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django_faker',
    'popolo',
)
SITE_ID = 1
SECRET_KEY = 'this-is-just-for-tests-so-not-that-secret'
ROOT_URLCONF = 'popolo.urls'
