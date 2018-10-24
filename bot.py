import os

import discord

TOKEN = os.environ['token']
client = discord.Client()
count = 0


async def on_ready():
    try:
        print(client.user.name)
        print(client.user.id)
        print('Discord.py Version: {}'.format(discord.__version__))
        print('')

    except Exception as e:
        print(e)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if 'oof' in message.content.lower():
        msg = 'OOF count : {}'.format(update_count())
        await client.send_message(message.channel, msg)


# TODO add postgress support
def update_count():
    return 1


client.run(TOKEN)
