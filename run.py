from main import Main
import os

from views.mute import register

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    raise Exception("TOKENが設定されてません")


extensions: tuple[str] = ("cogs.mute",)


if __name__ == "__main__":
    bot = Main(extensions, False)
    register(bot)
    bot.run(TOKEN)
