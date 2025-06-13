import pymongo
import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..models.models import User, TrackedProduct, ScheduledTask
from datetime import date, datetime
from bson import ObjectId
from pydantic_core import Url

MONGODB_URI = os.getenv('MONGODB_URI')

def mongo_compat_conv(dict_obj: dict) -> dict:
    for key,value in dict_obj.items():
        if type(value) is date or type(value) is datetime or type(value) is Url:
            dict_obj[key] = str(value)
    return dict_obj

# For MongoDB responses 
def json_compat_conv(mongo_dict_obj: dict) -> dict:
    for key,value in mongo_dict_obj.items():
        if type(value) is ObjectId:
            mongo_dict_obj[key] = str(value)
        elif type(value) is list:
            for i in range(0,len(value)):
                if type(value[i]) is dict:
                    for k,v in value[i].items():
                        if type(v) is ObjectId:
                            value[i][k] = str(v)
    return mongo_dict_obj

try:
    connection = pymongo.MongoClient(MONGODB_URI)
    db = connection.watchcorddb
    print("Connected to Database")

    dbrouter = APIRouter()

    @dbrouter.get("/getalltrackedproducts/")
    async def get_all_tracked_products():
        tracked_products = db.trackedproducts.find()
        return {"tracked_products": [product for product in tracked_products]}
    
    @dbrouter.post("/createuser/", status_code=201, response_class=JSONResponse)
    async def create_user(register_user: User) -> JSONResponse:
        create_user_check = db.Users.find_one({"discord_id" : register_user.discord_id})
        if create_user_check:
            return JSONResponse({"message" : "User Already Exists"},status_code=409)
        user_dict = register_user.model_dump()
        mongo_compat_create_user_dict = mongo_compat_conv(user_dict)
        create_user_query = db.Users.insert_one(mongo_compat_create_user_dict)
        if not create_user_query:
            return JSONResponse({"message" : "Internal Server Error"},status_code=500)
        return JSONResponse(content={"message" : "User Successfully Created", "id" : str(create_user_query.inserted_id)})
    
    @dbrouter.get("/readuser/{discord_id}", status_code=200, response_model= User)
    async def read_user(discord_id: str) -> User | JSONResponse:
        read_user_query = db.Users.find_one({"discord_id": discord_id})
        if not read_user_query:
            return JSONResponse(content={"message" : "User Not Found"},status_code=404)
        else:
            read_user_query = json_compat_conv(read_user_query)
        # return JSONResponse(content=read_user_query)
        return User(**read_user_query)
    
    @dbrouter.put("/updateuser/{discord_id}", status_code=200, response_class=JSONResponse)
    async def update_user(discord_id: str, update_user_data: User) -> JSONResponse:
        update_user_check = db.Users.find_one({"discord_id" : discord_id})
        if not update_user_check:
            return JSONResponse(content={"message" : "User Not Found"},status_code=404)
        update_user_data_dict = update_user_data.model_dump(exclude_unset=True)
        update_secure_user_dict = User(**update_user_data_dict).model_dump(exclude_unset=True)
        mongo_compat_update_user_dict = mongo_compat_conv(update_secure_user_dict)
        update_user_query = db.Users.update_one({"discord_id": discord_id}, {"$set": mongo_compat_update_user_dict})
        if not update_user_query:
            return JSONResponse({"message" : "Internal Server Error"},status_code=500)
        return JSONResponse(content={"message" : "User Successfully Updated", "user_id" : str(update_user_check["_id"])})
    
    @dbrouter.delete("/deleteuser/{discord_id}", status_code=200, response_class=JSONResponse)
    async def delete_user(discord_id: str) -> JSONResponse:
        delete_user_check = db.Users.find_one({"discord_id" : discord_id})
        if not delete_user_check:
            return JSONResponse(content={"message" : "User Not Found"},status_code=404)
        delete_user_query = db.Users.delete_one({"discord_id": discord_id})
        if not delete_user_query:
            return JSONResponse({"message" : "Internal Server Error"},status_code=500)
        return JSONResponse(content={"message" : "User Successfully Deleted", "deleted_user_id" : str(delete_user_check["_id"])})
    
    @dbrouter.post("/createtrackedproduct/", status_code=201, response_class=JSONResponse)
    async def create_tracked_product(scraped_product: TrackedProduct) -> JSONResponse:
        create_tracked_product_check = db.trackedproducts.find_one({"product_id" : scraped_product.product_id})
        if create_tracked_product_check:
            if create_tracked_product_check["product_id"] == scraped_product.product_id:
                return JSONResponse({"message" : "Product Already Exists"},status_code=409)
        scraped_product_dict = scraped_product.model_dump()
        mongo_compat_create_tracked_product_dict = mongo_compat_conv(scraped_product_dict)
        create_tracked_product_query = db.trackedproducts.insert_one(mongo_compat_create_tracked_product_dict)
        if not create_tracked_product_query:
            return JSONResponse({"message" : "Internal Server Error"},status_code=500)
        return JSONResponse(content={"message" : "Tracked Product Successfully Created", "id" : str(create_tracked_product_query.inserted_id)})
    
    @dbrouter.put("/updatetrackedproduct/{domain}/{product_id}", status_code=200, response_class=JSONResponse)
    async def update_tracked_product(domain: str, product_id: str, update_scraped_product_data: TrackedProduct) -> JSONResponse:
        update_tracked_product_check = db.trackedproducts.find_one({"$and": [{"product_id" : product_id}, {"domain" : domain}]})
        if not update_tracked_product_check:
            return JSONResponse(content={"message" : "User Not Found"},status_code=404)
        update_scraped_product_dict = update_scraped_product_data.model_dump(exclude_unset=True)
        update_tracked_product_dict = TrackedProduct(**update_scraped_product_dict).model_dump(exclude_unset=True)
        mongo_compat_update_tracked_product_dict = mongo_compat_conv(update_tracked_product_dict)
        update_tracked_product_query = db.trackedproducts.update_one({"$and": [{"product_id" : product_id}, {"domain" : domain}]}, {"$set": mongo_compat_update_tracked_product_dict})
        if not update_tracked_product_query:
            return JSONResponse({"message" : "Internal Server Error"},status_code=500)
        return JSONResponse(content={"message" : "Tracked Product Successfully Updated", "id" : str(update_tracked_product_check["_id"])})

except Exception as e:
    print("Error connecting to Database coz: ", e)