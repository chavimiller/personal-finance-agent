import re 
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

def is_transaction_row(row):
    row = [str(x).strip() for x in row if str(x).strip() != ""]

    if len(row) < 2:
        return False
    
    text = " ".join(row)

    has_date = bool(re.search(r"\d{1,2}[./-]\d{1,2}[./-]\d{2,4}", text))

    has_money = bool(re.search(r"-?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?", text))

    looks_like_metadata = any(
        kw in text for kw in ["מספר חשבון", "תאריך הפקה", "תנועות בחשבון"]
    )

    return has_date and has_money and not looks_like_metadata

def is_transaction_table(table):

    # function to determine whether table is relevant to transactions or not 

    if len(table) < 2:
        return False

    data_rows = table[1:]

    transaction_rows = sum(
        is_transaction_row(row) for row in data_rows
    )
    return transaction_rows >= 1
