from fastapi import FastAPI, Body, HTTPException, status
import motor.motor_asyncio
from pymongo import MongoClient
import os

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
