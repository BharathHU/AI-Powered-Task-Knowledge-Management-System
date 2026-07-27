# File: schemas/base.py
# Shared Pydantic base model for all API schemas. Enables ORM-mode
# serialization so SQLAlchemy model instances can be converted to
# Pydantic responses automatically.

from pydantic import BaseModel, ConfigDict


class ORMBaseModel(BaseModel):
    """Base schema with ORM-to-Pydantic conversion enabled."""
    model_config = ConfigDict(from_attributes=True)
