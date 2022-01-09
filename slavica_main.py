import discord
from discord.ext import commands
import pandas as pd
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from discord.utils import get
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import random
import configparser
import youtube_dl

# Read token################################
config = configparser.ConfigParser()
config.read_file(open(r'TOKEN.cfg'))
TOKEN = config.get('TOKENS', 'TOKEN_1')
############################################

bot = commands.Bot(command_prefix='!')


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

@bot.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot is playing')

    # check if the bot is already playing
    else:
        await ctx.send("Bot is already playing")
        return


@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

'''@ bot.event

async def on_message(message):

    if message.author == bot.user:

        return



    if message.content.startswith('Hello'):

        await message.channel.send('Hello!')

        print('Message')

'''

bot.run(TOKEN)
