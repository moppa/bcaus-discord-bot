import unittest

import sde
import sde.items


class TestSde(unittest.IsolatedAsyncioTestCase):
    async def test_download(self):
        sde_file = 'invTypes-nodescription.csv'
        await sde.download_sde(sde_file)

    async def test_initialize(self):
        await sde.items.initialize()
        print(len(sde.items._items))
        print(sde.items._items[4]['name'])


if __name__ == '__main__':
    unittest.main()
