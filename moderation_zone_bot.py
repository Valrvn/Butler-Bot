#moderation_zone_bot.py

#Fine-tuned method to copy all new messages from a certain message channel to another channel
#In the UPIG server:
    #copy all new messages from #rules (team zone) to #rules (member zone)
async def copy_new_message_to_channel(message):
    id_from = 698422697100574770 #rules (team zone)
    id_to = 825704830957125642   #rules (new members zone)
    if message.channel.id == id_from:
        to_channel = message.guild.get_channel(id_to)
        if to_channel is not None:
            await copy_one_message_to(message,to_channel,message.channel)
    return

#Copy one specific message from the channel where you post commmand to another channel. 
#Can only be used by server admin (person with admin in their role names) or server owner.
async def copy_one_msg_to_channel(message):
    if message.content[0:10] != '?cpyMsgTo ':
        return
    user_roles_names = [] 
    for r in message.author.roles:
        user_roles_names.append(r.name.lower())
    if (message.author == message.guild.owner or 'admin' in user_roles_names or 'server admin' in user_roles_names) and len(message.channel_mentions) == 1:
        m = await message.channel.fetch_message(message.content[10:28])
        to_channel=message.channel_mentions[0]
        if len(m.embeds) == 0:
            await to_channel.send(m.content)
        else:
            for e in m.embeds: 
                await to_channel.send(embed = e)
    return

#Copy all messages from one channel to another. Can be used by users that have and "admin" role and/or by the server owner
# '?cpyTo #channel'
async def copy_all_to_channel(message):
    if message.content[0:7] != '?cpyTo ':
        return
    user_roles_names = [] 
    for r in message.author.roles:
        user_roles_names.append(r.name.lower())
    if (message.author == message.guild.owner or 'admin' in user_roles_names) and len(message.channel_mentions) == 1:
        if message.channel.id != message.channel_mentions[0].id:
            await copy_messages_from_to(message.channel,message.channel_mentions[0])
            return
        return
    return

#Copy all messages from one channel to another. Can be used by users that have and "admin" role and/or by the server owner
# '?cpyFrom #channel'
async def copy_all_from_channel(message):
    if message.content[0:9] != '?cpyFrom ':
        return
    user_roles_names = [] 
    for r in message.author.roles:
        user_roles_names.append(r.name.lower())
    if (message.author == message.guild.owner or 'admin' in user_roles_names) and len(message.channel_mentions) == 1:
        if message.channel.id != message.channel_mentions[0].id:
            await copy_messages_from_to(message.channel_mentions[0],message.channel)
            return
        return
    return

#Move all messages from one channel to another. Can be used by users that have and "admin" role and/or by the server owner
# '?moveTo #channel'
async def move_all_to_channel(message):
    if message.content[0:8] != '?moveTo ':
        return
    user_roles_names = [] 
    for r in message.author.roles:
        user_roles_names.append(r.name.lower())
    if (message.author == message.guild.owner or 'admin' in user_roles_names) and len(message.channel_mentions) == 1:
        if message.channel.id != message.channel_mentions[0].id:
            await move_messages_from_to(message.channel,message.channel_mentions[0])
            return
        return
    return

#Move all messages from one channel to another. Can be used by users that have and "admin" role and/or by the server owner
# '?moveFrom #channel'
async def move_all_from_channel(message):
    if message.content[0:10] != '?moveFrom ':
        return
    user_roles_names = []
    for r in message.author.roles:
        user_roles_names.append(r.name.lower())
    if (message.author == message.guild.owner or 'admin' in user_roles_names) and len(message.channel_mentions) == 1:
        if message.channel.id != message.channel_mentions[0].id:
            await move_messages_from_to(message.channel_mentions[0],message.channel)
            return
        return
    return

#Helper method that copies messages from one channel to another
async def copy_messages_from_to(from_channel, to_channel):
    #Possible ToDo: history(limit = ????)
    #Copy all messages to recipient channel
    async for m in from_channel.history(limit=None,oldest_first=True):
       await copy_one_message_to(m,to_channel,from_channel)
    return

#Helper method that moves messages from one channel to another
async def move_messages_from_to(from_channel, to_channel):
    #Possible ToDo: history(limit = ????)
    #Copy all messages to recipient channel
    async for m in from_channel.history(limit=None,oldest_first=True):
        await copy_one_message_to(m,to_channel,from_channel)
    #Clear from from channel
    async for m in from_channel.history():
        await m.delete()
    return

#Helper method to copy one message to a channel
#Extra handling for embeds
async def copy_one_message_to(message,to_channel,from_channel):
    m_author = message.author
    if m_author in to_channel.members:
            m_author = message.author.mention
    if len(message.embeds) == 0:
        await to_channel.send(m_author + ' wrote in ' + from_channel.mention + ': ' + message.content)
    else:
        for e in message.embeds: 
            await to_channel.send(embed = e)
    return