import csv
import logging
import sde

logger = logging.getLogger('sde.{__name__}')


class Item(dict):
    def __init__(self, id: int, group_id: int, name: str):
        dict.__init__(self, id=id, group_id=group_id, name=name)


_items = {}


async def initialize():
    try:
        await sde.download_sde('invTypes-nodescription.csv')
        with open(sde.get_file_path('invTypes-nodescription.csv'), newline='', encoding='UTF-8') as csvfile:
            types_csv = csv.reader(csvfile, delimiter=',', quotechar='"')
            test = {int(row[0]): Item(int(row[0]), int(row[1]), str(row[2]))
                    for row in types_csv}
            _items.update(test)
    except Exception as ex:
        logger.fatal(
            f'Unable to initialize SDE Items, {type(ex).__name__} {ex.args}')


async def get(id: int):
    return _items.get(id, Item(id, -1, 'Unknown'))
