CELERYBEAT_SCHEDULE = {
    # Executes every minute
    'periodic_tasks': {
        'task': 'users.tasks.refresh_users',
        'schedule': 15,
    }
}
CELERY_IMPORTS = ['users.tasks']
TASK_NEW_USERS_QUANTITY = 2