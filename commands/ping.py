import hikari
import lightbulb

plugin = lightbulb.Plugin("Ping Command")


@plugin.command
@lightbulb.command('ping', "Test command")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond("Pong!", flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)
