import json
import logging

import requests

from app.exceptions import ExtendedException
from app.models import AllowedQueryParams, ApiResponse, Job
from app.utils import is_after_last_request

logger = logging.getLogger(__name__)


class RequestAPI:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.client = requests.Session()

    async def search_jobs(self, keyword: str) -> list[Job]:
        url = self.base_url

        with self.client as client:
            name, limit, off, workplace = [k.value for k in AllowedQueryParams]
            params = {name: keyword, limit: 0}

            try:
                data: list[Job] = []

                r = client.get(url, params=params)
                r.raise_for_status()
                res = ApiResponse.model_validate(json.loads(r.text))

                offset, total = res.pagination.offset, res.pagination.total
                while offset < total:
                    params.update({off: offset, workplace: 'hybrid,remote'})
                    params.pop(limit, None)

                    r = client.get(url, params=params)
                    r.raise_for_status()
                    res = ApiResponse.model_validate(json.loads(r.text))

                    dates: list[str] = [d.published_date for d in res.data]
                    validation = [is_after_last_request(d) for d in dates]
                    if all(validation):
                        data.extend(res.data)
                        offset += 10
                    else:
                        after = is_after_last_request
                        data.extend([d for d in res.data if after(d.published_date)])
                        offset = total

                return data

            except Exception as e:
                raise ExtendedException('Error processing request') from e
