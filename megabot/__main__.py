# -*- coding: utf-8 -*-

import os
import random
import discord
from . import speaker
import asyncio
from dotenv import load_dotenv
from discord import Intents
from .chifoumi import on_message as chifoumi_on_message
from .bgg import on_message as bgg_on_message
from .diceRoll import evaluate_dice_expression
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PRIVATE_GUILDS = os.getenv("PRIVATE_GUILDS")

intents = Intents.default()
intents.members = True
intents.message_content = True
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="?", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, welcome to my Discord server!"
    )


@bot.command(
    name="chifoumi",
    help="Lance une partie de Chifoumi, aprés le message Chi..fou..mi..!"
    " choisis entre pierre, feuille ou ciseaux et ecris vite ton choix.",
)
async def chifoumi(ctx):
    await ctx.send("Chi..fou..mi..!")

    # for performance, you might need to move this function outside `chifoumi`
    # right now, this function is "created" each time `chifoumi` is called
    # better have a def check(message, ctx)
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        message = await bot.wait_for(
            "message", check=check, timeout=30
        )  # Attendre 30 secondes pour la réponse de l'utilisateur
        await chifoumi_on_message(bot, message)
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé, la partie est annulée.")


@bot.command(
    name="roll",
    help="Lance un dès ! Utilisez ?roll XdY,"
    " où X est le nombre de dés"
    " et Y est le nombre de faces.",
)
async def roll(ctx, dice: str):
    ctx.send(f"string parameter : {dice}")
    result = evaluate_dice_expression(dice)
    await ctx.send(result)


@bot.command(name="bgg", help="en cours de dev, utilisation de boardgamegeek")
async def bgg(ctx):
    await ctx.send("saisir un nom de user bgg: ")

    # for performance, you might need to move this function outside `bgg`
    # right now, this function is "created" each time `bgg` is called
    # better have a def check(message, ctx)
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        message = await bot.wait_for(
            "message", check=check, timeout=30
        )  # Attendre 30 secondes pour la réponse de l'utilisateur
        await bgg_on_message(ctx, bot, message)
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé, abandon de la demande.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("?"):
        await bot.process_commands(message)
    else:
        if message.guild and message.guild.name in PRIVATE_GUILDS:
            if "megabot test" in message.content:
                await message.channel.send('bot response test ACR4')
        if "un sort" in message.content:
            response = random.choice(speaker.sortileges)
            await message.channel.send(response)
        elif message.content == "error":
            raise discord.DiscordException


@bot.event
async def on_error(event, *args, **kwargs):
    with open("err.log", "a") as f:
        if event == "on_message":
            f.write(f"Unhandled message: {args[0]}\n")
        else:
            raise


bot.run(TOKEN)
