import math

import discord
from discord.ext import menus
from discord.ext.menus.views import ViewMenuPages


REMOVE_BUTTONS = [
    "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f",
    "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f",
    "\N{BLACK SQUARE FOR STOP}\ufe0f",
]

class WildGrassPages(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=15)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page

        lines = [f"`{i+1}` **{v['name']}**　•　{v['rarity']}　•　{v['type']}　•　{v['age']}　•　{v['ovr']}/{v['pot']}"
                for i, v in enumerate(entries, start=offset)]

        footer = f"Showing entries {offset + 1}–{offset + len(lines)}"

        embed = discord.Embed(
            title="Wild Grass",
            description=f"\n".join(lines)[:2048],
            color=discord.Color.green()
        )
        embed.set_footer(text=footer)
        return embed

class ContinuablePages(ViewMenuPages):
    def __init__(self, source, allow_last=True, allow_go=True, **kwargs):
        super().__init__(source, **kwargs, timeout=120)
        self.allow_last = allow_last
        self.allow_go = allow_go
        for x in REMOVE_BUTTONS:
            self.remove_button(x)

    async def send_initial_message(self, ctx, channel):
        page = await self._source.get_page(self.current_page)
        kwargs = await self._get_kwargs_from_page(page)
        return await self.send_with_view(channel, **kwargs)

    async def show_checked_page(self, page_number):
        max_pages = self._source.get_max_pages()
        try:
            if max_pages is None:
                await self.show_page(page_number)
            elif page_number < 0 and not self.allow_last:
                await self.ctx.send(
                    "Sorry, this does not support going to last page. Try sorting in the reverse direction instead."
                )
            else:
                await self.show_page(page_number % max_pages)
        except IndexError:
            pass

    async def continue_at(self, ctx, page, *, channel=None, wait=False):
        self.stop()
        max_pages = self._source.get_max_pages()
        if max_pages is None:
            self.current_page = page
        else:
            self.current_page = page % self._source.get_max_pages()
        self.message = None
        await self.start(ctx, channel=channel, wait=wait)

        
