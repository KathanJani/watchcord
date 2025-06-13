from fastapi import FastAPI
import sys
import os
sys.path.insert(1,os.path.dirname(os.path.abspath(__file__)))
from .api.api import router
from.api.db.dbstuff import dbrouter

app = FastAPI()
app.include_router(router)
app.include_router(dbrouter)