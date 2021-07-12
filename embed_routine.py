import discord

#API for this functionality
#To be called for a Message that is the !start command
async def start(message):
    if '!start' == message.content.lower():
        sessionMessage = await message.channel.send(embed = await embed_selector("start"))
        for r in await embed_reaction_selector("start"):
            await sessionMessage.add_reaction(r)
        return
    elif "!start dm" == message.content.lower():
        sessionMessage = await message.channel.send(embed = await embed_selector("dm_start"))
        for r in await embed_reaction_selector("dm_start"):
            await sessionMessage.add_reaction(r)
        return
    return

async def edit(message,payload):
    await edit_embed(message,payload)
    return


#----------END of API-----------------------
#----------EMBED related code---------------
#EMBED GENERATORS

#The local embed types are strings for now.
#idea for a TODO - remake them as enums
#embedTypes = ["start","end","ERROR","dm_start","dm_colour_pick"]

#caller for all embed generators by type
async def embed_selector(type):
    if "start" == type:
        return await start_embed()
    if "end" == type:
        return await end_embed()
    if "dm_start" == type:
        return await start_dm_embed()
    if "dm_colour_pick" == type:
        return await colour_pick_dm_embed()
    return

#a method to give the proper list of reactions for each embed type
async def embed_reaction_selector(type):
    if "start" == type:
        return ["🖌","🤖","❌","🤫"]
    if "end" == type:
        return []
    if "dm_start" == type:
        return ["🎨"]
    if "dm_colour_pick" == type:
        return ["🐽","❤","🧡","💛","💚","💙","💜"]
    return

#a method to map the footer (unique ID) of an embed to it's type
async def embed_footer_to_type_selector(footer):
    if footer == "Start of personal session":
        return "start"
    if footer == "End of personal session":
        return "end"
    if footer == "Start of private session":
        return  "dm_start"
    if footer == "Colour settings of a private session":
        return "dm_colour_pick"
    return "ERROR"

#a method to make the proper change in embed upon a reaction
async def edit_embed(message,payload):
    #get the old embed type
    old_embed_type = await embed_footer_to_type_selector(message.embeds[0].footer.text)

    #do not touch these ones, they aren't ours!
    if old_embed_type == "ERROR":
        return
    
    #embed session was ended, pretent not to see it anymore
    if old_embed_type == "end":
        return
    
    #make a decision for the next embed type, default is to stay with the current one
    new_embed_type = old_embed_type
    #make a decision for the embed color, default is to stay with the old one
    new_embed_color = message.embeds[0].color

    #check the emoji that was used - only unicode reactions can make a change in type
    ems = str(payload.emoji)
    if payload.emoji.is_unicode_emoji:
        if ems == "❌":
            new_embed_type = "end"
            
        elif old_embed_type == "start":
                if ems == "🤫":
                    new_embed_type = "end"
                    dmSessionMessage = await payload.member.send(embed = await embed_selector("dm_start"))
                    for r in await embed_reaction_selector("dm_start"):
                        await dmSessionMessage.add_reaction(r)
        elif old_embed_type == "dm_start":
                if ems == "🎨":
                    new_embed_type = "dm_colour_pick"
        elif old_embed_type == "dm_colour_pick":
            new_embed_type = "dm_start"
            if ems == "🐽":
                new_embed_color = 0xf5b7cd
            elif ems == "❤":
                new_embed_color = 0xeb1010
            elif ems =="🧡":
                new_embed_color = 0xfc850d
            elif ems == "💛":
                new_embed_color = 0xf5ed0f
            elif ems =="💚":
                new_embed_color = 0x0ff51e
            elif ems =="💙":
                new_embed_color = 0x0fcef5
            elif ems == "💜":
                new_embed_color = 0x8605f0 

    #TODO - expand and change here as the embed types collection grows
    #This is the actual logic spot of the embed session

    #edit embed accordingly
    if "dm" not in old_embed_type:
        await message.clear_reactions()
        newEmbed = await embed_selector(new_embed_type)
        newEmbed.color = new_embed_color
        await message.edit(embed = newEmbed)
        for r in await embed_reaction_selector(new_embed_type):
            await message.add_reaction(r)
    else:
        newEmbed = await embed_selector(new_embed_type)
        newEmbed.color = new_embed_color
        newMessage = await message.channel.send(embed = newEmbed)
        for r in await embed_reaction_selector(new_embed_type):
            await newMessage.add_reaction(r)
    return

#----------------EMBED Creators----------------
#start of session
async def start_embed():
    embed= discord.Embed(
        title="Butler personal session", 
        description="Welcome to your personal session with Butler", 
        color=0xf5b7cd,
        )
    embed.add_field(
        name= "Click on the reactions bellow to help me find you what you're looking for", 
        value= "🖌 to change your colour in Discord\n"
               "🤖 to revert to the standard colour for your Discord rank\n"
               "🤫 to move this session into your private messages\n"
               "❌ to close this session\n", 
        inline=False
        )
    embed.set_footer(text=("Start of personal session"))
    return embed

#end of session
async def end_embed():
    embed= discord.Embed(
        title="Butler personal session", 
        description="Thank you for paying me a visit, my lovely friend!", 
        color=0xf5b7cd,
        )
    embed.set_footer(text=("End of personal session"))
    return embed

async def start_dm_embed():
    embed= discord.Embed(
        title="Butler private session", 
        description="Welcome to your private session with Butler", 
        color=0xf5b7cd,
        )
    embed.add_field(
        name= "Click on the reactions bellow to help me find you what you're looking for", 
        value= "🎨 to pick a new colour for this session\n", 
        inline=False
        )
    embed.set_footer(text=("Start of private session"))
    return embed

async def colour_pick_dm_embed():
    embed= discord.Embed(
        title="Butler private session", 
        description="Welcome to your private session with Butler", 
        color=0xf5b7cd,
        )
    embed.add_field(
        name= "Click on the reactions bellow to help me find you what you're looking for", 
        value= "🐽 for piggy pink\n"
               "❤ for red\n"
               "🧡 for organge\n"
               "💛 for yellow\n"
               "💚 for green\n"
               "💙 for blue\n"
               "💜 for purple\n", 
        inline=False
        )
    embed.set_footer(text=("Colour settings of a private session"))
    return embed