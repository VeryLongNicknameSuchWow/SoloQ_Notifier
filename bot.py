import sys

import aiohttp
import hikari
import lightbulb
import motor.motor_asyncio
from lightbulb.ext import tasks

import configuration

config_path = 'config.ini'
if len(sys.argv) == 2:
    config_path = sys.argv[1]
config = configuration.read_config(config_path)

bot = lightbulb.BotApp(token=config['DISCORD']['BOT_TOKEN'])
bot.load_extensions_from("./commands/")
bot.load_extensions_from("./tasks/")
tasks.load(bot)


@bot.listen()
async def on_starting(_: hikari.StartingEvent) -> None:
    bot.d.config = config

    bot.d.client_session = aiohttp.ClientSession(
        headers={'X-Riot-Token': config['RIOT']['API_KEY']},
        timeout=aiohttp.ClientTimeout(total=None),
    )

    bot.d.motor_client = motor.motor_asyncio.AsyncIOMotorClient(
        'mongodb://{db_user}:{db_password}@{db_host}:{db_port}'.format(**config['MONGO']),
    )


@bot.listen()
async def on_stopping(_: hikari.StoppingEvent) -> None:
    await bot.d.client_session.close()


@bot.command
@lightbulb.command('soloq', "main command group")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def main_command_group() -> None:
    pass


if __name__ == '__main__':
    bot.run()
