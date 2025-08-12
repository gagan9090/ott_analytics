# ott_analytics 
 

# OTT Analytics Dashboard

## Overview
A Django-based internal admin dashboard to analyze user behavior for an OTT platform.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

