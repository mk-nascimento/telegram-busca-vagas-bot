from dataclasses import dataclass, field
from enum import Enum

import httpcore
import requests


@dataclass
class Badges:
    friendlyBadge: bool  # NOSONAR


@dataclass
class Job(dict):
    id: int
    companyId: int
    name: str
    description: str
    careerPageId: int
    careerPageName: str
    careerPageLogo: httpcore.URL
    type: str
    publishedDate: str
    applicationDeadline: str
    isRemoteWork: bool
    city: str
    state: str
    country: str
    jobUrl: httpcore.URL
    badges: Badges
    disabilities: bool
    workplaceType: str
    careerPageUrl: httpcore.URL


@dataclass
class Pagination(dict):
    offset: int
    limit: int
    total: int


@dataclass
class ApiResponse(requests.models.Response):
    pagination: Pagination
    data: list[Job] = field(default_factory=list)


class AllowedQueryParams(Enum):
    JOB_NAME = 'jobName'
    LIMIT = 'limit'
    OFFSET = 'offset'
    WORKPLACE_TYPE = 'workplaceType'
