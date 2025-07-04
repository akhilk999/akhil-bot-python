import os
import discord
from discord.ext import commands
from discord.utils import find
# from keep_alive import keep_alive
from dotenv import load_dotenv
import re

load_dotenv()
token=os.getenv("TOKEN")

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
intents.typing = False
intents.presences = False
intents.reactions = True

hi_re = r"(?i)( |^)hi( |$)"
bye_re = r"(?i)( |^)bye( |$)"
snipe_message = None
snipe_author = None

count = 0

#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='&',
                      help_command=commands.MinimalHelpCommand(),
                      activity=discord.Game(name="&help"),
                      intents=intents)


#overrides page formatting for MinimalHelpCommand -> puts each page in an embed
class MyNewHelp(commands.MinimalHelpCommand):
  async def send_pages(self):
    destination = self.get_destination()
    for page in self.paginator.pages:
      emby = discord.Embed(description=page)
      await destination.send(embed=emby)

client.help_command = MyNewHelp()

class MyHelp(commands.HelpCommand):
  def get_command_signature(self, command):
    return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

  #overall help command
  async def send_bot_help(self, mapping):
    embed = discord.Embed(title="Help", color=discord.Color.blurple())
    for cog, commands in mapping.items():
      filtered = await self.filter_commands(commands, sort=True)
      command_signatures = [self.get_command_signature(c) for c in filtered]
      if command_signatures:
        cog_name = getattr(cog, "qualified_name", "No Category")
        embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
    channel = self.get_destination()
    await channel.send(embed=embed)

  #help for a certain command
  async def send_command_help(self, command):
    embed = discord.Embed(title=self.get_command_signature(command), color=discord.Color.random())
    if command.help:
      embed.description = command.help
    if alias := command.aliases:
      embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

    channel = self.get_destination()
    await channel.send(embed=embed)

  #helper function to add commands to embed
  async def send_help_embed(self, title, description, commands):
    embed = discord.Embed(title=title, description=description or "No help found...")
    if filtered_commands := await self.filter_commands(commands):
      for command in filtered_commands:
        embed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")
    await self.get_destination().send(embed=embed)
    
  async def send_group_help(self, group):
    title = self.get_command_signature(group)
    await self.send_help_embed(title, group.help, group.commands)

  async def send_cog_help(self, cog):
    title = cog.qualified_name or "No"
    await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.tree.sync()


#bot joins server
@client.event
async def on_guild_join(guild):
  general = find(lambda x: x.name == 'general', guild.text_channels)
  if general and general.permissions_for(guild.me).send_messages:
    await general.send('Hello {}!'.format(guild.name))


#member joins server
@client.event
async def on_member_join(member):
  welcome_channel = client.get_channel(1051917990096019478)
  print(f"{member} has joined!")
  await welcome_channel.send(
    f"{member.mention} has joined the server! Thank you!!")


#member leaves server
@client.event
async def on_member_remove(member):
  welcome_channel = client.get_channel(1051917990096019478)
  print(f"{member} has left!")
  await welcome_channel.send(
    f"{member.mention} has left the server! (finally :rofl:)")


#message is deleted
@client.event
async def on_message_delete(message):
  global snipe_message, snipe_author

  snipe_message = message.content
  snipe_author = message.author


#when a message is sent
@client.event
async def on_message(message):
  global count
  count += 1
  #returns nothing if message is from bot
  if message.author == client.user:
    return

  #random message every 1000 messages
  if count == 1000:
    await message.channel.send('I know what you did.')
    count = 0

  #message contains hi -> fr i agree + message
  if re.search(hi_re, message.content):
    await message.channel.send('fr i agree ' + message.content)

  #message contains bye -> girl bye...
  if re.search(bye_re, message.content):
    await message.channel.send('girl bye...')

  if message.content.startswith('real'):
    await message.channel.send('real')

  # process commands
  await client.process_commands(message)


#client.remove_command('help')

#commands


@client.hybrid_command()
async def profile(ctx, member: discord.Member = None):
  if not member:
    member = ctx.author
  userAvatar = member.avatar
  embed = discord.Embed()
  embed.set_image(url=userAvatar)
  await ctx.send(embed=embed)


@client.hybrid_command()
async def snipe(ctx):
  if snipe_message == None:
    embed = discord.Embed(description="No snipe available")
  else:
    pfp = snipe_author.avatar
    embed = discord.Embed(description=f"{snipe_message}")
    embed.set_author(name=f"{snipe_author}", icon_url=pfp)
  await ctx.send(embed=embed)


# keep_alive()
client.run(token)
