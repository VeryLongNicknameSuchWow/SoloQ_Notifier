import lightbulb
from lightbulb.ext import tasks

ping_plugin = lightbulb.Plugin("Test Task")


@tasks.task(s=30, auto_start=True)
async def test_task():
    pass


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ping_plugin)
