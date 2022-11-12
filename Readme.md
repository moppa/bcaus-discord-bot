# Setup local dev

1. Ensure you have the dependencies required for discord.py https://discordpy.readthedocs.io/en/stable/intro.html#installing  
   `sudo apt install libffi-dev libnacl-dev python3-dev python3.8-venv`
2. Create virtual environment `python3 -m venv .venv`
3. Activate virtual environment `source .venv/bin/activate`
4. Install requirements `pip install -r requirements.txt`
5. Copy `bot.json.example` to `bot.json` and add any missing secrets
6. Update your bot.json to include the modules/cogs you want your bot to run
7. Copy any .example configs in config/ and put in your values depending on which modules you load

# Run python script localy

`python3 bcaus_bot.py`

# Docker

## Build image

`docker build . -t bcaus-bot:local`

## Run image and mount local config folder

`docker run --rm -it -v ${PWD}/data:/usr/src/app/data -v ${PWD}/config:/usr/src/app/config bcaus-bot:local`

# Sample Cog

Create a new Cog in the cogs folder

```python
from discord.ext import commands
import discord
import logging


class Testcog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # An example ready initializer
        logging.info(f'Initialized: {__class__.__name__}')

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        # an example message listener with cogs
        logging.info('MESSSAGE!')

    @commands.command()
    async def command(self, ctx, arg1: str):
        # an example command with cogs
        await ctx.send(f'You said {arg1}')


async def setup(bot):
    await bot.add_cog(Testcog(bot))
```

Then register it to initialize in `bcaus_bot.py` within the main method `await bot.load_extension('cogs.cogclassname')`

```python
async def main():
    async with bot:
        ...
        await bot.load_extension('cogs.testcog')
        ...
        await bot.start(config['botToken'])
```
