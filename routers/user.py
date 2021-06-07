import models
from models import UpdateUserModel,UserModel
from pymongo import MongoClient
import database
from database import app,client
from fastapi import APIRouter, Depends, FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List

#Create User Route 
app = APIRouter(
    # prefix="/user",
    # tags=['Users']
)

db = client.user

#Create student route 
@app.post("/user", response_description="Add new user", response_model=UserModel,tags=['Users'])
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await db["students"].insert_one(user)
    created_user = await db["students"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@app.get(
    "/user", response_description="List all user", response_model=List[UserModel],tags=['Users']
)
async def list_users():
    users = await db["students"].find().to_list(1000)
    return users


@app.get(
    "/user/{id}", response_description="Get a single user", response_model=UserModel,tags=['Users']
)
async def show_user(id: str):
    if (user := await db["students"].find_one({"_id": id})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"user {id} not found")


@app.put("/user/{id}", response_description="Update a user", response_model=UserModel,tags=['Users'])
async def update_user(id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = await db["students"].update_one({"_id": id}, {"$set": user})

        if update_result.modified_count == 1:
            if (
                updated_user := await db["students"].find_one({"_id": id})
            ) is not None:
                return updated_user

    if (existing_user := await db["students"].find_one({"_id": id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"user {id} not found")


@app.delete("/user/{id}", response_description="Delete a user",tags=['Users'])
async def delete_user(id: str):
    delete_result = await db["students"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {id} not found")
