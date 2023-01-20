import os
import discord
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


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

  if message.content == '$help':
    await message.channel.send('Hi! I am AkhilBot. These are a list of commands I can use: ')

  if message.content.startswith('i am racist'):
    await message.channel.send('yooo me too')

  if message.content.startswith('kys daniel'):
    await message.channel.send('fr i agree kys daniel')

  if message.content.startswith('embed'):
    await message.channel.send(embed)

keep_alive()
client.run(os.environ['TOKEN'])
