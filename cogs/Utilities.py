import json
import random
import time

import discord
from discord.ext import commands
from replit import db

with open("advmessages.json", "r") as file:
  advmessages = json.load(file)

guild = advmessages["guild"]
descriptionGuild1 = advmessages["descriptionGuild1"]
descriptionGuild2 = advmessages["descriptionGuild2"]
hook = advmessages["hook"]
hook2 = advmessages["hook2"]
tempdict = {}


class Utilities(commands.Cog):
  """Basic utility commands as well as developer commands."""

  def __init__(self, bot):
    self.bot = bot

  #initiates the cog
  @commands.command(
      name='advmsg',
      help=('Generate a guild advertisement message created just for you!'
            'True: Lowercase ONLY, False: Lowercase and Uppercase'),
  )
  async def AdvertiseMessage(self, ctx, arg1=False, arg2 =1):
    for _ in range(0,arg2):
      firstDescription = descriptionGuild2[random.randint(
          0,
          len(descriptionGuild2) - 1)]
      secondDescription = None
      while True:
        secondDescription = descriptionGuild2[random.randint(
            0,
            len(descriptionGuild2) - 1)]
        if secondDescription != firstDescription:
          break
      message = (
          f"/ac {hook[random.randint(0, len(hook)-1)]} "
          f"{hook2[random.randint(0, len(hook2)-1)]} "
          f"{descriptionGuild1[random.randint(0, len(descriptionGuild1)-1)]} "
          f"with {firstDescription}, "
          f"{secondDescription}, and more, if that sounds fun /p me!")
      if arg1:
        await ctx.send(message.lower())
        time.sleep(0.35)
      else:
        await ctx.send(message)
        time.sleep(0.35)

  @commands.command(
      name='score',
      help='Question of the Day points! Run ?score help for more info')
  async def Score_CMDS(self, ctx, arg1, name=''):
    #-score check subcommand
    if arg1 == 'check' and name == '':  #score check command
      try:
        embed = discord.Embed(title="Checked:", color=discord.Color.green())
        embed.add_field(name="Here you go!",
                        value=str(ctx.author.name) + " has " +
                        str(db[ctx.author.name]) + " points!")
        await ctx.send(embed=embed)
      except KeyError:
        embed = discord.Embed(title="Checked:", color=discord.Color.red())
        embed.add_field(name="Oh no!", value="User is not on the leaderboard!")
        await ctx.send(embed=embed)

    if arg1 == 'check' and name != '':
      try:
        embed = discord.Embed(title="Checked:", color=discord.Color.green())
        embed.add_field(name="Here you go!",
                        value=str(name) + " has " + str(db[name]) + " points!")
        await ctx.send(embed=embed)
      except KeyError:
        embed = discord.Embed(title="Checked:", color=discord.Color.red())
        embed.add_field(name="Oh no!", value="User is not on the leaderboard!")
        await ctx.send(embed=embed)

    if arg1 == 'leaderboard' or arg1 == 'lb':  #score leaderboard command
      lblist = dict(db)
      print("dictionary saved")
      lblistsort = sorted(lblist.items(), key=lambda x: x[1], reverse=True)
      print("sorted list")
      print(lblistsort)
      string = ''
      string = '\n'.join([f"{name} : {score}" for name, score in lblistsort])
      print('appending string')
      print('assembling embed')
      lbembed = discord.Embed(title="QOTD Leaderboard!",
                              color=discord.Color.blurple())
      lbembed.add_field(name="", value=str(string))
      print('sending')
      await ctx.send(embed=lbembed)

    if arg1 == 'help':  #score help command
      helpembed = discord.Embed(title="QOTD Help!", color=discord.Color.blue())
      helpembed.add_field(
          name="Help for the ?score command!",
          value=
          "`?score help`: Shows this command.\n\n`?score leaderboard OR lb`: Shows the total leaderboard, self explanatory.\n\n`?scoreup <score> <user> (optional)`: Increases the score by an amount to yourself or a <user>. ***REQUIRES QOTD ACCESS***\n Example: `?scoreup 10 callanftw`, increases callanftw\'s score by 10. *Note: When increasing others scores, make sure to use their new discord name, not their \"nickname\" or \"server nickname\".*\n\n`?scoreclear <user> (optional)`: Clears a <user>\'s score, or your score if used without an argument. ***REQUIRES QOTD ACCESS***\n\n`?score check <user> (optional)`: Shows the score of a <user>. Checks own user if not used without an argument."
      )
      await ctx.send(embed=helpembed)

  @commands.command(name='scoreclear',
                    help='subcommand of `?score`, requires DUCK role')
  @commands.has_any_role("DUCK", "Owner/Fallen Master")
  async def score_clear(self, ctx, *, name=''):
    if name == '':
      try:
        del db[ctx.author.name]
        await ctx.send(str(ctx.author.name) + "\'s score was cleared")

      except KeyError:
        await ctx.send((str(ctx.author.name) + " was not on the leaderboard"))

    if name != '':
      try:
        del db[name]
        await ctx.send((str(name) + "\'s score was cleared"))
      except KeyError:
        await ctx.send((str(name) + " was not on the leaderboard"))
    else:
      await ctx.send("**Command not found!**")

  @commands.command(name='scoreup',
                    help='subcommand of ?score, also requires DUCK role.')
  @commands.has_any_role("DUCK", "Owner/Fallen Master")
  async def Score_Help(self, ctx, number='', *, name=''):
    if number == '':
      await ctx.send('Please make sure to put how much to increase score by!')
    if number != '':
      if int(number) % 1 != 0:
        await ctx.send('The score must be a number!')
      if name == '':  #for own person
        try:
          db[ctx.author.name] = int(db[ctx.author.name]) + int(
              number)  #set author's score to current author score plus number
          await ctx.send((str(ctx.author.name) + " now has " +
                          str(db[ctx.author.name]) + " points!"))
        except KeyError:
          try:
            await ctx.send("New user detected, " + (str(ctx.author.name)) +
                           " has " + str(int(number)) + " points!")
            db[str(ctx.author.name)] = int(number)
          except ValueError:
            await ctx.send(
                'I\'m sorry, make sure you put how much to increase score by!')
            print("bruh")

        try:
          db[name] = int(db[name]) + int(number)
          await ctx.send((str(name) + " now has " + str(number) + " points!"))
        except ValueError:
          await ctx.send('Make sure you\'re typing ?scoreup <points> <person>!'
                         )
        except KeyError:
          try:

            db[name] = int(number)

            await ctx.send(("New person, " + str(name) + " has " +
                            str(number) + " points!"))

          except ValueError:
            await ctx.send(
                'I\'m sorry, make sure you put how much to increase score by!')

  #@commands.command(number='dailyscore', help='Requires qotd access')
  #@commands.has_role("qotd access")
  #async def dailyscore(self, ctx):
  #  with open('qotdpoints.json', 'r') as openfile:
  #      lblist = json.load(openfile)
  #      string= ''
  #      for item in lblist:
  #        string += item + ' : ' + str(lblist[item]) + '\n    '
  #  channel = ctx.guild.get_channel(975550528358608966)
  #  print(channel)
  #  await channel.send("Our question of the day has ended!")
  #  await channel.send("**Current leaderboard is:** \n    " + str(string))

  #custom crypt command
  @commands.command(name='crypt',
                    help="?crypt <Minecraft IGN> to link skycrypt")
  async def crypt(self, ctx, *, playername=''):
    if playername == '':
      embedyes = discord.Embed(title="Wrong Arguments",
                               color=discord.Color.blue())
      embedyes.add_field(name="Use ?crypt <Minecraft IGN>", value='   ')
      await ctx.send(embed=embedyes)
    else:
      await ctx.send(f'https://sky.shiiyu.moe/stats/{playername}')

  #custom ping command
  @commands.command(name='ping', help="Returns the bot's latency")
  async def ping_cmd(self, ctx):
    await ctx.send('Pong! {0}ms latency!'.format(round(self.bot.latency, 3)))


async def setup(bot):
  await bot.add_cog(Utilities(bot))
