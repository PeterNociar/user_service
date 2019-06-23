from users import create_app
from users import celery_ as celery

app = create_app()
app.app_context().push()
