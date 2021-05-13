import discord
import json
from discord.ext import commands, tasks
from samp_client.client import SampClient

bot = commands.Bot(command_prefix='$', case_insensitive=True)



@bot.command() #SERVER INFO   --- $ip [ip] [port] 
async def ip(ctx,ADD,NUM):
    with SampClient(address=ADD, port=NUM) as client:
        info = client.get_server_info()
        rulevalue = [rule.value for rule in client.get_server_rules()]        
        await ctx.send(f'```Server: {info.hostname}\nIP: {ADD}:{NUM}\nPlayers: {info.players}/{info.max_players}\nGame Mode: {info.gamemode}\nLanguage: {info.language}\nCAC Version: {rulevalue[0]}\nLag Comp: {rulevalue[1]}\nMap: {rulevalue[2]}\nVersion: {rulevalue[3]}\nWeather: {rulevalue[4]}\nWeburl: {rulevalue[5]}\nWorld Time: {rulevalue[6]}```')

@ip.error
async def ip_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Usage: $ip [ip] [port]')


@bot.command() #SERVER INFO   ---   $players [ip] [port]
async def players(ctx,ADD,NUM):
    with SampClient(address=ADD, port=NUM) as client:
        info = client.get_server_info()
        players = [client.name for client in client.get_server_clients_detailed()]
        score = [client.score for client in client.get_server_clients_detailed()]
        playerping = [client.ping for client in client.get_server_clients_detailed()]
        res2 = [players[i] + " - " + str(score[i]) + " - " + str(playerping[i]) for i in range(len(players))]
        s = '\n'
        s = s.join(res2)
        await ctx.send(f'```Server: {info.hostname}\nPlayers: {info.players}/{info.max_players}\nIP: {ADD}\nGame Mode: {info.gamemode}\nLanguage: {info.language}```')
        await ctx.send(f'```--Player Name-- | --Score-- | --Ping--\n{s}```\n**Total Online: {info.players}**')

@players.error
async def players_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Usage: $players [ip] [port]')


#RCON COMMAND
@bot.command() # ----- $rcon [ip] [port] [rcon_password] [rcon_cmd]
async def rcon(ctx,ADD,NUM,PASS,*cmd):
    with SampClient(address=ADD, port=NUM, rcon_password=PASS) as client:
        conlist = '\n'.join(client.send_rcon_command(*cmd))
        await ctx.send(f'```{conlist}```')

@rcon.error
async def rcon_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Usage: $rcon [ip] [port] [rcon_password] [rcon_cmd]\n```For Ex:- $rcon 127.0.0.1 7777 nothing cmdlist```')


with open("./config.json", 'r') as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData["DISCORD_TOKEN"]

@bot.event
async def on_ready():
    activity = discord.Game(name="Made by DeViL#3078", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is Online!")

bot.run(TOKEN)