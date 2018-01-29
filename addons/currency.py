#!/usr/bin/env python3.6
import datetime
import os
import discord
from discord.ext import commands

class Currency:
    """
    Currency commands
    """

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))
        
    @commands.command()
    async def test2(self, ctx):
        """test"""
        return await ctx.send("ls: {}".format(os.listdir(path)))
        
def setup(bot):
    bot.add_cog(Currency(bot))
