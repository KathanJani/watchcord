###MEANT TO BE PLACED IN THE PARENT DIRECTORY. TO BE USED FOR TESTING PURPOSES ONLY.###
from celery import Celery
from scrapers.scrapers.spiders.amazon import run_spider2
import celery.schedules
from celery.schedules import crontab
from uuid import uuid4
from redbeat import RedBeatSchedulerEntry
from redbeat.schedules import rrule
import discord
from discord import SyncWebhook

celery_app = Celery(__name__)

celery_app.conf.broker_url="redis://localhost:6379"
celery_app.conf.result_backend="redis://localhost:6379"

# url_stuff="https://www.amazon.in/Steelbird-Sensitivity-Protective-Off-Road-Motorbike/dp/B09DYP3GCG/ref=sr_1_7?crid=2PQRTEIGU03ZC&dib=eyJ2IjoiMSJ9.kCMG2RKAD2JeEPl6E3mz3OHjuTyqEfwD7_j08jMEaKfad3bFU_O35D22MruYCL3Djas53tgOlBnA8Ha3kjH448kMkLdgihF9NbJZqQcnU4kcR96KFt7JOAAOLZ-NGuKJU37pzvalukQ-Ubb3I6P5zLKONeIyGauOIuIgu6MSb4h4fSjmAy07Efl8EBK52yXLQPUFztsWh9BaFbp0wCfh0t43Oi9_NonIcsbPmWYwXpMrddRCgyOQexrJ0B75vQTOlOcwVaO51Li4cucEYG29qTp8h8zOtlYPxJt5nZ8bV_o.mvMHMaBGoqZJrc7bdWe4AEqIjjg8gLkTs7mfzQUCqds&dib_tag=se&keywords=bike+gloves&qid=1729015657&sprefix=bike+glove%2Caps%2C227&sr=8-7"
# @celery_app.on_after_configure.connect
# def schedule_tasks(sender, *args, **kwargs):
#     sender.add_periodic_task(10.0,scrape_amazon_task.s(urls=url_stuff), expires=30)

@celery_app.task(name='watchcord.celery_workers.worker.random_task')
def random_task(name):
    print(f"Hello {name}")
    return "Hello"+name

@celery_app.task(name='watchcord.celery_workers.worker.scrape_amazon_task')
def scrape_amazon_task(urls: str):
    url_list = urls.split(',')
    data = run_spider2(url_list)
    print(f"Data: {data}")
    return data

# @celery_app.task(name='watchcord.celery_workers.worker.scrape_amazon_with_webhook_task')
# def scrape_amazon_with_webhook_task(urls: str, user: str):
#     webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1295990950216335400/X-8Y0HsMygXza-0MGBraAe15OA6msYj6oiWoW_2_GXAQCwAM429Lt_NUq--bpECIgkUe")
#     url_list = urls.split(',')
#     data = run_spider2(url_list)
#     print(f"Data: {data}")
#     print(f"Sending Data via Webhook: {webhook.url}")
#     for i in range(len(data['asins'])):
#         embed = discord.Embed(title=data['titles'][i], color=discord.Color.blue())
#         embed.set_author(name="Scraped Product")
#         embed.add_field(name="Price", value=data['prices'][i], inline=False)
#         embed.add_field(name="ASIN", value=data['asins'][i], inline=False)
#         embed.set_image(url=data["images"][i])
#         webhook.send(f"Hey <@{user}>! Here's your Scheduled data by Celery!",embed=embed)
#     return "Webhook Sent"

@celery_app.task(name='watchcord.celery_workers.worker.scrape_amazon_with_webhook_task')
def scrape_amazon_with_webhook_task(urls: str, user: str):
    webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1295990950216335400/X-8Y0HsMygXza-0MGBraAe15OA6msYj6oiWoW_2_GXAQCwAM429Lt_NUq--bpECIgkUe")
    url_list = urls.split(',')
    data = run_spider2(url_list)
    print(f"Data: {data}")
    print(f"Sending Data via Webhook: {webhook.url}")
    for i in range(len(data['asins'])):
        embed = discord.Embed(title=data['titles'][i], color=discord.Color.blue())
        embed.set_author(name=f"{user}'s Scraped Product")
        embed.add_field(name="Domain", value=data['domains'][i], inline=True)
        embed.add_field(name="Product ID", value=data['asins'][i], inline=True)
        embed.add_field(name="Rating", value=data['ratings'][i], inline=True)
        embed.add_field(name="MRP", value=data['mrps'][i], inline=True)
        embed.add_field(name="Discount", value=data['discount_percentages'][i], inline=True)
        embed.add_field(name="Current Price", value=data['current_prices'][i], inline=True)
        # embed.add_field(name="Categories", value=data['categories'][i], inline=False)
        embed.add_field(name="Categories", value=", ".join(category for category in data['categories'][i]), inline=False)
        # embed.add_field(name="Description", value=data['descriptions'][i][0:2], inline=False)
        embed.add_field(name="Description", value="\n".join(description for description in data['descriptions'][i][0:3]), inline=False)
        embed.set_image(url=data["images"][i])
        webhook.send(f"Hey <@{user}>! Here's your Scheduled data by Celery!",embed=embed)
    return "Webhook Sent"

# import requests
# @celery_app.task(name='watchcord.celery_workers.worker.scrape_amazon_with_webhook_task')
# def scrape_amazon_with_webhook_task(urls: str, user: str):
#     url_list = urls.split(',')
#     data = run_spider2(url_list)
#     print(f"Data: {data}")
#     response=requests.post(f"http://localhost:8000/webhooktest/{user}", json=data)
#     return {"Webhook Sent":response.text}

def schedule_tasks_with_redbeat(urls, schedule_for, user):
    interval = celery.schedules.schedule(run_every=schedule_for)
    entry = RedBeatSchedulerEntry(name="scrape_amazon_with_webhook_task"+str(uuid4()), task="watchcord.celery_workers.worker.scrape_amazon_with_webhook_task", schedule=interval, args=[urls, user], app=celery_app)
    entry.save()
    return {"status":"Task Scheduled", "task_key":entry.key}

def remove_scheduled_tasks_with_redbeat(entry_key):
    entry = RedBeatSchedulerEntry.from_key(entry_key, app=celery_app)
    entry.delete()
    return {"status":f"Task {entry_key} Deleted"}