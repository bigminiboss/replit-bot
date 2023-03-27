# TUTORIAL: https://replit.com/@Howtomakeabot/How-To-Make-Replit-Bots?v=1

import os
import json
import time
import logging
from random import randint
from requests import get
from replit_bot import Bot, Param, __license__, __version__, app
from threading import Thread
from markdown import markdown
from flask import render_template_string

app.route("/docs")(
    lambda: render_template_string(
        open("replit_bot/templates/index.html").read(),
        html=markdown(open("README.md").read(), extensions=["fenced_code"]),
    )
)

bot = Bot(os.environ["TOKEN"], prefix="/", bio="This is a bot")

times = []


def fetch():
    url = json.loads(get("https://meme-api.herokuapp.com/gimme").text)
    counter = 0
    while url["nsfw"]:
        url = json.loads(get("https://meme-api.herokuapp.com/gimme").text)
        counter += 1
        if counter > 10:
            return

    return url["url"]


def _resolve_timers():
    while True:
        for i in times:
            if i[0] >= time.time():
                i[1].reply("Your timer went off!")
        time.sleep(1)


@bot.command("enjoy-pancakes", alias=["enjoy"])
def enjoy(ctx):
    ctx.reply(
        f"hello! do you like pancakes?\n\n{ctx.button.yes}\t{ctx.button.no}",
        mention=True,
    )
    ctx.reply(
        "You traitor" if ctx.button.get_choice() == "no" else "yay! we're friends"
    )


@bot.command("personality-quiz", alias=["quiz"])
def person(ctx):
    count = {"a": 0, "b": 0}
    questions = [
        {"name": "do you like pancakes", "a": "no", "b": "yes"},
        {"name": "do you like waffles", "a": "yes", "b": "no"},
        {"name": "do you like eggs", "a": "yes", "b": "no"},
        {"name": "are pancakes better than waffles?", "a": "no", "b": "yes"},
    ]

    for i in questions:
        ctx.reply(
            f"{i['name']}\n\n{ctx.button.a} ({i['a']})\n\n{ctx.button.b} ({i['b']})"
        )
        count[ctx.button.get_choice()] += 1

    most = max(count, key=count.get)
    ctx.reply("You traitor" if most == "a" else "yay! we're friends")


@bot.command("repl")
def repl(ctx):
    repl = ctx.repl

    ctx.reply(
        f"""**{repl.title}**•*{repl.timeUpdated}*
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
def _random(
    ctx,
    low: Param(required=True, type_cast=int),
    high: Param(required=True, type_cast=int),
):
    ctx.reply(f"random number is {randint(low, high)}")


@bot.command("timer")
def _timer(ctx, num_time: Param(required=True, type_cast=int)):
    global times
    ctx.reply("starting timer")
    times.append((time.time() + num_time, ctx))


@bot.command("code-info")
def _code_info(ctx):
    ctx.reply(
        f"""> license: {__license__}
> version: {__version__}"""
    )


@bot.command("who-is")
def on_who_is(ctx, person: Param(required=True)):
    person = bot.users.fetch(person)
    ctx.reply(
        f"@{person.username} is {person.firstName} {person.lastName}. They speak {person.locale} and they are verified = {person.isVerified}. Their bio is: {person.bio}. They have {person.followerCount} followers and are following {person.followCount} people",
        mention=True,
    )


# @bot.listener("who-is")
# def on_who_is_log(ctx, person: Param(required=True)):
#     print("lol", person)


# @bot.follower
# def when_followed(ctx, person):
#     person.setFollowing(True)

Thread(target=_resolve_timers).start()
bot.run()
