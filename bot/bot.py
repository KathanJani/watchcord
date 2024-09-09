import discord
from discord import app_commands
from discord.ext import commands
import pandas as pd
import os
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="echo")
@app_commands.describe(echo_message = "Message To Echo:")
async def echo(interaction: discord.Interaction, echo_message: str):
    await interaction.response.send_message(f"{interaction.user.mention} echoes: `{echo_message}`")

@bot.tree.command(name="scrapeddemooutput")
async def scrapeddemooutput(interaction: discord.Interaction):
    embed = discord.Embed(title="Scraped Demo Output", description="This is a demo output of a scrape command", color=discord.Color.blue())
    embed.set_author(name=interaction.user.display_name)
    df = pd.read_csv('demodata/sampleproducts.csv')
    # embed.add_field(name="Field 1", value="Value 1", inline=False)
    for index, row in df.iterrows():
        embed.add_field(name=f"Product {index}", value=f"Title: {row['title']}\nPrice: {row['price']}", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="scrapedproductdemo")
async def scrapedproductdemo(interaction: discord.Interaction):
    df = pd.read_csv('demodata/sampleproducts.csv')
    product = df.iloc[1]
    embed = discord.Embed(title=product['title'], color=discord.Color.blue())
    embed.set_author(name="Scraped Product")
    embed.add_field(name="Price", value=product['price'], inline=False)
    image_url = "https://m.media-amazon.com/images/I/81citugjIUL._SL1500_.jpg"
    embed.set_image(url=image_url)
    await interaction.response.send_message(embed=embed)
    

bot.run(DISCORD_TOKEN) # type: ignore