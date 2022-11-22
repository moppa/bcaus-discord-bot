from discord.ext import commands
import discord
import json
import logging
import requests
import xmltodict


class Price(commands.Cog):
    def __init__(self, bot):
        logging.info("Price init")
        self.bot = bot
        self.logger = logging.getLogger(__class__.__name__)

    @commands.command()
    async def price(self, ctx, *args):
        try: 
            logging.debug("Price command caught")
            if ctx.author == self.bot.user:
                return
    
            if len(args) < 1:
                await ctx.channel.send(f"You need to supply an item to check price for!")
                return

            item = " ".join(args).strip()
            amount = "1"
            market = "jita"


            url = "https://evepraisal.com/appraisal"
            payload = {
                'raw_textarea': item + ' 1',
                'market': market,
            }
            r = requests.post(url, params=payload)
            appraisal_id = r.headers['X-Appraisal-Id']
            appraisal_url = "https://evepraisal.com/a/{}.json".format(appraisal_id)
            result = requests.get(appraisal_url).json()
    
            sell_avg = float(result["items"][0]["prices"]["sell"]["avg"])
            buy_avg = float(result["items"][0]["prices"]["buy"]["avg"])

            await ctx.channel.send(f"{market}: In average {item} sells for: {sell_avg:,.2f} and is bought for: {buy_avg:,.2f}")
        except KeyError:
            await ctx.channel.send(f"I could not find the item you were looking for.")
            return
        

async def setup(bot):
    await bot.add_cog(Price(bot))