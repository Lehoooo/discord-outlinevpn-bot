import requests
import discord
from discord.ext import commands
import time
import os
import json
import asyncio

TOKEN = 'BOTTOKEN'
bot = commands.Bot(command_prefix='>')

managementurl = "MANAGEMENETURL"

print("Starting Outline Bot - Made By Leho")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Outline Key Manager"))
    print("Ready")


@bot.command()
async def getkeys(ctx):
    await ctx.send("Getting Keys, Please Wait")

    r = requests.get(managementurl + "/access-keys", verify=False).json()

    numberofkeys = len(r['accessKeys'])

    embed = discord.Embed(title="Outline Keys")

    for k in range(numberofkeys):
        key = r['accessKeys'][k]
        print(key)
        n = key['name']
        if n == "":
            n = "no name"
        embed.add_field(name=str(key['id'] + " - " + n), value=str(key['accessUrl']), inline=False)
        embed.set_footer(text="Made with ❤ by Leho")

    await ctx.send(embed=embed)


@bot.command()
async def genkey(ctx, arg):
    await ctx.send("Generating key for " + arg)
    requests.post(managementurl + "/access-keys", verify=False)



@bot.command()
async def delkey(ctx, arg):
    numbtest = isinstance(arg, (int, float))

    if numbtest == "false":
        await ctx.send("error")
    else:
        await ctx.send("Deleting Key " + arg)
        r = requests.delete(managementurl + "/access-keys/" + str(arg), verify=False)
        rtext = r.text
        if rtext == "":
            await ctx.send("Success")
        else:
            await ctx.send("Error. Response was: " + str(rtext))

@bot.command()
async def renamekey(ctx, arg, arg2):
    await ctx.send("Renaming Key " + arg + " to: " + arg2)
    r = requests.put(managementurl + "/access-keys/" + str(arg) + "/name", data={'name': str(arg2)}, verify=False)
    print(r.text)
    if r == "":
        print("Renamed Successfully")
        await ctx.send("Renamed Successfully")


bot.run(TOKEN)
