import discord
from db.functions import *

with open('token', 'r') as f:
    TOKEN = f.read()
client = discord.Client()
data = {}

@client.event
async def on_ready():
    for server in client.guilds:
        try:
            get_server(server.id)
        except NullError:
            add_server(server.id)

@client.event
async def on_guild_join(guild):
    add_server(guild.id)

@client.event
async def on_message(message):
    if message.content.startswith('!connect'):
        if message.author.guild_permissions.manage_roles:
            argv = message.content.split(';')
            if len(argv) > 1:
                channels = dict()
                for channel in message.guild.channels:
                    channels[channel.name] = channel.id
                roles = dict()
                for role in message.guild.roles:
                    roles[role.name] = role.id
                try:
                    add_channel(message.guild.id, channels[argv[1]], roles[argv[2]])
                    msg = 'Channel linked successfully!'
                    await message.channel.send(msg)
                except IndexError:
                    msg = 'Sorry! We could not find a channel and/or a role with that name. Please check your spelling and try again!'
                    await message.channel.send(msg)
            else:
                msg = 'Improper Usage! The proper use of this command is: !connect;<Voice Channel>;<Role>.'
                await message.channel.send(msg)
    if message.content.startswith('!disconnect'):
        if message.author.guild_permissions.manage_roles:
            argv = message.content.split(';')
            if len(argv) > 0:
                channels = dict()
                for channel in message.guild.channels:
                    channels[channel.name] = channel.id
                try:
                    drop_channel(message.guild.id, channels[argv[1]])   
                    msg = 'Channel unlinked successfully!'
                    await message.channel.send(msg)
                except IndexError:
                    msg = 'Sorry! We could not find a channel with that name. Please check your spelling and try again!'
                    await message.channel.send(msg)
            else:
                msg = 'Improper Usage! The proper use of this command is !disconnect;<Voice Channel>'
                await message.channel.send(msg)
    elif message.content.startswith('!help'):
        with open('app/messages/help', 'r') as f:
            msg = f.read()
        await message.channel.send(msg)
        
@client.event
async def on_voice_state_update(member, before, after):
    before = before.channel
    after = after.channel
    try:
        r = before.guild.get_role(role(before.id))
        roles = member.roles
        roles.remove(r)
        await member.edit(roles=roles)
    except (ValueError, AttributeError, NullError):
        pass
    try:
        r = after.guild.get_role(role(after.id))
        roles = member.roles
        roles.insert(1, r)
        await member.edit(roles=roles)
    except (AttributeError, NullError):
        pass
        
client.run(TOKEN)