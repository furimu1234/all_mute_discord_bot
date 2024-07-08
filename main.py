from discord.ext import commands
import discord


class Main(commands.Bot):
    def __init__(self, extensions: tuple[str, ...], is_sync_tree: bool):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

        self._extensions = extensions
        self.is_sync_tree = is_sync_tree
        self.muters = {}

    async def setup_hook(self) -> None:
        for extension in self._extensions:
            if "cogs." not in extension:
                extension = f"cogs.{extension}"

            try:
                await self.load_extension(extension)
            except:
                import traceback

                traceback.print_exc()

        if self.is_sync_tree:
            await self.tree.sync()

    async def on_ready(self):
        print("起動完了")
