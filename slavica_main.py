import discord
from discord.ext import commands
import asyncio
from discord import FFmpegPCMAudio
import os
import random
import subprocess
import configparser
import yt_dlp
from openai import OpenAI
import urllib
from mflux import Flux1, Config
import datetime
import time

# Read token################################
config = configparser.ConfigParser()
config.read_file(open(r'TOKEN.cfg'))
TOKEN = config.get('TOKENS', 'TOKEN_1')
############################################

client = OpenAI(api_key=config.get('TOKENS', 'OPENAI_API_KEY'))

# Radio URLS
radio_urls = {
    'tdi': 'https://streaming.tdiradio.com/tdiradio.mp3',
    'bbc': 'http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one'
}

intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.voice_states = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load the model
flux = Flux1.from_name(
   model_name="dev",  # "schnell" or "dev"
   quantize=8,            # 4 or 8
)

""" 
def generate_flux_image(prompt):
    image = flux.generate_image(
    seed=2,
    prompt=prompt,
    config=Config(
        num_inference_steps=4,  # "schnell" works well with 2-4 steps, "dev" works well with 20-25 steps
        height=1024,
        width=1440,
    ),
    )
    return image
"""
def generate_flux_image(prompt, output_path):
    # Prepare output path
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Build the command
    command = [
        "mflux-generate",
        "--prompt", prompt,
        "--model", "dev",
        "--steps", "14",
        "--height", "768",
        "--width", "1024",
        "--seed", "1",
        "-q", "8",
        "--lora-paths", "lora/uberRealisticPornMerge_v13.safetensors",
        "--output", output_path
    ]

    # Run the command
    subprocess.run(command, check=True)

# Chat GPT text completion
def generate_text(prompt):
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ])
    return completion.choices[0].message.content

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not connected to a voice channel.")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

# PAINTED WORLD OF SLAVICA
@bot.command()
async def nacrtaj(ctx, prompt):
    date_prefix = datetime.datetime.now().strftime("%Y%m%d")
    rand_digits = random.randint(00, 99)
    filename = f"{date_prefix}_{rand_digits}_{prompt[0:40]}.jpg"
    os.makedirs('flux_images', exist_ok=True)
    image_path = os.path.join('flux_images', filename)
    generate_flux_image(prompt,image_path)
    # Save and ensure file is written
    #image.save(image_path, image_path)
    # Wait briefly to ensure file system sync (optional, but helps on some systems)
    await asyncio.sleep(1)    
    if os.path.exists(image_path):
        await ctx.send(file=discord.File(image_path))
    else:
        await ctx.send("Failed to generate image.")

@bot.command()
async def napisi(ctx, prompt):
    # Get AI generated text
    text_response = generate_text(prompt)
    await ctx.send(text_response)

@bot.command()
async def cibe(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def vine(ctx):
    vine_file_name = random.choice(os.listdir("Memes"))
    await ctx.send(file=discord.File(f"Memes/{vine_file_name}"))

@bot.command()
async def vic(ctx):
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    driver = webdriver.Chrome('chromedriver')
    driver.get("https://vicevi.net/site/best")
    vic_text = driver.find_element(By.XPATH, "//*[@class='col-lg-12']").text
    await ctx.send(vic_text)
    driver.quit()

@bot.command()
async def radio(ctx, url: str = random.choice(list(radio_urls.values()))):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await channel.connect()
        ctx.voice_client.play(FFmpegPCMAudio(url))
    else:
        await ctx.send("You are not connected to a voice channel.")

@bot.command()
async def ispovest(ctx):
    ispovest = random.choice(os.listdir("Ispovesti"))
    video_name = ispovest[:-4]
    video_link = f'Ispovesti/{ispovest}'

    if ctx.author.voice:
        if not ctx.voice_client:
            channel = ctx.author.voice.channel
            await channel.connect()

        FFMPEG_OPTIONS = {'options': '-vn'}
        ctx.voice_client.play(FFmpegPCMAudio(source=video_link, **FFMPEG_OPTIONS))
        await ctx.send(video_name)
    else:
        await ctx.send("You are not connected to a voice channel.")

@bot.command()
async def play(ctx, url: str):
    if ctx.author.voice:
        if not ctx.voice_client:
            channel = ctx.author.voice.channel
            await channel.connect()

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        ctx.voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
    else:
        await ctx.send("You are not connected to a voice channel.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
    else:
        await ctx.send("Currently no audio is playing.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
    else:
        await ctx.send("The audio is not paused.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    else:
        await ctx.send("No audio is currently playing.")

bot.run(TOKEN)
