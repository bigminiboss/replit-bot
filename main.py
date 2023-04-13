# TUTORIAL: https://replit.com/@Howtomakeabot/How-To-Make-Replit-Bots?v=1

import os
import json
import time
import logging
import asyncio
from random import randint
from requests import get
from replit_bot.AsyncBot import Bot
from replit_bot import Param, __license__, __version__
from threading import Thread
from markdown import markdown
from flask import Flask

app = Flask(__name__)
bot = Bot(os.environ["TOKEN"], prefix="/", bio="This is a bot")


@bot.command("milo-cat")
async def milo_cat(ctx):
    count = {"a": 0, "b": 0}
    questions = [
        {"name": "do you like pancakes", "a": "no", "b": "yes"},
        {"name": "do you like waffles", "a": "yes", "b": "no"},
        {"name": "do you like eggs", "a": "yes", "b": "no"},
        {"name": "are pancakes better than waffles?", "a": "no", "b": "yes"},
    ]
    i = questions[0]
    x = await ctx.reply(
        f"{i['name']}\n\n{ctx.button.a} ({i['a']})\n\n{ctx.button.b} ({i['b']})"
    )
    count[await ctx.button.get_choice()] += 1
    for i in questions[1:]:
        await x.edit(
            f"{i['name']}\n\n{ctx.button.a} ({i['a']})\n\n{ctx.button.b} ({i['b']})"
        )
        count[await ctx.button.get_choice()] += 1

    most = max(count, key=count.get)
    await x.edit("You traitor" if most == "a" else "yay! we're friends")


@bot.command("enjoy-pancakes", alias=["enjoy"])
async def enjoy(ctx):
    await ctx.reply(
        f"{ctx.author.mention} hello! do you like pancakes?\n\n{ctx.button.yes}\t{ctx.button.no}",
    )
    await ctx.reply(
        "You traitor" if await ctx.button.get_choice() == "no" else "yay! we're friends"
    )


@bot.command("personality-quiz", alias=["quiz"])
async def person(ctx):
    count = {"a": 0, "b": 0}
    questions = [
        {"name": "do you like pancakes", "a": "no", "b": "yes"},
        {"name": "do you like waffles", "a": "yes", "b": "no"},
        {"name": "do you like eggs", "a": "yes", "b": "no"},
        {"name": "are pancakes better than waffles?", "a": "no", "b": "yes"},
    ]

    for i in questions:
        await ctx.reply(
            f"{i['name']}\n\n{ctx.button.a} ({i['a']})\n\n{ctx.button.b} ({i['b']})"
        )
        count[await ctx.button.get_choice()] += 1

    most = max(count, key=count.get)
    await ctx.reply("You traitor" if most == "a" else "yay! we're friends")


@bot.command("repl")
async def repl(ctx):
    repl = ctx.repl

    await ctx.reply(
        f"""**{repl.title}**•**{repl.timeUpdated}**
```
➤ Id: {repl.id}
➤ Created: {repl.timeCreated}
➤ Published: {repl.timeUpdated}
➤ language: {repl.language}
➤ template repl: {repl.rootOriginReplUrl}
➤ Size (Bytes): {repl.size}
➤ Forks: {repl.publicForkCount}
```"""
    )


# @bot.command("meme", desc="yk, the famous meme command")
# def meme(ctx):
#     ctx.reply(ctx.Image(fetch()))


# @bot.command("lotsa-memes", thread=True)
# def lotsa(ctx):
#     stop = False
#     while not stop:
#         ctx.reply(f"{ctx.Image(fetch())}\n\n{ctx.button.next}\n\n{ctx.button.stop}")
#         stop = ctx.button.get_choice() == "stop"


@bot.command("random-number", alias=["rand", "randint", "rand-num"])
async def _random(
    ctx,
    low: Param(required=True, type_cast=int),
    high: Param(required=True, type_cast=int),
):
    await ctx.reply(f"random number is {randint(low, high)}")


@bot.command("timer")
async def _timer(ctx, num_time: Param(required=True, type_cast=int)):
    global times
    await ctx.reply("starting timer")
    await asyncio.sleep(num_time)
    await ctx.reply("timer went off!")


@bot.command("code-info")
async def _code_info(ctx):
    await ctx.reply(
        f"""> license: {__license__}
> version: {__version__}"""
    )


@bot.command("who-is")
async def on_who_is(ctx, person: Param(required=True)):
    person = await bot.users.fetch(person)
    await ctx.reply(
        f"{ctx.author.mention} @{person.username} is {person.firstName} {person.lastName}. They speak {person.locale} and they are verified = {person.isVerified}. Their bio is: {person.bio}. They have {person.followerCount} followers and are following {person.followCount} people"
    )


# @bot.listener("who-is")
# def on_who_is_log(ctx, person: Param(required=True)):
#     print("lol", person)


# @bot.follower
# def when_followed(ctx, person):
#     person.setFollowing(True)

bot.run(auto_create_docs=True, flask_app=app)
