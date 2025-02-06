"""
This module contains the base class for a speech and other models.
"""
from pydantic import BaseModel, ConfigDict


class BaseClass(BaseModel):
    """A class to be used as base for other speeches data"""
    model_config = ConfigDict(populate_by_name=True,
                              frozen=True)
