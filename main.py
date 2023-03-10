import os
import discord
from discord.ext import commands
from discord.utils import find
from keep_alive import keep_alive

token = os.environ['TOKEN']

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
intents.typing = False
intents.presences = False
intents.reactions = True

#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='&', help_command=commands.MinimalHelpCommand(), activity = discord.Game(name="&help"), intents=intents)

#overrides page formatting for MinimalHelpCommand -> puts each page in an embed
class MyNewHelp(commands.MinimalHelpCommand):
  async def send_pages(self):
    destination = self.get_destination()
    for page in self.paginator.pages:
      emby = discord.Embed(description=page)
      await destination.send(embed=emby)
client.help_command = MyNewHelp()

class MyHelp(commands.HelpCommand):
  async def send_bot_help(self, mapping):
    embed = discord.Embed(title="Help")
    for cog, commands in mapping.items():
      command_signatures = [self.get_command_signature(c) for c in commands]
      if command_signatures:
        cog_name = getattr(cog, "qualified_name", "No Category")
        embed.add_field(name=cog_name, value)
    channel = self.get_destination()
    await channel.send(embed=embed)



async def embed():
  embed=discord.Embed(title="Sample Embed",  url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and     the different components", color=0xFF5733)
  await embed

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

#bot joins server
@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {}!'.format(guild.name))

#member joins server
@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(1051917990096019478)
    print(f"{member} has joined!")
    await welcome_channel.send(f"{member.mention} has joined the server! Thank you!!")

#member leaves server
@client.event
async def on_member_remove(member):
  welcome_channel = client.get_channel(1051917990096019478)  
  print(f"{member} has left!")
  await welcome_channel.send(f"{member.mention} has left the server! (finally :rofl:)")


#message is deleted
@client.event
async def on_message_delete(message):
  await message.channel.send(f"Message: \"{message.content}\" was deleted\nMessage by: {message.author}")

#when a message is sent
@client.event
async def on_message(message):   
  if message.author == client.user:
    return 

  if message.content.startswith('i am racist'):
    await message.channel.send('yooo me too')

  if message.content.startswith('hi'):
    await message.channel.send('fr i agree '+message.content)

  if message.content.startswith('real'):
    await message.channel.send('real')

  if message.content.startswith('embed'):
    await message.channel.send(embed=embed())

  # process commands
  await client.process_commands(message)

#client.remove_command('help')
    
#commands
#@client.command()
#async def help(ctx):
 # await ctx.send('Hi! I am AkhilBot. These are a list of commands I can use: ')
  
keep_alive()
client.run(token)
