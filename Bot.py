''' 
Program for a Basic Discord Bot
'''
import discord
from discord.ext import commands
import json
import youtube_dl
import random

#Making an instance of class Bot 
client=commands.Bot(command_prefix = "!")
#Removing Default Help Command so we can add our own
client.remove_command("help")
players = {}

#Opening json file with token and swearwords
with open('C:\\Users\\troge\\Projects\\Discord\\config.json','r') as config:
	jsonfile = json.loads(config.read())
	token = jsonfile['TOKEN']
	badwords = jsonfile['Bad_Words']
	serverid = jsonfile['Server_Id']

#Prints Bot is Online 
@client.event
async def on_ready():
	for guild in client.guilds:
		if(guild.name == serverid):
			break
	print(f"{client.user} is connected to the following guild:")
	print(f"{guild.name} (id: {guild.id})")
	members= '\n - '.join([member.name for member in guild.members])
	print(f"Guild Members:\n - {members}")
	await client.change_presence(status = discord.Status.idle, activity = discord.Game(name = 'Fortnut'))
	print("Bot is Online")

#Greets New Users
@client.event 
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(f"Hi {member.name}, welcome to our Guild!")
	for channel in member.guild.channels:
		if (str(channel) == "voidmain"):
			await channel.send(f"Welcome to the server {member.mention}")

#Shows Which Member Was removed		
@client.event
async def on_member_remove(member):
	for channel in member.guild.channels:
		if (str(channel) == "voidmain"):
			await channel.send(f"{member.mention} Was kicked RIP")
	
		
#Shows Who wrote what on terminal and Censors Bad Words			
@client.event 
async def on_message(message):
	if(message.author == client.user):
		return	
	author = message.author
	content = message.content
	channel = message.channel
	#Check if entered message  had a slang
	if(message.content in badwords):
		await message.channel.purge(limit = 1)
	print(f'{author}: {content}')
	#To check if message contains valid command
	await client.process_commands(message)

#Shows What Was deleted by who on terminal	
@client.event 
async def on_message_delete(message):
	author = message.author
	content = message.content
	channel = message.channel
	print(f"{author} deleted message: {content}")

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Please Pass in all required arguments")

@client.command()
async def help(ctx):
	embed = discord.Embed(
	title = "Help On I'maBot",
	description = "Some Useful Commands(Commands start with !)\n",
	colour = discord.Colour.red()
	)
	embed.add_field(name = "users", value = "Shows Total Number of Users in The server", inline = False)
	embed.add_field(name = "ping", value = "Shows the Bot's Ping to the server\n", inline = False)
	embed.add_field(name = "clear", value = "Clears Messages According to the value after command", inline = False)
	embed.add_field(name = "noice", value = "Try it", inline = False)
	embed.add_field(name = "echo", value = "Echo!!!", inline = False)
	embed.add_field(name = "ninenine", value = "NINE-NINE", inline = False)
	embed.add_field(name = "99", value = "B99 Quotes", inline = False)
	embed.set_author(name = "I'mTHEBot" , icon_url = "https://mpng.pngfly.com/20180709/ysa/kisspng-discord-internet-bot-computer-software-teamspeak-c-discord-icon-circle-5b42ddfd4ae4a3.8911388115311088613068.jpg")
	await ctx.send(content = None, embed=embed)

@client.command(name='99')
async def nine_nine(ctx):
	b99quotes=["I'm the human form of the 💯 emoji.","Bingpot!","Cool. Cool cool cool cool cool cool cool","no doubt no doubt no doubt no doubt"]
	response = random.choice(b99quotes)
	await ctx.send(response)

@client.command()
async def users(ctx):
	#Shows Total Number of Users in The server
	id = client.get_guild(int(serverid))
	await ctx.send(f"Total Number of Members: {id.member_count}")

@client.command()
async def ping(ctx):
	#Shows the Bot's Ping to the server
    await ctx.send(f"Pong! {int(client.latency*1000)}ms")

@client.command()
async def clear(ctx, amount = 2):
	#Clears Messages According to the value after command Else Clears a message
	if (amount == 0):
		await ctx.send(f"You cannot delete 0 messages")
	else:
		amount += 1
		await ctx.channel.purge(limit = amount)

@client.command()
async def noice(ctx):
	#Prints Toit!
    await ctx.send("Toit!")

@client.command()
async def echo(ctx,*args):
	#Repeats The message
	output = ''
	for word in args:
		output+=(word+' ') 
	await ctx.send(output)

@client.command()
async def ban(ctx, member : discord.Member, *, reason = None):
	await member.ban(reason = reason)

@client.command()
async def kick(ctx, member : discord.Member, * , reason = None):
	await member.kick(reason = reason)

@client.command()
async def ninenine(ctx):
		await ctx.send("NINE-NINE")

@client.command(pass_context = True)
async def play(ctx,url):
	guild = ctx.message.guild
	voice_client = guild.voice_client
	player = await voice_client.create_ytdl_player(url)
	players[guild.id] = player
	player.start()
	
@client.command()
async def  logout(ctx):
	#Turns Bot OFF
	await client.logout()
	
client.run(token)