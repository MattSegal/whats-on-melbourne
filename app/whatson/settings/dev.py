from . import *

DEBUG = True
SECRET_KEY = "dev-secret-key"
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS = True

CELERY_TASK_ALWAYS_EAGER = False
