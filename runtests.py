#!/usr/bin/env python
import sys
import os

from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(os.path.dirname(__file__), 'test.db'),
                'TEST_NAME': os.path.join(os.path.dirname(__file__), 'test.db'),

            }
        },
        INSTALLED_APPS=(
            'django.contrib.contenttypes',
            'django_nose',
            'south',
            'django_faker',
            'popolo',
        ),
        TEST_RUNNER = 'django_nose.NoseTestSuiteRunner',
        SITE_ID=1,
        SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
        ROOT_URLCONF='popolo.urls',
        SOUTH_TESTS_MIGRATE = False,
        SKIP_SOUTH_TESTS = True,
    )


from django.test.utils import get_runner


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['promises', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
