import discord
from discord.ext import commands
from discord.utils import get

client = discord.Client()

userpath = 'bot\\data\\userid.txt'

@client.event
async def on_ready():
    print('ready')

@client.event
async def on_message(message):

    prefix = 'ap!'
    user = open(userpath, "+r")

    if message.content == prefix + 'create':

        if str(message.author.id) in user.read():
            await message.channel.send("Youve Already Applied! If you want you can use `ap!remove` to start over!")
        else:
            guild = message.author.guild
            await guild.create_role(name=message.author.name)
            role = discord.utils.get(guild.roles, name=message.author.name)
            approver = discord.utils.get(guild.roles, name='MODERATOR')
            mod = discord.utils.get(guild.roles, name='SOVERGN')
            await message.author.add_roles(role)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                role: discord.PermissionOverwrite(read_messages=True),
                approver: discord.PermissionOverwrite(read_messages=True),
                mod: discord.PermissionOverwrite(read_messages=True)
            }
            user.write(str(message.author.id))
            user.write('\n')
            crt_chan = await guild.create_text_channel(message.author.name, overwrites=overwrites)
            questionpath = 'bot\\temp\\questions.txt'
            question = open(questionpath, "+r")
            await message.author.send(question.read())
        
    if message.content == prefix + "finish":
        app_role = get(message.author.guild.roles, name=message.author.name)
        await message.author.remove_roles(app_role)
        with open(userpath, "r") as f:
            lines = f.readlines()
        with open(userpath, "w") as f:
            for line in lines:
                if line.strip('\n')  != message.author.id:
                    f.write(line)
        await message.author.send('Thank your for your application!')    

client.run('LOL')