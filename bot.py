import sys

import hikari
import lightbulb
import miru
from lightbulb.ext import tasks
from pyot.conf.model import activate_model, ModelConf
from pyot.conf.pipeline import activate_pipeline, PipelineConf

import configuration

config_path = 'config.ini'
if len(sys.argv) == 2:
    config_path = sys.argv[1]
config = configuration.read_config(config_path)


@activate_model('lol')
class LolModel(ModelConf):
    default_platform = 'eun1'
    default_region = 'europe'
    default_version = 'latest'
    default_locale = 'en_us'


@activate_pipeline('lol')
class LolPipeline(PipelineConf):
    name = 'lol_main'
    default = True
    stores = [
        {
            'backend': 'pyot.stores.rediscache.RedisCache',
            'host': config['REDIS']['HOST'],
            'port': config['REDIS']['PORT'],
            'db': config['REDIS']['DB'],
        },
        {
            'backend': 'pyot.stores.cdragon.CDragon',
        },
        {
            'backend': 'pyot.stores.riotapi.RiotAPI',
            'api_key': config['RIOT']['API_KEY'],
            'rate_limiter': {
                'backend': 'pyot.limiters.redis.RedisLimiter',
                'limiting_share': 1,
                'host': config['REDIS']['HOST'],
                'port': config['REDIS']['PORT'],
                'db': config['REDIS']['DB'],
            }
        },
    ]


bot = lightbulb.BotApp(token=config['DISCORD']['BOT_TOKEN'])
miru.install(bot)

bot.load_extensions_from("./commands/")
bot.load_extensions_from("./tasks/")
tasks.load(bot)


@bot.listen()
async def on_starting(_: hikari.StartingEvent) -> None:
    bot.d.config = config


@bot.listen()
async def on_stopping(_: hikari.StoppingEvent) -> None:
    pass


@bot.command
@lightbulb.command('soloq', "main command group")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def main_command_group() -> None:
    pass


if __name__ == '__main__':
    bot.run()
