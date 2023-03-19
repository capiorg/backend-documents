import io
import re
import json
import logging
from typing import Any, Dict, List, Tuple, Union, Optional
from urllib.parse import unquote

import aiohttp
import async_timeout
from aiohttp import ContentTypeError

from services.http.errors.errors import DecodeJsonError


logger = logging.getLogger(__name__)


class FailedDecodeJson(Exception):
    pass


class HTTPClientDependencyMarker:
    pass


class HTTPClient:
    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        delay: int = 60,
        **kwargs,
    ) -> Tuple[Dict[str, Any], int] | Tuple[io.BytesIO, int]:
        if not headers:
            headers = {}
        url = re.sub(r"(https?:\/\/)|(\/){2,}", "\\1\\2", url)

        logger.info(msg=f"Отправляем запрос на {url}")

        async with async_timeout.timeout(delay=delay):
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.request(method=method, url=url, **kwargs) as resp:
                    return await self.handle_response(resp)

    async def handle_response(
        self, resp: aiohttp.ClientResponse
    ) -> Tuple[Dict[str, Any], int] | Tuple[io.BytesIO, int]:
        if resp.status >= 400:
            try:
                error_content = json.loads((await resp.content.read()).decode("utf-8"))
            except (UnicodeError, json.decoder.JSONDecodeError):
                error_content = {}

            logger.error(
                f"Произошла ошибка при отправке HTTP запроса, подробнее: {resp.json()}"
            )
            # raise HTTPRequestServiceError(
            #     detail=f"Произошла ошибка. Подробности: {error_content}",
            #     code=resp.status,
            # )

        content_type = resp.headers.get("Content-Type")
        try:
            if "text/plain" in content_type:
                resp_text = await resp.text()
                resp_json = json.loads(resp_text)
                return self.decode_json(resp_json), resp.status

            elif "application/json" in content_type:
                resp_json = await resp.json()
                return resp_json, resp.status

            else:
                resp_content = await resp.content.read()
                buffer = io.BytesIO(resp_content)
                return buffer, resp.status

        except ContentTypeError as e:
            raise FailedDecodeJson(f"Check args, URL is invalid - {e}") from e

    @staticmethod
    def decode_json(data: Union[List, Dict[str, Any]]) -> Dict[str, Any]:

        data_dumps = json.dumps(data, ensure_ascii=False)
        decoded_data_str = unquote(data_dumps)
        data_data_json = json.loads(decoded_data_str)
        return data_data_json
