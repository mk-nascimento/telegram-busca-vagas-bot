import logging
from http.client import HTTPException

import httpx

from app.models import AllowedQueryParams, ApiResponse, Job
from app.utils import is_after_last_request

logger = logging.getLogger(__name__)


class RequestAPI:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.client = httpx.Client()

    async def search_jobs(self, keyword: str) -> list[Job]:
        base_url = self.base_url

        with self.client as client:
            query_params_keys = [k.value for k in AllowedQueryParams]
            job_name, limit_key, offset_key, workplace = query_params_keys

            query_params = {job_name: keyword, limit_key: 0}
            params = httpx.QueryParams(query_params)

            try:
                data: list[Job] = []

                _res: ApiResponse = client.get(base_url, params=params).json()
                response = ApiResponse(**_res)

                page = response.pagination
                offset, total = int(page.get('offset', 0)), int(page.get('total', 0))

                while offset < total:
                    query_params.update({offset_key: offset, workplace: 'remote'})
                    query_params.pop(limit_key, None)
                    params = httpx.QueryParams(query_params)

                    _res = client.get(base_url, params=params).json()
                    response, jobs = ApiResponse(**_res), [j for j in response.data]

                    str_dates: list[str] = [job['publishedDate'] for job in jobs]
                    validation = [is_after_last_request(date) for date in str_dates]

                    is_all_new = all(validation)
                    if not is_all_new:
                        data.extend(jobs)
                        offset += 10
                        page = response.pagination
                    else:
                        data.extend([j for j in jobs if (
                            is_after_last_request(j['publishedDate']))])
                        offset = total

                return data
            except HTTPException as e:
                raise HTTPException('Request Failed') from e
