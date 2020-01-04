''' 
Program for a Basic Discord Bot
'''
import discord
from discord.ext import commands
import json

client=commands.Bot(command_prefix = "~")

with open('C:\\Users\\troge\\Projects\\Discord\\config.json','r') as config:
	jsonfile = json.loads(config.read())
	token = jsonfile['TOKEN']
	badwords = jsonfile['Bad_Words']

@client.event
async def on_ready():
	print("Bot is Ready")
	
@client.event 
async def on_member_join(member):
	for channel in member.guild.channels:
		if (str(channel) == "voidmain"):
			await channel.send(f"Welcome to the server {member.mention}")
			
@client.event
async def on_member_remove(member):
		for channel in member.guild.channels:
			if (str(channel) == "voidmain"):
				await channel.send(f"{member.mention} Was kicked RIP")
			
@client.event 
async def on_message(message):
	author = message.author
	content = message.content
	channel = message.channel
	if(message.content in badwords):
		await message.channel.purge(limit = 1)
	print(f'{author}: {content}')
	#To check if message contains valid command
	await client.process_commands(message)
	
@client.event 
async def on_message_delete(message):
	author = message.author
	content = message.content
	channel = message.channel
	await channel.send(f'{author}: {content}')
	
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {int(client.latency*1000)}ms")

@client.command()
async def clear(ctx, amount = 5):
	if (amount == 0):
		await ctx.send(f"You cannot delete 0 messages")
	else:
		amount += 1
		await ctx.channel.purge(limit = amount)

@client.command()
async def noice(ctx):
    await ctx.send("Toit!")

	

@client.command()
async def echo(ctx,*args):
	output = ''
	for word in args:
		output+=(word+' ') 
	await ctx.send(output)

client.run(token)
