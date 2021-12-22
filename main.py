import logging
from logging import config

from fastapi import FastAPI

from app.infrastructure.database import create_tables
from routes import collabs, content, courses, metrics, reviews

try:
    config.fileConfig("logging.conf", disable_existing_loggers=False)
except KeyError as e:
    pass

logger = logging.getLogger(__name__)

app = FastAPI(title="courses")

create_tables()

app.include_router(courses.router)
app.include_router(collabs.router)
app.include_router(reviews.router)
app.include_router(content.router)
app.include_router(metrics.router)
