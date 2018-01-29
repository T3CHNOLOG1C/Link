#!/usr/bin/env python3.6
import os
import configparser
import asyncio
import traceback
import json
import copy
from subprocess import call
from os import execv
from sys import argv
import discord
from discord.ext import commands

# Change to script's directory
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

bot_prefix = ["l.", "<@406073912406048769> "]
bot = commands.Bot(command_prefix=bot_prefix, description="Link, a general purpose bot.", max_messages=10000, pm_help=None)

# Read config.ini
config = configparser.ConfigParser()
config.read("config.ini")


bot.errorlogs_channel = discord.utils.get(guild.text_channels, name="{}".format(config['Channels']['ErrorLogs']))

# Handle errors
# Taken from 
# https://github.com/916253/Kurisu/blob/31b1b747e0d839181162114a6e5731a3c58ee34f/run.py#L88
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.errors.CommandNotFound):
        pass  # ...don't need to know if commands don't exist
    if isinstance(error, commands.errors.CheckFailure):
        await bot.send_message(ctx.message.channel, "{} You don't have permission to use this command.".format(ctx.message.author.mention))
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        formatter = commands.formatter.HelpFormatter()
        await bot.send_message(ctx.message.channel, "{} You are missing required arguments.\n{}".format(ctx.message.author.mention, formatter.format_help_for(ctx, ctx.command)[0]))
    else:
        bot.errorlogs_channel.send("An error occurred while processing the `{}` command.".format(ctx.command.name))
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        print(''.join(tb))
        
@bot.event
async def on_ready():
    for guild in bot.guilds:
        bot.guild = guild

        
# Load addons
addons = [
    'addons.misc',
    'addons.currency',
]

for addon in addons:
    try:
        bot.load_extension(addon)
    except Exception as e:
        print("Failed to load {} :\n{} : {}".format(addon, type(e).__name__, e))

bot.all_ready = True

print("Client logged in.")
    
    
# Core commands
@bot.command(hidden=True)
async def unload(ctx, addon: str):
    """Unloads an addon."""
    user = ctx.message.author
    if user.id == 208370244207509504:
        try:
            addon = "addons." + addon
            bot.unload_extension(addon)
            await ctx.send('✅ Addon unloaded.')
        except Exception as e:
            await ctx.send('💢 Error trying to unload the addon:\n```\n{}: {}\n```'.format(type(e).__name__, e))

@bot.command(name='reload', aliases=['load'], hidden=True)
async def reload(ctx, addon : str):
    """(Re)loads an addon."""
    user = ctx.message.author
    if user.id == 208370244207509504:
        try:
            addon = "addons." + addon
            bot.unload_extension(addon)
            bot.load_extension(addon)
            await ctx.send('✅ Addon reloaded.')
        except Exception as e:
            await ctx.send('💢 Failed!\n```\n{}: {}\n```'.format(type(e).__name__, e))

@bot.command(hidden=True, name="pull", aliases=["pacman"])
async def pull(ctx, pip=None):
    """Pull new changes from Git and restart.\nAppend -p or --pip to this command to also update python modules from requirements.txt."""
    user = ctx.message.author
    if user.id == 208370244207509504:
        await ctx.send("`Pulling changes...`")
        call(["git", "stash", "save"])
        call(["git", "pull"])
        call(["git", "stash", "clear"])
        pip_text = ""
        if pip == "-p" or pip == "--pip" or pip == "-Syu":
            await ctx.send("`Updating python dependencies...`")
            call(["python3.6", "-m", "pip", "install", "--user", "--upgrade", "-r",
                "requirements.txt"])
            pip_text = " and updated python dependencies"
        await ctx.send("Pulled changes{}! Restarting...".format(pip_text))
        execv("python3.6 Link.py", argv)
    else:
        if "pacman" in ctx.message.content:
            await ctx.send("`{} is not in the sudoers file. This incident will be reported.`".format(ctx.message.author.display_name))
        else:
            await ctx.send("Only the bot owner can use this command.")

@bot.command()
async def restart(ctx):
    """Restart the bot (Staff Only)"""
    user = ctx.message.author
    if user.id == 208370244207509504:
        await ctx.send("`Restarting, please wait...`")
        execv("python3.6 Link.py", argv)

# Run the bot
bot.run(config['Main']['token'])	
