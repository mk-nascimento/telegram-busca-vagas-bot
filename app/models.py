from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Badges(BaseModel):
    friendly_badge: bool = Field(..., alias='friendlyBadge')


class Job(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    id: int
    company_id: int = Field(..., alias='companyId')
    name: str
    description: str
    keywords: list[str] = Field(..., default_factory=list)
    career_page_id: int = Field(..., alias='careerPageId')
    career_page_name: str = Field(..., alias='careerPageName')
    career_page_logo: str = Field(..., alias='careerPageLogo')
    career_page_url: str = Field(..., alias='careerPageUrl')
    type: str
    published_date: str = Field(..., alias='publishedDate')
    application_dead_line: Optional[str] = Field(..., alias='applicationDeadline')
    remote: bool = Field(..., alias='isRemoteWork')
    city: str
    state: str
    country: str
    job_url: str = Field(..., alias='jobUrl')
    badges: Badges
    disabilities: bool
    workplace_type: str = Field(..., alias='workplaceType')


class Pagination(BaseModel):
    offset: int
    limit: int
    total: int


class ApiResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    pagination: Pagination
    data: list[Job] = Field(default_factory=list)


class AllowedQueryParams(str, Enum):
    JOB_NAME = 'jobName'
    LIMIT = 'limit'
    OFFSET = 'offset'
    WORKPLACE_TYPE = 'workplaceType'
