import discord
from discord.ext import commands
class Autoroles(commands.Cog):
  """Autoroles."""
  
  def __init__(self, bot):
    self.bot = bot
  def myguild(self):
    return self.bot.get_guild(973721507282972682)




  async def autorole_dungeon(self):
    classrole_ids = [
      1151732157304291368, 1151733954299306026, 1151733091220607036, 1151733734706520104,
      1151734417648263169
    ]
    classroles = []
    gangroles = []
    rolestoadd = []

    def formatit(a):
      classroles.extend(member.id for member in a.members
                        if member.id not in classroles)
      
      for role_id in classrole_ids:
        role = self.myguild().get_role(role_id)
        if role:
          formatit(role)
    rolestoadd = list(set(classroles) ^ set(gangroles))
    return rolestoadd

  

async def setup(bot):
  await bot.add_cog(Autoroles(bot))
