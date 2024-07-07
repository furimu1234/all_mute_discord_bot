from __future__ import annotations

from discord import ui

import discord, re

from typing import Self, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from main import Main

mute_base = "mute:"
mute_base += "cid:{channel_id}:"

mute_template = mute_base.format(channel_id=r"(?P<channel_id>\w+)")

unmute_base = "unmute:"
unmute_base += "cid:{channel_id}:"

unmute_template = unmute_base.format(channel_id=r"(?P<channel_id>\w+)")


def register(bot: Main):
    bot.add_dynamic_items(MuteButton)
    bot.add_dynamic_items(UnMuteButton)


class MuteButton(ui.DynamicItem[ui.Button], template=mute_template):
    def __init__(self, channel_id: int):
        super().__init__(
            ui.Button(
                label="ミュート",
                style=discord.ButtonStyle.red,
                custom_id=mute_base.format(channel_id=channel_id),
            )
        )
        self.channel_id = channel_id

    @classmethod
    async def from_custom_id(
        cls: type[Self],
        interaction: discord.Interaction[Main],
        item: ui.Item,
        match: re.Match,
    ) -> Self:
        channel_id = int(match["channel_id"])

        return cls(channel_id)

    async def callback(self, interaction: discord.Interaction[Main]) -> Any:
        await interaction.response.defer(ephemeral=True)

        if not interaction.guild:
            return

        channel = interaction.guild.get_channel(self.channel_id)

        if not isinstance(channel, discord.VoiceChannel):
            return

        for member in channel.members:
            if not member.voice:
                continue

            if member.voice.mute:
                continue

            await member.edit(deafen=True, mute=True)

        await interaction.channel.send("全員ミュートにしました", delete_after=15)  # type: ignore


class UnMuteButton(ui.DynamicItem[ui.Button], template=unmute_template):
    def __init__(self, channel_id: int):
        super().__init__(
            ui.Button(
                label="ミュート解除",
                style=discord.ButtonStyle.green,
                custom_id=unmute_base.format(channel_id=channel_id),
            )
        )
        self.channel_id = channel_id

    @classmethod
    async def from_custom_id(
        cls: type[Self],
        interaction: discord.Interaction[Main],
        item: ui.Item,
        match: re.Match,
    ) -> Self:
        channel_id = int(match["channel_id"])

        return cls(channel_id)

    async def callback(self, interaction: discord.Interaction[Main]) -> Any:
        await interaction.response.defer(ephemeral=True)

        if not interaction.guild:
            return

        channel = interaction.guild.get_channel(self.channel_id)

        if not isinstance(channel, discord.VoiceChannel):
            return

        for member in channel.members:
            if not member.voice:
                continue

            if not member.voice.mute:
                continue

            try:
                await member.edit(deafen=False, mute=False)
            except:
                pass

        await interaction.channel.send("全員のミュートを解除しました", delete_after=15)  # type: ignore


class MuteManageView(ui.View):
    def __init__(self, channel_id: int):
        super().__init__(timeout=None)

        self.add_item(MuteButton(channel_id))
        self.add_item(UnMuteButton(channel_id))

    async def start(self, channel):
        e = discord.Embed(title="下のボタンを押してミュートを管理できます！")
        await channel.send(embeds=[e], view=self)
        await self.wait()
