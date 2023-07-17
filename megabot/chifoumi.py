# -*- coding: utf-8 -*-

import random

chifoumi_options = {
    "pierre": "🗿 Pierre !",
    "feuille": "🍃 Feuille !",
    "ciseaux": "✂️ Ciseaux !",
}
userChifoumi_options = [
    "pierre",
    "ciseaux",
    "feuille",
]


def determine_result(user_choice, computer_choice):
    rules = {
        "pierre": {
            "pierre": "⚖️ égalité",
            "feuille": "☠️ défaite",
            "ciseaux": "🎉 victoire",
        },
        "feuille": {
            "pierre": "🎉 victoire",
            "feuille": "⚖️ égalité",
            "ciseaux": "☠️ défaite",
        },
        "ciseaux": {
            "pierre": "☠️ défaite",
            "feuille": "🎉 victoire",
            "ciseaux": "⚖️ égalité",
        },
    }

    result = rules[user_choice][computer_choice]
    return result


async def on_message(client, message):
    if message.author == client.user:
        return

    for user_choice in userChifoumi_options:
        if user_choice in message.content:
            response = random.choice(list(chifoumi_options.keys()))
            print(f"chifoumis {response}")
            await message.channel.send(chifoumi_options[response])
            result = determine_result(user_choice, response)
            await message.channel.send(result)
