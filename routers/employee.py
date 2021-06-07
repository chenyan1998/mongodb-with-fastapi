from models import EmployeeModel,UpdateEmployeeModel
from pymongo import MongoClient
from database import app,client
from fastapi import APIRouter,Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

#Create User Route 
app = APIRouter(
    # prefix="/employee",
    # tags=['Employee']
)

db = client.employee

#Create employee route 
#Employee list , to check who already take this 
@app.post("/employee", response_description="Add new employee", response_model=EmployeeModel,tags=['Employee'])
async def create_employee(employee: EmployeeModel = Body(...)):
    employee = jsonable_encoder(employee)
    new_employee = await db["employees"].insert_one(employee)
    created_employee = await db["employees"].find_one({"_id": new_employee.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_employee)


@app.get(
    "/employee", response_description="List all employees", response_model=List[EmployeeModel],tags=['Employee']
)
async def list_employees():
    employees= await db["employees"].find().to_list(1000)
    return employees


@app.get(
    "/employee/{id}", response_description="Get a single employee", response_model=EmployeeModel,tags=['Employee']
)
async def show_employee(id: str):
    if (employee := await db["employees"].find_one({"_id": id})) is not None:
        return employee

    raise HTTPException(status_code=404, detail=f"employee {id} not found")

@app.put("/employee/{id}", response_description="Update an employee", response_model=EmployeeModel,tags=['Employee'])
async def update_employee(id: str, employee: UpdateEmployeeModel = Body(...)):
    employee = {k: v for k, v in employee.dict().items() if v is not None}

    if len(employee) >= 1:
        update_result = await db["employees"].update_one({"_id": id}, {"$set": employee})

        if update_result.modified_count == 1:
            if (
                updated_employee := await db["employees"].find_one({"_id": id})
            ) is not None:
                return updated_employee

    if (existing_employee := await db["employees"].find_one({"_id": id})) is not None:
        return existing_employee

    raise HTTPException(status_code=404, detail=f"employee {id} not found")

@app.delete("/employee/{id}", response_description="Delete an employee",tags=['Employee'])
async def delete_employee(id: str):
    delete_result = await db["employees"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Employee {id} not found")
