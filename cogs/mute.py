from __future__ import annotations

from discord.ext import commands
from typing import TYPE_CHECKING
import discord

from views.mute import MuteManageView

if TYPE_CHECKING:
    from main import Main


class MuteCog(commands.Cog):
    def __init__(self, bot: Main):
        self.bot = bot

    @commands.command("ミュートパネル", aliases=["mute", "ミュート"])
    async def create_mute_panel(self, ctx: commands.Context):
        if not isinstance(ctx.author, discord.Member):
            return

        if not ctx.author.voice or not ctx.author.voice.channel:
            return await ctx.send("VCに接続してから実行してね!", delete_after=15)

        view = MuteManageView(ctx.author.voice.channel.id)

        await view.start(ctx)


async def setup(bot):
    await bot.add_cog(MuteCog(bot))
