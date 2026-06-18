import pandas as pd
import re

def is_header(row):
    row = [str(x).strip() for x in row if str(x).strip() != ""]
    
    if len(row) < 3:    
        return False

    numeric_count = sum(
        bool(re.fullmatch(r"-?\d+([.,]\d+)?", x.replace(",", "")))
        for x in row
    )

    non_numeric_ratio = (len(row) - numeric_count) / len(row)

    keywords = ["תאריך", "זכות", "חובה", "סכום", "יתרה", "פרטים", "אסמכתא", "מספר", 'חשבון']

    keyword_matches = sum(
        any(kw in cell for kw in keywords)
        for cell in row
    )

    has_date_like = any(
        re.search(r"\d{1,2}/\d{1,2}/\d{2,4}", cell)
        for cell in row
    )
    
    return (
        non_numeric_ratio > 0.8 and     
        keyword_matches >= 2 and        
        not has_date_like              
    ) 

def split_data_tables(rows):
    tables = []
    current_table = [] # visually: tables = [[current_table], [current_table]]
    headers = []

    for row in rows:
        
        if all(str(x).strip() == "" for x in row):
            if current_table:
                tables.append(current_table)
                current_table = []
            continue
        
        if is_header(row):
            headers.append(row)

            if current_table: # if there is already a different table held in current_table
                tables.append(current_table) # then lets close out this table, add to tables list
            current_table = [row] # now lets start our new table with the row we are on
            continue
       
        if current_table:
                current_table.append(row)
        

    if current_table:
        tables.append(current_table)

    return tables, headers