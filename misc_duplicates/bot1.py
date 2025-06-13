###MEANT TO BE PLACED IN THE PARENT DIRECTORY. TO BE USED FOR TESTING PURPOSES ONLY.###
import discord
from discord import app_commands
from discord.ext import commands
import pandas as pd
import os
from scrapers.scrapers.spiders.amazon import run_spider
# import requests
import aiohttp
import logging
# from dotenv import load_dotenv

discord.utils.setup_logging(level=logging.DEBUG, root=False)
# DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# if not DISCORD_TOKEN:
#     load_dotenv()
#     DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
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

# @bot.tree.command(name="scrapedproductdemo")
# async def scrapedproductdemo(interaction: discord.Interaction):
#     df = pd.read_csv('demodata/sampleproducts.csv')
#     product = df.iloc[1]
#     embed = discord.Embed(title=product['title'], color=discord.Color.blue())
#     embed.set_author(name="Scraped Product")
#     embed.add_field(name="Price", value=product['price'], inline=False)
#     image_url = "https://m.media-amazon.com/images/I/81citugjIUL._SL1500_.jpg"
#     embed.set_image(url=image_url)
#     await interaction.response.send_message(embed=embed)
    
# async def get_spider_data(url_to_scrape):
#     response = requests.get("http://localhost:8000/scrapeamazon/", params={"url":url_to_scrape})
#     return response.json()
async def get_spider_data(urls_to_scrape):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/scrapeamazon/', params={"urls":urls_to_scrape}) as response:
            response_data = await response.json()
    return response_data

async def get_test_celery(name):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/testcelery/', params={"name":name}) as response:
            response_data = await response.text()
    return response_data

async def get_celery_spider_data(urls_to_scrape):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/scrapeamazoncelery/', params={"urls":urls_to_scrape}) as response:
            response_data = await response.json()
    return response_data

async def get_test_celery_schedule(test_url, test_schedule, user):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/scheduletaskdemo/', params={"urls":test_url,"test_schedule":test_schedule, "user":user}) as response:
            response_data = await response.json()
    return response_data

async def get_test_celery_schedule_delete(test_key):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/deletescheduledtaskdemo/', params={"key":test_key}) as response:
            response_data = await response.json()
    return response_data

# @bot.tree.command(name="amazonscrapingdemo")
# @app_commands.describe(urls_to_scrape = "URL To Scrape:")
# async def amazonscrapingdemo(interaction: discord.Interaction, urls_to_scrape: str):
#     await interaction.response.defer()
#     spider_data = await get_spider_data(urls_to_scrape=urls_to_scrape)
#     for i in range(len(spider_data['asins'])):
#         embed = discord.Embed(title=spider_data['titles'][i], color=discord.Color.blue())
#         embed.set_author(name="Scraped Product")
#         embed.add_field(name="Price", value=spider_data['prices'][i], inline=False)
#         embed.add_field(name="ASIN", value=spider_data['asins'][i], inline=False)
#         embed.set_image(url=spider_data["images"][i])
#         await interaction.followup.send(f"Hey {interaction.user.mention}! Here's your data!",embed=embed)
#     # await interaction.response.send_message(embed=embed)
#     # await interaction.followup.send(f"{spider_data}")

@bot.tree.command(name="amazonscrapingdemo")
@app_commands.describe(urls_to_scrape = "URL To Scrape:")
async def amazonscrapingdemo(interaction: discord.Interaction, urls_to_scrape: str):
    await interaction.response.defer()
    spider_data = await get_spider_data(urls_to_scrape=urls_to_scrape)
    for i in range(len(spider_data['asins'])):
        embed = discord.Embed(title=spider_data['titles'][i], color=discord.Color.blue())
        embed.set_author(name=f"{interaction.user.display_name}'s Scraped Product")
        embed.add_field(name="Domain", value=spider_data['domains'][i], inline=True)
        embed.add_field(name="Product ID", value=spider_data['asins'][i], inline=True)
        embed.add_field(name="Rating", value=spider_data['ratings'][i], inline=True)
        embed.add_field(name="MRP", value=spider_data['mrps'][i], inline=True)
        embed.add_field(name="Discount", value=spider_data['discount_percentages'][i], inline=True)
        embed.add_field(name="Current Price", value=spider_data['current_prices'][i], inline=True)
        # embed.add_field(name="Categories", value=spider_data['categories'][i], inline=False)
        embed.add_field(name="Categories", value=", ".join(category for category in spider_data['categories'][i]), inline=False)
        # embed.add_field(name="Description", value=spider_data['descriptions'][i][0:2], inline=False)
        embed.add_field(name="Description", value="\n".join(description for description in spider_data['descriptions'][i][0:3]), inline=False)
        embed.set_image(url=spider_data["images"][i])
        await interaction.followup.send(f"Hey {interaction.user.mention}! Here's your data!",embed=embed)
    # await interaction.response.send_message(embed=embed)
    # await interaction.followup.send(f"{spider_data}")

@bot.tree.command(name="test_celery")
@app_commands.describe(test_name = "Name To Test Celery:")
async def test_celery(interaction: discord.Interaction, test_name: str):
    await interaction.response.defer()
    celery_data = await get_test_celery(name=test_name)
    await interaction.followup.send(f"{interaction.user.mention} celery says: `{celery_data}`")

# from celery.result import AsyncResult
@bot.tree.command(name="scrape_amazon_celery_demo")
@app_commands.describe(urls_to_scrape = "URL To Scrape:")
async def scrape_amazon_celery_demo(interaction: discord.Interaction, urls_to_scrape: str):
    await interaction.response.defer()
    celery_spider_data = await get_celery_spider_data(urls_to_scrape=urls_to_scrape)
    # await interaction.followup.send(f"Hey {interaction.user.mention}! Celery is processing your task: {celery_spider_data}")
    # while AsyncResult(celery_spider_data["task_id"]).status == 'PENDING':
    #     continue
    # await interaction.followup.edit_message(message_id=interaction.id,content=f"Hey{interaction.user.mention}! Celery has processed your data: {AsyncResult(celery_spider_data["task_id"]).result}")
    # await interaction.followup.send(f"Hey {interaction.user.mention}! Celery gave: {celery_spider_data}")
    for i in range(len(celery_spider_data["task_result"]['asins'])):
        embed = discord.Embed(title=celery_spider_data["task_result"]['titles'][i], color=discord.Color.blue())
        embed.set_author(name="Scraped Product")
        embed.add_field(name="Price", value=celery_spider_data["task_result"]['prices'][i], inline=False)
        embed.add_field(name="ASIN", value=celery_spider_data["task_result"]['asins'][i], inline=False)
        embed.set_image(url=celery_spider_data["task_result"]["images"][i])
        await interaction.followup.send(f"Hey {interaction.user.mention}! Here's your data by Celery!",embed=embed)

@bot.tree.command(name="test_celery_scheduling")
@app_commands.describe(test_url = "URL To Track:", test_schedule = "Schedule For Task(in seconds):")
async def test_celery_scheduling(interaction: discord.Interaction, test_url: str, test_schedule: int):
    await interaction.response.defer()
    celery_scheduled_data = await get_test_celery_schedule(test_url=test_url, test_schedule=test_schedule, user=interaction.user.id)
    await interaction.followup.send(f"{interaction.user.mention} celery says: `{celery_scheduled_data}`")

@bot.tree.command(name="test_celery_schedule_delete")
@app_commands.describe(test_key = "Key To Delete:")
async def test_celery_schedule_delete(interaction: discord.Interaction, test_key: str):
    await interaction.response.defer()
    celery_deleted_schedule_data = await get_test_celery_schedule_delete(test_key=test_key)
    await interaction.followup.send(f"{interaction.user.mention} celery says: `{celery_deleted_schedule_data}`")

bot.run(DISCORD_TOKEN) # type: ignore