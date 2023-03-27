from replit_bot import Bot
import os

TOKEN = os.environ["API_TOKEN"]
bot = Bot(TOKEN)

@bot.default
def reg_command(ctx):
    ctx.reply("this happens when no set command is sent")

bot.run()