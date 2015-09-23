import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'popolo',
    'taggit',
    'promises',
)
SITE_ID = 1
SECRET_KEY = 'this-is-just-for-tests-so-not-that-secret'
ROOT_URLCONF = 'popolo.urls'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
