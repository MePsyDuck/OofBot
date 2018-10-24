import os
import re

import discord
import psycopg2

TOKEN = os.environ['TOKEN']
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
conn.autocommit = True

client = discord.Client()


async def on_ready():
    try:
        print(client.user.name)
        print(client.user.id)
        print('Discord.py Version: {}'.format(discord.__version__))
        print('Hail Potato!')

    except Exception as e:
        print(e)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif has_oof(message.content):
        msg = '<:Oof:504616782695366657> count : {}'.format(update_count())
        await client.send_message(message.channel, msg)
        return
    elif message.content == '!rst_count':
        reset_count()
        message.reply('Count reset to 0')
        return


def reset_count():
    cur = conn.cursor()
    reset_query = 'UPDATE oofcounttable SET oof_count = 0'
    cur.execute(reset_query)
    print('Set count to 0')

    cur.close()


def has_oof(msg):
    tokens = re.split(r'[ `\-=~!@#$%^&*()_+\[\]{};\'\\:"|,./<>?]', msg.lower())
    for token in tokens:
        if re.search(r'oo[f]+', token):
            return True
    return False


def update_count():
    cur = conn.cursor()
    update_query = 'UPDATE oofcounttable SET oof_count = oof_count + 1'
    cur.execute(update_query)
    query = 'SELECT oof_count FROM oofcounttable;'
    cur.execute(query)
    count = cur.fetchone()[0]
    print('New count is {}'.format(count))

    cur.close()
    return count


client.run(TOKEN)
