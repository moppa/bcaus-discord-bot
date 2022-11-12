from discord.ext import commands
import discord
import json
import logging


class Forward(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.channels = {}
        self.logger = logging.getLogger(__class__.__name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Initializing channel forwarding config')
        for sourceKey in self.config:
            self.channels[int(sourceKey)] = []
            self.logger.debug(f'sourcekey: {sourceKey}')
            for destKey in self.config[sourceKey]:
                self.logger.debug(f'destKey: {destKey}')
                channel = self.bot.get_channel(destKey)
                self.channels[int(sourceKey)].append(channel)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author == self.bot.user:
            return
        try:
            source = self.channels[msg.channel.id]
            if (source):
                self.logger.debug(
                    f'Received message in: #{msg.channel.name} ({msg.channel.id}) from {msg.author.display_name}')
                destination: discord.TextChannel
                for destination in source:
                    self.logger.debug(
                        f'Forwarding to: #{destination.name} ({destination.id})')
                    name = '**' + msg.author.display_name + '**: '
                    content = name + msg.content
                    files = []
                    for attachment in msg.attachments:
                        files.append(await attachment.to_file())
                    await destination.send(content, files=files)
        except KeyError:
            pass


async def setup(bot):
    with open("config/forward.json", "r") as jsonfile:
        config = json.load(jsonfile)
    await bot.add_cog(Forward(bot, config))
