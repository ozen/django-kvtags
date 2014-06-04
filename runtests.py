#!/usr/bin/env python
import os
import sys

from django.conf import settings
from django.core.management import execute_from_command_line


settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'tagging',
        'tests',
    ]
)

if not settings.configured:
    pass

def runtests():
    upper_dir = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    sys.path.append(upper_dir)
    argv = sys.argv[:1] + ['test'] + sys.argv[1:]
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()