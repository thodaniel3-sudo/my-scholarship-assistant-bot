"""Pydantic models for structured data."""
from datetime import date
from pydantic import BaseModel, HttpUrl
from typing import Optional


class ScholarshipRecord(BaseModel):
    title: str
    organization: Optional[str] = None
    host_country: Optional[str] = None
    host_university: Optional[str] = None
    degree_levels: Optional[str] = None
    eligible_nationalities: Optional[str] = None
    deadline: Optional[date] = None
    application_portal: Optional[HttpUrl] = None
    info_source: Optional[HttpUrl] = None
    notes: Optional[str] = None