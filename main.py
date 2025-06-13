from dotenv import load_dotenv
# import sys
# import os
# sys.path.insert(1,os.path.dirname(os.path.abspath(__file__)))
# from celery import Celery
# from fastapi import FastAPI
# from .api.api import router
# from .scrapers.scrapers.spiders.amazon import run_spider
# import discord
# from discord import SyncWebhook
# from .celery_workers.worker import random_task, scrape_amazon_task, schedule_tasks_with_redbeat, remove_scheduled_tasks_with_redbeat
# from celery.result import AsyncResult
load_dotenv()
# celery_app = Celery(__name__, broker="redis://localhost:6379", backend="redis://localhost:6379", include=["celery_tasks.tasks"])
# app = FastAPI()
# app.include_router(router)

# async def printstuff(url:str):
#     data = await run_spider([url])
#     print(data)

# @app.get("/scrapeamazon/")
# async def scrape_amazon(background_tasks: BackgroundTasks, url: str):
#     background_tasks.add_task(printstuff, url)
#     return {"data": "task added"}

# @app.get("/scrapeamazon/")
# async def scrape_amazon(urls: str):
#     url_list = urls.split(',')
#     data = await run_spider(url_list)
#     return data

# @app.get("/testcelery/")
# async def test_celery(name:str):
#     task = random_task.delay(name)
#     task_result = AsyncResult(task.id)
#     return task_result.result

# @app.get("/scrapeamazoncelery/")
# async def scrape_amazon_celery(urls:str):
#     task = scrape_amazon_task.delay(urls)
#     # task_result = AsyncResult(task.id)
#     while AsyncResult(task.id).status == 'PENDING':
#         continue
#     task_result = AsyncResult(task.id)
#     return {"task_id":task_result.id, "task_status":task_result.status, "task_result":task_result.result}

# @app.get("/scheduletaskdemo/")
# async def schedule_task_demo(urls:str, test_schedule:int, user:str):
#     scheduled_task=schedule_tasks_with_redbeat(urls, test_schedule, user)
#     return {"task":str(scheduled_task)}

# @app.get("/deletescheduledtaskdemo/")
# async def delete_scheduled_task_demo(key:str):
#     deleted_scheduled_task=remove_scheduled_tasks_with_redbeat(key)
#     return {"task":str(deleted_scheduled_task)}

# @app.post("/webhooktest/{user_id}")
# async def webhooktest(user_id: str, webhook_data: dict = Body(...)):
#     webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1295990950216335400/X-8Y0HsMygXza-0MGBraAe15OA6msYj6oiWoW_2_GXAQCwAM429Lt_NUq--bpECIgkUe")
#     print(f"Sending Data via Webhook: {webhook.url}")
#     for i in range(len(webhook_data['asins'])):
#         embed = discord.Embed(title=webhook_data['titles'][i], color=discord.Color.blue())
#         embed.set_author(name="Scraped Product")
#         embed.add_field(name="Price", value=webhook_data['prices'][i], inline=False)
#         embed.add_field(name="ASIN", value=webhook_data['asins'][i], inline=False)
#         embed.set_image(url=webhook_data["images"][i])
#         webhook.send(content=f"Hey <@{user_id}>! Here's your Scheduled data by Celery!",embed=embed, username="WatchCordBot#4259")
#     return {"status":"Webhook sent"}

if __name__ == "__main__":
    # from celery_tasks.tasks import celery_app
    from bot.bot import bot
    import os
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    if not DISCORD_TOKEN:
        load_dotenv()
        DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(DISCORD_TOKEN) # type: ignore