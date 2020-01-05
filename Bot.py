''' 
Program for a Basic Discord Bot
'''
import discord
from discord.ext import commands
import json
import random
import requests,bs4

#Some Functions For Commands
#Prints movie review from imdb
def movie_review(mov):
	res=requests.get('https://www.google.com/search?q='+mov)
	soup=bs4.BeautifulSoup(res.text,'html.parser')
	for link in soup.find_all('div',class_='kCrYT'):
		try:
			if('imdb' in link.a['href']):
				moviereq=requests.get('http://google.com'+link.a['href'])  
				break
			else:
				moviereq=False
		except:
			continue
	if(moviereq!=False):
		soupm=bs4.BeautifulSoup(moviereq.text,'html.parser')
		summary=soupm.find('div',class_='summary_text')
		return(summary.text.strip())
	else:
		return("Movie Not Found")

#Prints First Link on Google.com		
def first_link(link, platform = ""):
	link = link + f"+{platform}"
	res = requests.get(link)
	yousoup =  bs4.BeautifulSoup(res.text, "html.parser")
	for item in yousoup.find_all('div',class_='kCrYT'):
		try:
			if(platform in item.a["href"]):
				return "http://google.com"+item.a["href"]
		except:
			continue
	return "Link Not Found"

#Get's the lyrics of songs
def song_lyrics(song):
	res=requests.get("https://www.google.com/search?q="+song+" lyrics")
	linksoup=bs4.BeautifulSoup(res.text,"html.parser")
	lyrics=linksoup.find('div',class_='hwc')

	if lyrics!=None:
		try:
			if lyrics.div.div.div.text != None:
				return(lyrics.div.div.div.text)
		except:
			return("Song Not Found")
	else:
		return("Song Not Found")

#Making an instance of class Bot 
client=commands.Bot(command_prefix = "!")
#Removing Default Help Command so we can add our own
client.remove_command("help")

#Opening json file with token, swearwords and Server ID
with open("C:\\Users\\troge\\Projects\\Discord\\config.json",'r') as config:
	jsonfile = json.loads(config.read())
	token = jsonfile["TOKEN"]
	badwords = jsonfile["Bad_Words"]
	serverid = jsonfile["Server_Id"]

#Prints Bot is Online 
@client.event
async def on_ready():
	#checking if server matches with id
	for guild in client.guilds:
		if(guild.name == serverid):
			break
	print(f"{client.user} is connected to the following guild:")
	print(f"{guild.name} (id: {guild.id})")
	members= '\n - '.join([member.name for member in guild.members])
	print(f"Guild Members:\n - {members}")
	#Changing Bot's Status
	await client.change_presence(status = discord.Status.idle, activity = discord.Game(name = "Fortnut"))
	print("Bot is Online")

#Greets New Users
@client.event 
async def on_member_join(member):
	#Prints on terminal
	print(f"{member.mention} has Joined the server")
	#Sends Direct Message
	await member.create_dm()
	await member.dm_channel.send(f"Hi {member.name}, welcome to our Guild!")
	#Greets On Main Channel
	for channel in member.guild.channels:
		if (str(channel) == "voidmain"):
			await channel.send(f"Welcome to the server {member.mention}")

#Shows Which Member Was removed on server
@client.event
async def on_member_remove(member):
	#Prints on terminal
	print(f"{member.mention} has left the server")
	#Says on Main Channel
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
	if(str(message.content).lower() in badwords):
		await message.channel.purge(limit = 1)
		await author.create_dm()
		await author.dm_channel.send(f"Dear {author}, Please refrain from using Cursewords in our Server!")
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

#Checking For Errors
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Please Pass in all required arguments")

#Making Custom Help command
@client.command()
async def help(ctx):
	embed = discord.Embed(
	title = "Help On I'maBot",
	description = "Some Useful Commands(Commands start with !)\n",
	colour = discord.Colour.red()
	)
	embed.set_author(name = "I'mTHEBot" , icon_url = "https://mpng.pngfly.com/20180709/ysa/kisspng-discord-internet-bot-computer-software-teamspeak-c-discord-icon-circle-5b42ddfd4ae4a3.8911388115311088613068.jpg")
	embed.set_thumbnail(url = "https://mpng.pngfly.com/20180709/ysa/kisspng-discord-internet-bot-computer-software-teamspeak-c-discord-icon-circle-5b42ddfd4ae4a3.8911388115311088613068.jpg")
	embed.add_field(name = "users", value = "Shows Total Number of Users in The server", inline = False)
	embed.add_field(name = "ping", value = "Shows the Bot's Ping to the server\n", inline = False)
	embed.add_field(name = "clear", value = "Clears Messages According to the value after command", inline = False)
	embed.add_field(name = "movie", value = "Shows Short Summary of Movie given After Command", inline = False)
	embed.add_field(name = "google", value = "Shows Google Search Top Result", inline = False)
	embed.add_field(name = "youtube", value = "Shows Youtube Link Given After Command", inline = False)
	embed.add_field(name = "song", value = "Shows the Lyrics of Song Given After Command", inline = False)
	embed.add_field(name = "noice", value = "Try it", inline = False)
	embed.add_field(name = "echo", value = "Echo!!!", inline = False)
	embed.add_field(name = "ninenine", value = "NINE-NINE", inline = False)
	embed.add_field(name = "99", value = "B99 Quotes", inline = False)
	await ctx.send(content = None, embed=embed)

@client.command(name='99')
async def nine_nine(ctx):
	#Simple Command Which Generates Random Brooklyn Nine Nine Quotes
	b99quotes=[
	"I'm the human form of the 💯 emoji.",
	"Bingpot!",
	"Cool Cool cool cool cool cool cool cool",
	"no doubt no doubt no doubt no doubt"
	]
	response = random.choice(b99quotes)
	await ctx.send(response)

@client.command()
async def ninenine(ctx):
	#Says NINE-NINE
	await ctx.send("NINE-NINE")

@client.command()
async def noice(ctx):
	#Prints Toit
	await ctx.send("Toit!!!")
	
@client.command()
async def echo(ctx,*args):
	#Repeats The message
	output = ''
	for word in args:
		output += (word + ' ') 
	await ctx.send(output)

@client.command()
async def youtube(ctx, *args):
	#Shows First Link On Google According To Command With Platfrom Youtube
	search_word = ''
	for word in args:
		search_word += (word + '+')
	link = "https://www.google.com/search?q=" + word
	link = first_link(link, "youtube.com")
	await ctx.send(f"{link}")	

@client.command()
async def google(ctx, *args):
	#Shows First Link On Google Accordint To Command
	search_word = ''
	for word in args:
		search_word += (word + '+')
	link = "https://www.google.com/search?q=" + word
	link = first_link(link)
	await ctx.send(f"{link}")

@client.command()
async def movie(ctx, *args):
	#Shows A short Summary of the movie given as an Arguments
	output = ''
	for word in args:
		output += (word + ' ') 
	review = movie_review(output)
	await ctx.send(review)

@client.command()
async def song(ctx, *args):
	#Prints the lyrics of song given
	output = ''
	for word in args:
		output += (word + ' ') 
	await ctx.send(song_lyrics(output))

@client.command()
async def users(ctx):
	#Shows Total Number of Users in The server
	id = client.get_guild(int(serverid))
	await ctx.send(f"Total Number of Members: {id.member_count}")

@client.command()
async def ping(ctx):
	#Prints Bot's latency to the server
	await ctx.send(f"Pong! {round(client.latency*1000)}ms")
	
@client.command()
async def clear(ctx, amount = 1):
	#Clears Messages According to the value after command Else Clears a message
	if (amount == 0):
		await ctx.send(f"You cannot delete 0 messages")
	else:
		amount += 1
		await ctx.channel.purge(limit = amount)

@client.command()
async def ban(ctx, member : discord.Member, *, reason = None):
	#Ban's User
	await member.ban(reason = reason)
	await ctx.send(f"Banned {member.mention}")

@client.command()
async def unban(ctx, * , member):
	#Unban User
	banned_users = await ctx.guild.bans()
	member_name,member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		if ((user.name, user.discriminator) == (member_name,member_discriminator)):
			await ctx.guild.unban(user)
			await ctx.send(f"Unbanned {user.mention}")
			return

@client.command()
async def kick(ctx, member : discord.Member, * , reason = None):
	#Kick User From Server
	await member.kick(reason = reason)

@client.command()
async def  logout(ctx):
	#Turns Bot OFF
	await ctx.send("Peace")
	await client.logout()
	
client.run(token)
