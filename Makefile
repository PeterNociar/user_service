all: run

install:
	pip install -r requirements.txt && pip install -r requirements_dev.txt

run:
	FLASK_APP=users USER_SERVICE_SETTINGS=../settings.cfg flask run

test:
	USER_SERVICE_SETTINGS=../settings.cfg python -m pytest tests

celerybeat:
    celery -A celery_worker:celery beat --loglevel=INFO

celery:
    celery worker -A celery_worker.celery --loglevel=info -E --config=celeryconfig
