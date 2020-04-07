import discord

with open('token', 'r') as f:
    TOKEN = f.read()
client = discord.Client()
data = {}

@client.event
async def on_ready():
    global data
    for server in client.guilds:
        data[server.id] = {}

@client.event
async def on_guild_join(guild):
    global data
    data[guild.id] = {}

@client.event
async def on_message(message):
    if message.content.startswith('!connect'):
        if message.author.guild_permissions.manage_roles:
            channels = message.guild.channels
            argv = message.content.split()
            cnames = [channel.name for channel in channels]
            roles = message.guild.roles
            rnames = [role.name for role in roles]
            if argv[1] in cnames and argv[2] in rnames:
                server = data[message.guild.id]
                try:
                    vc = [channel for channel in channels if channel.name == argv[1]][0]
                    role = [role for role in roles if role.name == argv[2]][0]
                    server[vc] = role
                    msg = 'Channel linked successfully!'
                    await message.channel.send(msg)
                except IndexError:
                    msg = 'Sorry! Either the Channel or the Role was not found on this server. Check your spelling and try again.'
                    await message.channel.send(msg)             
            else:
                msg = 'Improper Usage! The proper use of this command is: !connect <Voice Channel> <Role>'
                await message.channel.send(msg)
    elif message.content.startswith('!help'):
        with open('app/messages/help', 'r') as f:
            msg = f.read()
        await message.channel.send(msg)
        
@client.event
async def on_voice_state_update(member, before, after):
    before = before.channel
    after = after.channel
    if before and before.guild.id in data:
        server = data[before.guild.id]
        if before in server:
            roles = member.roles
            roles.remove(server[before])
            await member.edit(roles=roles)
    if after and after.guild.id in data:
        server = data[after.guild.id]
        if after in server:
            roles = member.roles
            roles.insert(1, server[after])
            await member.edit(roles=roles)
        
client.run(TOKEN)