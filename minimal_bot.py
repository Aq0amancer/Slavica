import discord
from discord.ext import commands
import pandas as pd
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import random

TOKEN = 'Nzc2NDE0OTIxMDQxNzcyNjE0.X60ivg.V0aSzqUyQPjjHt6Op2DprM-cqVg'

bot = commands.Bot(command_prefix='!')

ispovesti = pd.read_csv('Ispovesti.csv')


@ bot.event
async def on_ready():

    print('We have logged in as a fucking {0.user}'.format(bot))


@ bot.command(pass_context=True)
async def join(ctx):

    channel = ctx.author.voice.channel

    await channel.connect()


@bot.command()
async def test(ctx, arg):

    await ctx.send(arg)


@bot.command()
async def cibe(ctx):

    await ctx.voice_client.disconnect()


@bot.command()
async def clear(ctx, amount=5):

    await ctx.channel.purge(limit=amount)


@bot.command()
async def vine(ctx):

    vine_file_name = random.choice(os.listdir("Memes"))


@bot.command()
async def vic(ctx):

    driver = webdriver.Chrome('chromedriver')

    driver.get("https://vicevi.net/site/best")

    vic_text = driver.find_element_by_xpath("//*[@class='col-lg-12']").text

    web_url = 'https://vicevi.net/site/best?page=15'


@bot.command()
async def ispovest(ctx):

    video = ispovesti.sample()

    #video_name = video['Title'].iloc[0]

    #video_link = video['URL'].iloc[0]
    ispovest = random.choice(os.listdir("Ispovesti"))
    video_name = ispovest[:-4]
    video_link = 'Ispovesti/' + ispovest

    # check where the message was typed

    if ctx.voice_client is None:

        channel = ctx.author.voice.channel

        await channel.connect()

    YDL_OPTIONS = {'format': 'bestaudio/best',

                   'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',

                   'restrictfilenames': True,

                   'noplaylist': True,

                   'nocheckcertificate': True,

                   'ignoreerrors': False,

                   'logtostderr': False,

                   'quiet': True,

                   'no_warnings': True,

                   'default_search': 'auto',

                   # bind to ipv4 since ipv6 addresses cause issues sometimes
                   'source_address': '0.0.0.0'

                   }

    FFMPEG_OPTIONS = {'options': '-vn'}
    # voice = get(bot.voice_client, guild=ctx.guild)

    server = ctx.message.guild

    voice_channel = server.voice_client

    if not voice_channel.is_playing():

        voice_channel.play(FFmpegPCMAudio(
            source=video_link, **FFMPEG_OPTIONS))

        voice_channel.is_playing()

        await ctx.send(video_name)

    else:

        await ctx.send("Cekaj da zavrsim pricu")

        return


'''@ bot.event

async def on_message(message):

    if message.author == bot.user:

        return



    if message.content.startswith('Hello'):

        await message.channel.send('Hello!')

        print('Message')

'''

bot.run(TOKEN)
