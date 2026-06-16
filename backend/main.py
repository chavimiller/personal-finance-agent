from fastapi import FastAPI, UploadFile, File
import pandas as pd

from core.parsing import split_data_tables
from core.transactions import is_transaction_table

app = FastAPI()