#!/usr/bin/env python3.6
import datetime
import discord
from discord.ext import commands

class Misc:
    """
    Miscellaneous commands
    """

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))
        
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong!"""
        # https://github.com/appu1232/Discord-Selfbot/blob/master/cogs/misc.py#L595
        msgtime = ctx.message.created_at.now()
        await (await self.bot.ws.ping())
        now = datetime.datetime.now()
        ping = now - msgtime
        return await ctx.send(":ping_pong:! Response Time: {} ms".format(str(ping.microseconds / 1000.0)))

    @commands.command(pass_context=True, aliases=['mc'])
    async def membercount(self, ctx):
        """Prints current member count"""
        return await ctx.send(str(self.bot.guild.name)+" currently has " + str(len(self.bot.guild.members)) + " members!")
    
    @commands.command()
    async def about(self, ctx):
        """About Link."""
        return await ctx.send("View my source code here: https://github.com/T3CHNOLOG1C/Link")
        
def setup(bot):
    bot.add_cog(Misc(bot))
