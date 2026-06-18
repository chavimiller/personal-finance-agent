from fastapi import FastAPI
from routes.transaction_router import router as transaction_router
from routes.categories_router import router as categories_router

app = FastAPI()

app.include_router(transaction_router, prefix="/transactions", tags=["Transactions"])
app.include_router(categories_router, prefix="/categories", tags=["Categories"])

@app.get("/")
def home():
    return {"message": "backend is running!"}
