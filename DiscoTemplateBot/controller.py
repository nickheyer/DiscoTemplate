from DiscoTemplateClient.utils import get_config
from DiscoTemplateBot.bot import DiscordBot


async def main():
    print("[CONTROLLER] BOT STARTING")

    config = await get_config()
    token = (
        config.discord_token
    )

    bot_instance = DiscordBot()
    await bot_instance.start(token)


async def kill():
    bot_instance = DiscordBot()
    await bot_instance.close()

    print("[CONTROLLER] BOT KILLED")
