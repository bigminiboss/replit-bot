# @howtomakeabot

from replit_bot import Bot, Param #Importing The Function, adding 'Param' or 'Parameters' as people call them
import os #Adding the 'Secrets' Module
import openai #Importing ChatGPT
my_secret = os.environ['OPENAIKEY'] #Getting OPENAI Key
openai.api_key = my_secret #Inputting it it
TOKEN = os.environ["API_TOKEN"] #Gaining the Module
bot = Bot(TOKEN) #Implementing it in

@bot.command('Hello World') #This shows that, if you type '/Hello World'
def helloworld(ctx):#This has to be under the command. This is a function, name it anything
  ctx.reply("Hello, you said 'Hello World'.") #What it replies when typing '/Hello World'
def OPENAI(prompt): #If you want to learn this, then comment your name =P
  response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
  message = response.choices[0].text.strip()
  return message
@bot.command('ask') #You know what this is :P
def ask(ctx, question = Param(required = True)): #Adds Params to sense what the person says
  ctx.reply(OPENAI(question))


bot.run() #Runs The Bot