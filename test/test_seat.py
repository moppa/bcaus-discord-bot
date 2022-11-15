import unittest
import json
import seat.contracts


class TestSeat(unittest.IsolatedAsyncioTestCase):
    async def test_get_holdingcorp(self):
        odata_filter = 'status eq \'outstanding\' and type eq \'item_exchange\' and detail.assignee_id eq 1620149686'
        contracts = await seat.contracts.get_contracts(1620149686, odata_filter)
        self.assertGreater(len(contracts), 0)

    async def test_get_alliance_courier(self):
        odata_filter = 'status eq \'outstanding\' and type eq \'courier\' and detail.assignee_id eq 99010484'
        contracts = await seat.contracts.get_contracts(1620149686, odata_filter)
        self.assertGreater(len(contracts), 0)
        # with open('data/newcontract.json', 'w+') as json_file:
        #     json.dump(contracts[next(iter(contracts))], json_file)


if __name__ == '__main__':
    unittest.main()
