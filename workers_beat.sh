. ./env/bin/activate
export ENV=development

celery -A main.celery beat --max-interval 1 -l info
deactivate