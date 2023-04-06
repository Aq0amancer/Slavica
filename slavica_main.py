import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import random
import configparser
import yt_dlp
import openai
import urllib

# Read token################################
config = configparser.ConfigParser()
config.read_file(open(r'TOKEN.cfg'))
TOKEN = config.get('TOKENS', 'TOKEN_1')
openai.api_key=config.get('TOKENS', 'OPENAI_API_KEY')
############################################
# Radio URLS
radio_urls={'tdi':'https://streaming.tdiradio.com/tdiradio.mp3','bbc':'http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one'}

bot = commands.Bot(command_prefix='!')

## Open AI

def generate_image(prompt):
    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="256x256"
    )
    return response['data'][0]['url']

# Chat GPT text completion
def generate_text(prompt):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message.content

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

# PAINTED WORLD OF SLAVICA
@bot.command()
async def nacrtaj(ctx,prompt):
    # Get AI generated image
    image_url=generate_image(prompt)
    image_path=f'/home/pi/Slavica/openai_images/{prompt}.jpg'
    urllib.request.urlretrieve(image_url, image_path)
    await ctx.send(file=discord.File(image_path))

@bot.command()
async def napisi(ctx,prompt):
    # Get AI generated image
    text_response=generate_text(prompt)
    await ctx.send(text_response)

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
async def radio(ctx, url: str = random.choice(list(radio_urls.values()))):
    channel = ctx.message.author.voice.channel
    global player
    try:
        player = await channel.connect()
    except:
        pass
    player.play(FFmpegPCMAudio(random.choice(list(radio_urls.values()))))


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
async def play(ctx, url : str):

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if ctx.voice_client is None:

        channel = ctx.author.voice.channel

        await channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],'noplaylist' : 1,
    }

    server = ctx.message.guild

    voice_channel = server.voice_client

    if not voice_channel.is_playing():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice_channel.play(discord.FFmpegPCMAudio("song.mp3"))\

        voice_channel.is_playing()

    else:

        await ctx.send("Cekaj da se zavrsi play ili kucaj '!stop'.")

    return
    

@bot.command()
async def leave(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client.is_connected():
        await voiceChannel.disconnect()
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
