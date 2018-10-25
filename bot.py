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

    elif message.content.lower().startswith('!oof_count'):
        await client.send_message(message.channel, get_count())
        return

    elif message.content.lower().startswith('!oof_king') or message.content.lower().startswith('!oof_queen'):
        user_ids = get_max_oof_users()
        msg = '<:Oof:504616782695366657> It\'s '
        if len(user_ids) == 1:
            user_name = await client.get_user_info(user_ids[0]).display_name
            msg += '{}'.format(user_name)
        else:
            for user_id in user_ids[:-2]:
                user_name = await client.get_user_info(user_id).display_name
                msg += '{}, '.format(user_name)
            second_last = await client.get_user_info(user_ids[-2]).display_name
            last = await client.get_user_info(user_ids[-1]).display_name
            msg += '{} and {}'.format(second_last, last)
        await client.send_message(message.channel, msg)
        return

    elif has_oof(message.content):
        update_count(message.author.id)
        msg = '<:Oof:504616782695366657> count : {}'.format(get_count())
        await client.send_message(message.channel, msg)
        return


def get_max_oof_users():
    cur = conn.cursor()
    max_user_query = 'SELECT user_id from oofcounttable WHERE oof_count = ' \
                     '(SELECT MAX(oof_count) from oofcounttable WHERE user_id <> \'resv\' )'
    cur.execute(max_user_query)
    user_id_tuple = cur.fetchall()
    user_ids = [user_id for user_id_row in user_id_tuple for user_id in user_id_row]
    return user_ids


def get_count():
    cur = conn.cursor()
    get_query = 'SELECT sum(oof_count) FROM oofcounttable;'
    cur.execute(get_query)
    count = cur.fetchone()[0]
    cur.close()
    return count


def has_oof(msg):
    tokens = re.split(r'[ `\-=~!@#$%^&*()_+\[\]{};\'\\:"|,./<>?]', msg.lower())
    for token in tokens:
        if re.search(r'[o]{2,}[f]+', token):
            return True
    return False


def update_count(user_id):
    cur = conn.cursor()
    update_query = 'UPDATE oofcounttable SET oof_count = oof_count + 1 WHERE user_id = %s'
    cur.execute(update_query, (user_id,))
    if cur.rowcount == 0:
        insert_query = 'INSERT INTO oofcounttable (oof_count, user_id) VALUES (%s, %s)'
        cur.execute(insert_query, (1, user_id,))
    cur.close()


client.run(TOKEN)
