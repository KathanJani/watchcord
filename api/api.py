from fastapi import APIRouter, Body
from ..scrapers.scrapers.spiders.amazon import run_spider
from ..scrapers.scrapers.spiders.flipkart import run_flipkart_spider
import discord
from discord import SyncWebhook
from ..celery_tasks.tasks import random_task, scrape_amazon_task, schedule_tasks_with_redbeat, remove_scheduled_tasks_with_redbeat, scrape_flipkart_task, schedule_flipkart_tasks_with_redbeat, remove_flipkart_scheduled_tasks_with_redbeat
from celery.result import AsyncResult

router = APIRouter()

# async def printstuff(url:str):
#     data = await run_spider([url])
#     print(data)

# @router.get("/scrapeamazon/")
# async def scrape_amazon(background_tasks: BackgroundTasks, url: str):
#     background_tasks.add_task(printstuff, url)
#     return {"data": "task added"}

@router.get("/scrapeamazon/")
async def scrape_amazon(urls: str):
    url_list = urls.split(',')
    data = await run_spider(url_list)
    return data

@router.get("/scrapeflipkart/")
async def scrape_flipkart(urls: str):
    url_list = urls.split(',')
    data = await run_flipkart_spider(url_list)
    return data

@router.get("/testcelery/")
async def test_celery(name:str):
    task = random_task.delay(name)
    task_result = AsyncResult(task.id)
    return task_result.result

@router.get("/scrapeamazoncelery/")
async def scrape_amazon_celery(urls:str):
    task = scrape_amazon_task.delay(urls)
    # task_result = AsyncResult(task.id)
    while AsyncResult(task.id).status == 'PENDING':
        continue
    task_result = AsyncResult(task.id)
    return {"task_id":task_result.id, "task_status":task_result.status, "task_result":task_result.result}

@router.get("/scrapeflipkartcelery/")
async def scrape_flipkart_celery(urls:str):
    task = scrape_flipkart_task.delay(urls)
    # task_result = AsyncResult(task.id)
    while AsyncResult(task.id).status == 'PENDING':
        continue
    task_result = AsyncResult(task.id)
    return {"task_id":task_result.id, "task_status":task_result.status, "task_result":task_result.result}

@router.get("/scheduletaskdemo/")
async def schedule_task_demo(urls:str, test_schedule:int, user:str):
    scheduled_task=schedule_tasks_with_redbeat(urls, test_schedule, user)
    return {"task":str(scheduled_task)}

@router.get("/deletescheduledtaskdemo/")
async def delete_scheduled_task_demo(key:str):
    deleted_scheduled_task=remove_scheduled_tasks_with_redbeat(key)
    return {"task":str(deleted_scheduled_task)}

@router.get("/scheduleflipkarttaskdemo/")
async def schedule_flipkart_task_demo(urls:str, test_schedule:int, user:str):
    scheduled_task=schedule_flipkart_tasks_with_redbeat(urls, test_schedule, user)
    return {"task":str(scheduled_task)}

@router.get("/deleteflipkartscheduledtaskdemo/")
async def delete_flipkart_scheduled_task_demo(key:str):
    deleted_scheduled_task=remove_flipkart_scheduled_tasks_with_redbeat(key)
    return {"task":str(deleted_scheduled_task)}

@router.post("/webhooktest/{user_id}")
async def webhooktest(user_id: str, webhook_data: dict = Body(...)):
    webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1295990950216335400/X-8Y0HsMygXza-0MGBraAe15OA6msYj6oiWoW_2_GXAQCwAM429Lt_NUq--bpECIgkUe")
    print(f"Sending Data via Webhook: {webhook.url}")
    for i in range(len(webhook_data['asins'])):
        embed = discord.Embed(title=webhook_data['titles'][i], color=discord.Color.blue())
        embed.set_author(name="Scraped Product")
        embed.add_field(name="Price", value=webhook_data['prices'][i], inline=False)
        embed.add_field(name="ASIN", value=webhook_data['asins'][i], inline=False)
        embed.set_image(url=webhook_data["images"][i])
        webhook.send(content=f"Hey <@{user_id}>! Here's your Scheduled data by Celery!",embed=embed, username="WatchCordBot#4259")
    return {"status":"Webhook sent"}