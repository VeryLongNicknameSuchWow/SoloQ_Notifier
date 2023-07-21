from typing import Tuple, Dict

import aiohttp

from riot.common import make_request

summoner_api_routing = {
    'br': 'br1',
    'eune': 'eun1',
    'euw': 'euw1',
    'lan': 'la1',
    'las': 'la2',
    'na': 'na1',
    'oce': 'oc1',
    'ru': 'ru1',
    'tr': 'tr1',
    'jp': 'jp1',
    'kr': 'kr',
    'ph': 'ph2',
    'sg': 'sg2',
    'tw': 'tw2',
    'th': 'th2',
    'vn': 'vn2',
}


def get_routing(region: str) -> str | None:
    region = region.casefold()
    if region in summoner_api_routing:
        return summoner_api_routing[region]
    return None


async def by_name(session: aiohttp.ClientSession, routing: str, summoner_name: str) -> Tuple[Dict, int]:
    url = f'https://{routing}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    return await make_request(session, url)


async def by_puuid(session: aiohttp.ClientSession, routing: str, puuid: str) -> Tuple[Dict, int]:
    url = f'https://{routing}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}'
    return await make_request(session, url)
