import os
import discord
from discord.ext import commands
from discord.utils import find
from keep_alive import keep_alive

token = os.environ['TOKEN']
#prefix = os.environ['PREFIX']

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
intents.typing = False
intents.presences = False
intents.reactions = True

#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='&', activity = discord.Game(name="&help"), intents=intents)

async def embed():
  embed=discord.Embed(title="Sample Embed",  url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and     the different components", color=0xFF5733)
  await channel.send(embed=embed)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):   
  if message.author == client.user:
    return 

  if message.content == '&help':
    await message.channel.send('Hi! I am AkhilBot. These are a list of commands I can use: ')

  if message.content.startswith('i am racist'):
    await message.channel.send('yooo me too')

  if message.content.startswith('hi'):
    await message.channel.send('fr i agree '+message.content)

  if message.content.startswith('real'):
    await message.channel.send('real')

  if message.content.startswith('embed'):
    await message.channel.send(embed)

#@client.command
#async def help
@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {}!'.format(guild.name))

@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(1051917990096019478)
    print(f"{member} has joined!")
    await welcome_channel.send(f"{member.mention} has joined the server! Thank you!!")

@client.event
async def on_member_remove(member):
  welcome_channel = client.get_channel(1051917990096019478)  
  print(f"{member} has left!")
  await welcome_channel.send(f"{member.mention} has left the server! (finally :rofl:)")

@client.event
async def on_message_delete(message):
  await message.channel.send(f"Message: \"{message.content}\" was deleted\nMessage by: {message.author}")

keep_alive()
client.run(token)
