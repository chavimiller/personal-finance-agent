import pandas as pd
from io import BytesIO

from core.parsing import split_data_tables
from core.transactions import is_transaction_row, is_transaction_table

async def process_csv_controller(file):
    content = await file.read()

    df = pd.read_csv(BytesIO(content), encoding="utf-8-sig")
    df = df.dropna(axis="columns", how="all")

    rows = df.values.tolist()

    tables = split_data_tables(rows)

    result_tables = []

    for table in tables:
        if not is_transaction_table(table):
            continue

        header = table[0]

        data_rows = [
            r[:len(header)]
            for r in table[1:]
            if is_transaction_row(r)
        ]

        if not data_rows:
            continue

        table_df = pd.DataFrame(data_rows)

        table_df.columns = [
             str(col).strip() if col else f"col_{i}"
             for i, col in enumerate(header[:len(table_df.columns)])
             ]
        result_tables.append(
            table_df.to_dict(orient="records")
        )

    return {
        "tables" : result_tables
    }
