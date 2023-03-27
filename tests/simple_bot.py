from replit_bot import Bot, Param
import os

TOKEN = os.environ["API_TOKEN"]
bot = Bot(TOKEN)

@bot.command('say')
def ask(ctx, p:Param(required=True)):
    ctx.reply(p)

bot.run()