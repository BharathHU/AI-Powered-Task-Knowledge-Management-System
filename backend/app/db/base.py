# File: db/base.py
# Aggregator that imports all ORM model classes so that
# SQLAlchemy's metadata.create_all() can discover every table
# without requiring each model file to be imported individually.

from app.models.activity_log import ActivityLog
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.role import Role
from app.models.task import Task
from app.models.user import User
