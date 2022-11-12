import json
import logging
from pathlib import Path

import discord
from discord.ext import commands, tasks

import formatting
import seat.contracts


class Hauling(commands.Cog):
    def __init__(self, bot: commands.Bot, channel_id: int):
        self.logger = logging.getLogger(__class__.__name__)
        self.bot = bot
        self.channel_id = channel_id
        self.odata_filter = 'status eq \'outstanding\' and type eq \'courier\' and detail.assignee_id eq 99010484'
        self.corp_id = 1620149686

        try:
            Path('data/hauling/').mkdir(parents=True, exist_ok=True)
            with open('data/hauling/contractstate.json', 'r') as json_file:
                self.current_contracts = json.load(json_file)
        except:
            self.current_contracts = {}
        self.check_hauling_contracts.start()

    def cog_unload(self):
        self.check_hauling_contracts.cancel()

    async def post_contract(self, contract):
        title = contract['title'] if contract['title'] else 'Courier Contract'

        from_system = contract['start_location']['system_id'] if 'system_id' in contract[
            'start_location'] else contract['start_location']['solar_system_id']
        to_system = contract['end_location']['system_id'] if 'system_id' in contract[
            'end_location'] else contract['end_location']['solar_system_id']

        embed = discord.Embed(
            title=title,
            url=f"https://evemaps.dotlan.net/route/2:{from_system}:{to_system}",
            color=discord.Color.blue(),
        )
        embed.add_field(name='From',
                        value=contract['start_location']['name'], inline=False)
        embed.add_field(name='To',
                        value=contract['end_location']['name'], inline=False)
        embed.add_field(name='Issuer',
                        value=contract['issuer']['name'], inline=True)
        embed.add_field(name='Expires',
                        value=contract['date_expired'], inline=True)
        embed.add_field(name='Volume',
                        value=formatting.to_volume(contract['volume']), inline=False)
        embed.add_field(name='Reward',
                        value=formatting.to_isk(contract['reward']), inline=True)
        embed.add_field(name='Collateral',
                        value=formatting.to_isk(contract['collateral']), inline=True)

        await self.channel.send(embed=embed)

    @tasks.loop(minutes=1.0)
    async def check_hauling_contracts(self):
        try:
            contracts = await seat.contracts.get_contracts(
                self.corp_id, self.odata_filter)
            new_contracts = set(contracts.keys()) - \
                (self.current_contracts.keys())

            if len(new_contracts) > 0:
                for contract_id in new_contracts:
                    await self.post_contract(contracts.get(contract_id))
                self.current_contracts = contracts
                with open('data/hauling/contractstate.json', 'w+') as json_file:
                    json.dump(contracts, json_file)

        except Exception as e:
            self.logger.error(
                f'Unable to process new contracts {type(e).__name__}, {e.args}')

    @check_hauling_contracts.before_loop
    async def before_check_hauling_contracts(self):
        self.logger.info('Waiting for bot initialization')
        await self.bot.wait_until_ready()
        self.channel = self.bot.get_channel(self.channel_id)
        self.logger.info(f'Initialized')


async def setup(bot):
    with open('config/hauling.json', 'r') as jsonfile:
        config = json.load(jsonfile)
    await bot.add_cog(Hauling(bot, config['channel']))
