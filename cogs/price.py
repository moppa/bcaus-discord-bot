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

            url = "https://evepraisal.com/appraisal/structured.json?persist=no"
            market = "jita"

            payload = json.dumps({
                "market_name": market,
                "items": [
                    {
                        "name": item
                    }
                ]
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.post(url, headers=headers, data=payload)
            result = json.loads(response.text)

            sell_avg = float(result["appraisal"]["items"][0]["prices"]["sell"]["avg"])
            buy_avg = float(result["appraisal"]["items"][0]["prices"]["buy"]["avg"])

            await ctx.channel.send(f"{market}: In average {item} sells for: {sell_avg:,.2f} and is bought for: {buy_avg:,.2f}")
        except KeyError as ke:
            print(ke)
            await ctx.channel.send(f"I could not find the item you were looking for.")
            return
        

async def setup(bot):
    await bot.add_cog(Price(bot))