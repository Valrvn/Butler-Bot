#fun_zone_bot.py
import os
import random

import xlrd                                                    #Excel File read library for Rules of Acquisition
from google_images_search import GoogleImagesSearch            #Google Images API

import discord

#Apig routine
async def apig_message(message):
    if '?apig' == message.content.lower():
        #send Pig Prayer
        await message.channel.send('Our HogFather,\nwho farts in Fedspace,\nhallowed be thy node.\nThy Klingon come.\nThy Rom be done on Earth\nas it is on Vulcan.\nGive us this kill,\nour daily goal,\nAnd forgive us our baseraids,\n\nAs we forgive none\nwho trash talk about us,\nAnd lead us not into empties,\nBut deliver us fat miners.\nFor thine is the pigsty,\nAnd the powergain,\nand the glorykill.\nForever and oinkoink.\n\nApig 🐷')
        
        #notify @here, if the Pig Priestess is requesting the prayer
        if "Valravn#5717" == str(message.author):
            await message.channel.send("Time for GC Apig @here")
        else:
            pigPriestess = 'the Pig Priestess'
            #id of OG Pig Priestess
            priestess_inguild = message.guild.get_member(436182601904947211)
            if priestess_inguild is not None:
                pigPriestess = str(priestess_inguild.mention)
            await message.channel.send("Someone raise "+ pigPriestess +" from slumber for a GC Pig Prayer!")
        return
    return

#Handler for the special commands for images
async def send_photo_on_command(message):
    #send random pigcorn image
    if '?unipig' == message.content.lower() or '?pigcorn' == message.content.lower() or '?upig' == message.content.lower():
        await message.channel.send(file=discord.File("Images\\Unipigs\\" + random.choice(os.listdir("Images\\Unipigs"))))
        return

    #send random unicorn image
    if '?unicorn' == message.content.lower() or '?🦄' == message.content:   
        await message.channel.send(file=discord.File("Images\\Unicorns\\" + random.choice(os.listdir("Images\\Unicorns"))))
        return
    
    #send random pig image
    if '?pig' == message.content.lower() or '?hog' == message.content.lower() or '?🐗' == message.content or '?🐷' == message.content or '?🐖' == message.content or'?🐽' == message.content:
        await message.channel.send(file=discord.File("Images\\Pigs\\" + random.choice(os.listdir("Images\\Pigs"))))
        return
    
    #send random aubergine image
    if '?aubergine' == message.content.lower() or '?eggplant' == message.content.lower() or '?🍆' == message.content:
        await message.channel.send(file=discord.File("Images\\Eggplants\\" + random.choice(os.listdir("Images\\Eggplants"))))
        return

    #send random sausage image
    if '?sausage' == message.content.lower():
        await message.channel.send(file=discord.File("Images\\Sausages\\" + random.choice(os.listdir("Images\\Sausages"))))
        return

    #send random bacon image
    if '?bacon' == message.content.lower():
        await message.channel.send(file=discord.File("Images\\Bacon\\" + random.choice(os.listdir("Images\\Bacon"))))
        return

    #send random cake image
    if '?cake' == message.content.lower() or '?🍰' == message.content.lower() or '?🎂' == message.content.lower() or '?🧁' == message.content.lower() or '?🥧' == message.content.lower():
        await message.channel.send(file=discord.File("Images\\Cakes\\" + random.choice(os.listdir("Images\\Cakes"))))
        return

    #send random octopus image
    if '?poulpe' == message.content.lower() or '?8' == message.content.lower() or '?🐙' == message.content.lower() or '?kraken' == message.content.lower() or '?octopus' == message.content.lower() or '?korosensei' == message.content.lower() or '?octo' == message.content.lower():
        await message.channel.send(file=discord.File("Images\\Poulpes\\" + random.choice(os.listdir("Images\\Poulpes"))))
        return

    #send random pineapple image
    if '?pineapple' == message.content.lower() or '?🍍' == message.content.lower():
        await message.channel.send(file=discord.File("Images\\Pineapples\\" + random.choice(os.listdir("Images\\Pineapples"))))
        return
    return

#Rules of Acquisition Setup
#path to RoA file:
roa_file_path = "Excels\\RoA.xls"
#RoA file settings:
roa_work_book = xlrd.open_workbook(roa_file_path) 
roa_sheet = roa_work_book.sheet_by_index(0)

#Rules of Acquisition message:
async def roa_message(message):
    if '?roa' == message.content.lower() or '?rulesofacquisition' == message.content.lower():
        #get a random index between 0 and total number of rules:
        index = random.randrange(0, 154)

        #send cell value with rule
        await message.channel.send(str(roa_sheet.cell_value(index,0)))
        return
    return

#Google Images Parameters
gis = GoogleImagesSearch('AIzaSyAC1N7KAdA7sHYUWmFXZbrLulY-LMBkaRc', '8dbb2bb91041d61c5')
    
#Google Image Search
async def google_an_image(message):
    if '?gi ' == message.content.lower()[:4]:
        # define search params:
        _search_params = {
        'q': message.content[3:],
        'num': 5,
        'safe': 'high',
        'fileType': 'JPG',
        'imgSize': 'MEDIUM',
        }

        #search for images:
        gis.search(search_params=_search_params, path_to_dir='Images\\GoogleImagesSearch')

        #send the downloaded image
        await message.channel.send(file=discord.File("Images\\GoogleImagesSearch\\" + random.choice(os.listdir("Images\\GoogleImagesSearch"))))

        #clear the GoogleImagesSearch Directory
        for fn in os.listdir("Images\\GoogleImagesSearch"):
            os.remove("Images\\GoogleImagesSearch\\" + fn)

        return
    return