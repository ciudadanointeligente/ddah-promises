#!/usr/bin/env python
import sys

from django.conf import settings
import django


if not settings.configured:
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'testing_settings'
    django.setup()

from django.test.utils import get_runner


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['promises', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
