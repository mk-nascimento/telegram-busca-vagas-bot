import logging

import requests

from app.exceptions import ExtendedException
from app.models import AllowedQueryParams, ApiResponse, Job, Pagination
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
                res = ApiResponse(**r.json())

                page = Pagination(**res.pagination)
                offset, total = page.offset, page.total

                while int(offset) < int(total):
                    params.update({off: offset, workplace: 'hybrid,remote'})
                    params.pop(limit, None)

                    r = client.get(url, params=params)
                    r.raise_for_status()
                    res = ApiResponse(**r.json())

                    dates: list[str] = [d['publishedDate'] for d in res.data]
                    validation = [is_after_last_request(d) for d in dates]
                    if all(validation):
                        data.extend(res.data)
                        offset += 10
                        page = res.pagination
                    else:
                        data.extend(
                            [
                                d
                                for d in res.data
                                if (is_after_last_request(d['publishedDate']))
                            ]
                        )
                        offset = total

                return data

            except Exception as e:
                raise ExtendedException('Error processing request') from e
