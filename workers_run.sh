. ./env/bin/activate
export ENV=development

celery -A main.celery worker -l info
deactivate