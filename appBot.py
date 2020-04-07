import discord 
from discord.utils import get
from discord.ext import commands
#from bot.config.roles import builder
#idk why this is creating errors???

client = discord.Client()

@client.event
async def on_ready():
    print('[JBC] RDY')

@client.event
async def on_message(message):
    guild = message.guild
    prefix = 'ap!' #you can make this into a text file if you reeaaally want to
    perms = discord.PermissionOverwrite

    jr_path = 'role_data//jr_builder_id.txt'
    jr_id = open(jr_path, "+r")
    questions = open('temp\\questions.txt', "r")
    role_list = open('temp\\role_list.txt', "r")
    #defining some stuff...
    approver = get(guild.roles, name='Approver')
    #roles can be defined here until i can move them to roles.py
    application_channel = get(guild.channels, name='applications')

    if message.content == prefix + 'junior builder':
        if str(message.author.id) in jr_id.read():
            await message.channel.send(':x: Sorry! Looks like youve already applied for that role! You can use `ap!cancel` to start over!')
        else:

            await guild.create_role(name=message.author.name + ' ap-jr_build')
            role = get(guild.roles, name=message.author.name + ' ap-jr_build')
            await message.author.add_roles(role)

            overwrites = {
                guild.roles[0]: perms(read_messages=False), #covers every role in the server
                guild.me: perms(read_messages=True), #The bot's role/the bot itself
                role: perms(read_messages=True), #the new role that was created when the user applied
                approver: perms(read_messages=True) #approver role
                }
            await guild.create_text_channel(message.author.name + '-jr_build-ap', overwrites=overwrites)
            jr_id.write(str(message.author.id))
            jr_id.write('\n')
            await message.channel.send(':white_check_mark:Application Created! Check Your Dms to continue!')
            await message.author.send(questions.read())
            await application_channel.send('{} has Created an application for Junior Builder!'.format(message.author.mention))


    if message.content == prefix + 'cancel':
        if str(message.author.id) in jr_id.read():
            with open(jr_path, "r") as f:
                lines = f.readlines()
            with open(jr_path, "w") as f:
                for line in lines:
                    if line.strip("\n") != message.author.id:
                        f.write(line)
            role = get(guild.roles, name=message.author.name + ' ap-jr_build')
            await message.author.remove_roles(role)
            await message.channel.send(':white_check_mark:Application Canceled!')
        else:
            await message.channel.send(":x: Sorry! Looks like you havent made an application yet! Use `ap!junior builder` to make an application!")
    
    if message.content == prefix + 'list':
        await message.channel.send(role_list.read())

    if message.content == prefix + 'finish':
        if str(message.author.id) in jr_id.read():
            application_channel = get(guild.channels, name='applications')
            role = get(guild.roles, name=message.author.name + ' ap-jr_build')
            await message.author.remove_roles(role)
            await application_channel.send('{} has completed their application for Junior Builder!'.format(message.author.mention))
        else:
            await message.channel.send(':x: Sorry! you havent made an application yet! Use `ap!junior builder` to apply!')

    

token = open('config\\token.txt', "+r")
client.run(token.read())