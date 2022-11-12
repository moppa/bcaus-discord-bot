import logging
import os
from pathlib import Path
import aiohttp


sde_path = Path('data/sde/')
sde_path.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger('sde')


def get_file_path(file):
    return f'{str(sde_path)}{os.sep}{file}'


async def download_sde(sde_file):
    async with aiohttp.ClientSession() as session:
        try:
            with open(get_file_path(f'{sde_file}.time'), 'r') as time_file:
                time = time_file.read()
                if time != None:
                    session.headers.add('if-modified-since', time)
        except:
            pass
        async with session.get(f'https://www.fuzzwork.co.uk/dump/latest/{sde_file}') as r:
            if r.status == 200:
                logger.debug('SDE Types: Downloaded')
                with open(get_file_path(sde_file), 'wb+') as content_file:
                    async for chunk in r.content.iter_chunked(1024):
                        content_file.write(chunk)
                with open(get_file_path(f'{sde_file}.time'), 'w+') as time_file:
                    time_file.write(r.headers.get('Last-Modified', None))
            elif r.status == 304:
                logger.debug('SDE Types: Not newer')
            else:
                logger.error('SDE Types: Errror downloading')
