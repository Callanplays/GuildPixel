# Standard library imports
import contextlib
import json
import multiprocessing
import os
import sys
import traceback
from datetime import datetime

import discord
import pytz
import requests

# Related third-party imports
from colorama import Fore
from discord.ext import commands, tasks
from flask import Flask

# Discord bot setup
bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
# Flask app setup
app = Flask(__name__)
@app.route('/')
def hello():
    return "Hello, World!"
# Function to run Flask app
def run_flask():
    app.run(host='0.0.0.0', port=8080)
  
bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
intents = discord.Intents.default()
intents.members = True

API_KEY = '20e3288b-276d-4445-96af-1b93802e6172'
whitelist = []
errorTooFast = {
    'success': False,
    'cause': 'You have already looked up this name recently'
}
badapikey = {'success': False, 'cause': 'Invalid API key'}


#~~~RUNS BOT~~~~
def getguildcount(guildid):  #gets guild member count from Hypixel API
  with open("serverchannel.json",
            "r") as read_file:  #open the file to read the channels
    data = json.load(read_file)  #load the file
    global guildname
    guildname = data[guildid]['guildname']
  data = requests.get(
      url=f'https://api.hypixel.net/guild?key={API_KEY}&name={guildname}',
      params={
          "key": f'{API_KEY}'
      }).json()
  if data["success"] is True:
    guild = data['guild']
    guild = guild['members']
    membercount = len(guild)
    return membercount
  else:
    print(data["success"])
    print(f'Failed to fetch data, reason: {data["cause"]}')
    return 'N/A'


def getservercount():  #gets member count in the discord server
  for guild in bot.guilds:
    membercount = guild.member_count
    return membercount


def getdiscchannel(guildid):  #gets discord channel from json file
  with open("serverchannel.json", "r") as read_file:
    data = json.load(read_file)
    return data[guildid]['discchannel']


def getguildchannel(guildid):  #gets guild channel from json file
  with open("serverchannel.json", "r") as read_file:
    data = json.load(read_file)
    return data[guildid]['guildchannel']



@tasks.loop(seconds=3600.0)
async def countermainloop():  # loop that consistently updates channel
  for guild in bot.guilds:
    discordmemb = None
    guildmemb = None
    # Attempt to get the discord channel and swallow any exceptions
    with contextlib.suppress(Exception):
      discordmemb = bot.get_channel(getdiscchannel(f'{guild.id}'))
    # Attempt to get the guild channel with the same strategy
    with contextlib.suppress(Exception):
      guildmemb = bot.get_channel(getguildchannel(f'{guild.id}'))
    # Get member counts
    guildmembers = getguildcount(f'{guild.id}')  # gets guild member count
    discmembers = getservercount()  # gets discord member count
    # Edits both channels if the variables have been successfully assigned
    # and if the channels are VoiceChannels
    if discordmemb is not None and isinstance(discordmemb, discord.VoiceChannel):
      try:
          await discordmemb.edit(name=f'Discord Members: {discmembers}')
      except discord.Forbidden:
          print(f"Do not have permissions to edit channel names in guild {guild.name}.")
    if guildmemb is not None and isinstance(guildmemb, discord.VoiceChannel):
      try:
          await guildmemb.edit(name=f'Guild Members: {guildmembers}')
      except discord.Forbidden:
          print(f"Do not have permissions to edit channel names in guild {guild.name}.")
    #Logs Changes in Console
    tz_Ch = pytz.timezone('America/Chicago')
    time_Ch = datetime.now(tz_Ch)
    time = time_Ch.strftime("%H:%M:%S")
    print(f'Updated with {discmembers} discord members and {guildmembers} guild members at {time} CST in guild {guild.name}')

@bot.event
async def on_ready():
  await load_extensions()
  print(f'{Fore.BLUE}Logged on as {bot.user}!{Fore.WHITE}')
  global myguild
  myguild = bot.get_guild(973721507282972682)
  if myguild is None:
    print('The bot is not connected to a guild.')
    return
  

  global modlogchannel
  modlogchannel = bot.get_channel(975527334373380137)
  global gangrole
  gangrole = myguild.get_role(1153835803106091008)
  countermainloop.start()

  await bot.change_presence(activity=discord.Activity(
      type=discord.ActivityType.playing,
      name="the game of life |by Callan v3.0\nPrefix: ?"))


@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    if "??" in str(ctx.message.content):
      pass
    else:
      await ctx.send(
          "**Command not found! please check the spelling carefully**")
      print(ctx.message.content)
  elif isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
    return await ctx.send("You dont have the correct role to use this command!"
                          )
  elif isinstance(error, (commands.MissingRequiredArgument)):
    return await ctx.send("Please put the correct arguments!")
  else:
    #All other Errors not returned come here and we can just print the default Traceback
    print('Ignoring exception in command {}:'.format(ctx.command),
          file=sys.stderr)
    traceback.print_exception(type(error),
                              error,
                              error.__traceback__,
                              file=sys.stderr)


async def load_extensions():
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      # cut off the .py from the file name
      try:
        await bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"{Fore.LIGHTBLUE_EX}{filename} was loaded.{Fore.WHITE}")
      except Exception as e:
        print(f"{Fore.RED}Oh no! {e}")
        print(f"{Fore.RED}{filename} could not be loaded.{Fore.WHITE}")


if __name__ == "__main__":
  # Start the Flask app in a separate process
  flask_process = multiprocessing.Process(target=run_flask)
  flask_process.start()

  # Run the Discord bot
  bot.run(os.environ["DISCORD_TOKEN"])