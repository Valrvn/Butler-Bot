# bot.py

import fun_zone_bot as fzb                                      #Fun Zone implementations for the bot
import moderation_zone_bot as mzb                               #Moderation Zonde implementations for the bot
import embed_routine as ezb                                     #Embed-based-communication

import os

import discord

from dotenv import load_dotenv                                  #environment for the DC Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#the code needs a .env file with the following content
# # .env
# DISCORD_TOKEN=<copy and paste your token from the Discord Developer Portal here>
#check sources.txt for more information on this step

#client, with fix for intentions -> this is the bot
client = discord.Client(intents=discord.Intents.all())

#Method for debugging
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#Method for commands
@client.event
async def on_message(message):

    #Routines for messages from the bot itself
    if message.author == client.user:
        return

    #Messages from other users (can also be bots)

    await send_butler_menu(message)             #Butler menu
    await fzb.apig_message(message)             #Apig routine
    await fzb.roa_message(message)              #Method for Rules of Acquisition
    await fzb.google_an_image(message)          #Google Image Search
    await fzb.send_photo_on_command(message)    #Special commands for images

    await mzb.copy_all_to_channel(message)          #Copy all messages of channel to another channel
    await mzb.copy_all_from_channel(message)        #Copy all messages of another channel to channel
    await mzb.move_all_to_channel(message)          #Move all messages of channel to another channel
    await mzb.move_all_from_channel(message)        #Move all messages of channel to another channel
    await mzb.copy_new_message_to_channel(message)  #copy all new messages of channel to another channel
    await mzb.copy_one_msg_to_channel(message)      #copy one specific message of channe to another channel

    await ezb.start(message)                    #start a personal session with Butler, based on embeds
    
    return

@client.event
async def on_raw_reaction_add(payload):
    #Routines for reactions from the bot itself
    if payload.user_id == client.user.id:
        return

    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)

    #only edit messages with one embed that have been written by the same bot
    if message.author == client.user and len(message.embeds) == 1:
        await ezb.edit(message,payload)

    return

#Butler Menu (Help)
async def send_butler_menu(message):
    if '?butler' == message.content.lower() or '?help' == message.content.lower():
        await message.channel.send(
            "\t- ?help or ?butler - post the bot menu\n"
            "Fun zone:\n"
            "\t- ?apig - post the pig prayer. If PigPriestess is the user that requested Apig, also tag here. If not post message, saying that Val needs to wake up...\n"
            "\t- ?upig, ?unipig, ?pigcorn =  send random unicorn pig image\n"
            "\t- ?unicorn, ?🦄 = send random unicorn image\n"
            "\t- ?🐽, ?pig, ?🐖, ?🐷, ?🐗, ?hog =  send random pig image\n"
            "\t- ?aubergine, ?eggplant, ?🍆 =  send random aubergine image\n"
            "\t- ?sausage = send random sausage image\n"
            "\t- ?bacon = send random bacon image\n"
            "\t- ?cake, ?🍰, ?🎂, ?🧁, ?🥧 = send random cake image\n"
            "\t- ?poulpe, ?8, ?octo, ?korosensei, ?octopus, ?kraken, ?🐙 = send random octopus image\n"
            "\t- ?rulesOfAcquisition, ?roa (Capitalization doesn't matter) = send random rule of Acquisition\n"
            "\t- ?gi <parameter> = Google Image search. Put search parameters after the ?gi command. Please keep it clean, or Butler will get upset and go offline...\n"
            "\n"
            "For any complaints or bot requests, message @Valravn aka the one learning Python with this silly little bot.\n"
            #"The bot is restricted to #funny-pics and #🦄🐽-upig-of-the-day only when in the UPIG server.\n"
            "\t- !start = start a personal interactive session with Butler"
        )
        return
    return

client.run(TOKEN)