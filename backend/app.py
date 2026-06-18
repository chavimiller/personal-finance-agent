from fastapi import FastAPI, UploadFile, File
from core.transactions import router as transaction_router

from core.parsing import split_data_tables
from core.transactions import is_transaction_table

app = FastAPI()

app.include_router(transaction_router, prefix="/transactions")

@app.get("/")
def home():
    return {"message": "backend is running!"}
