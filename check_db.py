#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_analyzer.settings')
django.setup()

from django.conf import settings

db_config = settings.DATABASES['default']
print(f"Database Engine: {db_config['ENGINE']}")
print(f"Database Name: {db_config.get('NAME', 'N/A')}")
print(f"Database Host: {db_config.get('HOST', 'N/A')}")
print(f"Full Config: {db_config}")
