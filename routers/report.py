from models import ReportModel
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

db = client.report

#Create report route 
#Report list , to check who already take this 
@app.post("/report", response_description="Add new report", response_model=ReportModel,tags=['Report'])
async def create_report(report: ReportModel = Body(...)):
    report = jsonable_encoder(report)
    new_report = await db["report"].insert_one(report)
    created_report = await db["report"].find_one({"_id": new_report.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_report)


@app.get(
    "/report", response_description="List all report", response_model=List[ReportModel],tags=['Report']
)
async def list_report():
    report= await db["report"].find().to_list(1000)
    return report

# metric and filter have problems 
@app.get("/report/{metric}", response_model=List[ReportModel], tags=['Report'])
async def get_report_metric(metric: str):
    with MongoClient() as client:
        report_metric = db.find({"metric":metric})
        response_msg_list = []
        for report in report_metric:
            response_msg_list.append(ReportModel(**report))
        return response_msg_list

@app.get(
    "/report/{filter_tape}", response_description="filter type ", response_model=ReportModel,tags=['Report']
)
async def show_report_metrics(filter_type: str):
    if (report := await db["report"].find_one({"filter_type": filter_type})) is not None:
        return report

    raise HTTPException(status_code=404, detail=f"report {filter_type} not found")



@app.delete("/report/{id}", response_description="Delete a report",tags=['Report'])
async def delete_report(id: str):
    delete_report = await db["report"].delete_one({"_id": id})

    if delete_report.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Report {id} not found")
