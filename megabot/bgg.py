# -*- coding: utf-8 -*-

# necessary : pip install requests-cache==0.4.4
import random
import asyncio
from boardgamegeek import BGGClient


async def on_message(ctx, client, message):
    if message.author == client.user:
        return

    bgg = BGGClient()
    await message.channel.send(
        f"Tu as demandé à charger la collection de : {message.content}"
    )
    collection = bgg.collection(message.content)
    await message.channel.send(
        "tu peux par exemple me demander un jeux aléatoire issue de cette collection."
    )

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        message = await client.wait_for(
            "message", check=check, timeout=30
        )  # Attendre 30 secondes pour la réponse de l'utilisateur
        if "aléatoire" in message.content:
            randomGame = random.choice(collection.items)
            await message.channel.send(f"Tu vas jouer à : {randomGame.name}")
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé, abandon de la demande.")
