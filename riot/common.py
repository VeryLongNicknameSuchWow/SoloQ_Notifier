import logging
from typing import Tuple, Dict

import aiohttp

logger = logging.getLogger(__name__)


async def make_request(session: aiohttp.ClientSession, url: str) -> Tuple[Dict, int]:
    try:
        async with session.get(url) as response:
            return await response.json(), response.status
    except aiohttp.ClientError as e:
        logger.error(e, exc_info=True)
        return {'status': {'message': 'Client Error', 'status_code': -1}}, -1
