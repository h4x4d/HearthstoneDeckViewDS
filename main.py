import random

from db.config import TOKEN
from image_creator import create_picture

import datetime
import os

import discord
from discord.ext import commands
import logging

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


client = commands.Bot(command_prefix="/",
                      activity=discord.Game(name="Analyzing decks"),
                      intents=discord.Intents.all())


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(discord.__version__)
    print('------')

    print('Servers connected to:')
    sum_servers, sum_members = 0, 0
    for guild in client.guilds:
        sum_servers += 1
        sum_members += guild.member_count
        print(guild.name, "-----", guild.member_count, "members")

    print(f"ALL: {sum_servers} servers, {sum_members} members")
    print("\n\n---------\n\n")


@client.event
async def on_message(message: discord.message.Message):
    try:
        text = message.content.split()

        start_time = datetime.datetime.now()

        for word in text:
            if word[:2] == 'AA':
                ctx: discord.ext.commands.context.Context = await client.get_context(message)

                image = await create_picture(word)

                x, y = image.size
                image = image.resize((int(x / 1.2), int(y / 1.2)))

                name = random.randint(1000000, 10000000)

                image.save(f"{name}.png", format="PNG")

                await ctx.send(file=discord.File(f"{name}.png"))

                os.remove(f"{name}.png")

                print(datetime.datetime.now() - start_time)
    except Exception as e:
        print(f"ERR: {e}")


client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
