import logging
from pathlib import Path
import aiohttp
import sde.items
import json

logger = logging.getLogger('seat.{__name__}')

try:
    with open('config/seat.json', 'r') as jsonfile:
        config = json.load(jsonfile)
    _urlbase = config['baseurl']
    _token = config['token']
    _headers = {'X-Token': _token}
except:
    pass


async def get_contracts(corp_id, odata_filter: str):
    async with aiohttp.ClientSession(headers=_headers) as session:
        url = f'{_urlbase}/api/v2/corporation/contracts/{corp_id}?'
        if odata_filter and len(odata_filter) > 0:
            url += f'$filter={odata_filter}&'
        last_page = 2
        current_page = 1
        contracts = {}
        while current_page <= last_page:
            async with session.get(f'{url}page={current_page}') as r:
                if r.status == 200:
                    json_body = await r.json()
                    metadata = json_body['meta']
                    data = json_body['data']
                    last_page = metadata['last_page']
                    current_page += 1
                    for contract in data:
                        for item in contract['lines']:
                            item['item'] = await sde.items.get(item['type_id'])
                        contracts.update({contract['contract_id']: contract})
                else:
                    logger.error(
                        f'Could not get Contract data {url}page={current_page}')
                    raise Exception(
                        f'Could not get Contract data {url}page={current_page}')

        return contracts
