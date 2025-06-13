from celery import Celery
import os
from dotenv import load_dotenv

BROKER_URL = os.getenv("BROKER_URL")
BACKEND_URL = os.getenv("BACKEND_URL")
if not BROKER_URL or not BACKEND_URL:
    load_dotenv()
    BROKER_URL = os.getenv("BROKER_URL")
    BACKEND_URL = os.getenv("BACKEND_URL")

celery_app = Celery(__name__, broker=BROKER_URL, backend=BACKEND_URL, include=["celery_tasks.tasks"])