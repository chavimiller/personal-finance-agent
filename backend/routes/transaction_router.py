from fastapi import APIRouter, UploadFile, File
from controllers.transaction_controller import process_csv_controller

router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(file:UploadFile = File(...)):
   return await process_csv_controller(file)

