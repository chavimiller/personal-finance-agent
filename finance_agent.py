import streamlit as st
import pandas as pd
import unicodedata 
import re

# STEP ONE: Split up all data in csv to tables
# STEP TWO: Decide which tables are relevant and discard the ones that are not
def is_header(row):
    row = [str(x).strip() for x in row]

    non_numeric_ratio = sum(not re.fullmatch(r"-?\d+(\.\d+)?", x.replace(",", "")) for x in row) / len(row)

    has_keywords = any(
        any(kw in cell for kw in ["יתרה", "זכות", "חובה", "סכום", "תאריך"])
        for cell in row
    )
    return non_numeric_ratio > 0.7 and (has_keywords or len(row) >= 4)

def split_data_tables(rows):
    tables = []
    current_table = [] # visually: tables = [[current_table], [current_table]]

    for row in rows:
        
        if all(str(x).strip() == "" for x in row):
            continue

        if is_header(row):
            if current_table: # if there is already a different table held in current_table
                tables.append(current_table) # then lets close out this table, add to tables list
                current_table = [row] # now lets start our new table with the row we are on
                continue
       
        if current_table:
                current_table.append(row)
        

    if current_table:
        tables.append(current_table)

    return tables

def is_transaction_table(table):

    # function to determine whether table is relevant to transactions or not

    if len(table) < 4:
        return False
    
    has_real_numbers = any(
        any(re.search(r"\d", str(cell)) for cell in row)
        for row in table[1:]
    )

    if not has_real_numbers:
        return False
    
    return True

st.title("Please upload your financial statement in CSV form to get started!")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file: 
    df = pd.read_csv(uploaded_file).dropna(axis='index', how='all')
    df = df.dropna(axis='columns', how='all')
    st.dataframe(df)

    rows = df.values.tolist()
    tables = split_data_tables(rows)

    relevant_tables = [t for t in tables if is_transaction_table(t)]
    # Have variable for current_table
    # Variable to hold all tables
    # Collecting = True/False ?
    # use is_header(line) to determine if given line is a header or not

    # if True, store line as first line of current_table, it will be index 0
        # loop through all lines
        # if line is blank, end current_table.
        # store current_table as table_1

    # if False, continue until we hit logic that returns True

# EXPECTED_HEADERS = [ 
#     "תאריך",  "הפעולה", "פרטים","אסמכתא" ,"חובה" , "זכות" , "יתרה בש''ח" , "תאריך ערך", "חיוב לתאריך", "שם בית עסק"
# ]

# def normalize_string(s):
#     s = str(s)
#     s = s.strip()                
#     s = s.replace("\u200f", "")     
#     s = s.replace("\xa0", "")      
#     s = s.replace('"', '')        
#     s = unicodedata.normalize('NFKC', s)  
#     return s

# def is_section_header(line):
#     line = line.strip()

#     if not line:
#         return False
#     if "\t" in line:
#         return False
#     if len(line) > 60:
#         return False
#     if re.search(r"[א-תA-Za-z]",line):
#         return True
#     return False

# def split_into_sections(lines):
#     sections = []
#     current_section = {"name": "unknown", "lines": []}
#     for line in lines:
#         line = line.strip()
#         if not line:
#             continue
#         if is_section_header(line): # if we encounter a section header
#             if current_section["lines"]: # if "lines": in current_section has any collected rows
#                 sections.append(current_section) # add the last section to the sections array
#             current_section = { # clear current section now and start new section
#                 "name" : line,
#                 "lines" : []
#             }
#         else:
#             current_section["lines"].append(line) # otherwise store this line inside the current section's line array
#     # the loop has finished
#     if current_section["lines"]: # if the current section has any collected rows
#         sections.append(current_section) # then add this last current section to the sections array
#     return sections # return all the sections

# def score_header_row(row):
#     print("DEBUG ROW:", row)
#     raw_text = normalize_string(" ".join(normalize_string(x) for x in row))
#     text_str = raw_text.lower()
#     score = 0

#     if 4 <= len(row) <= 10:
#         score += 1

#     positive_signals = [
#        "תאריך",
#         "אסמכתא",
#         "עסק",
#         "סכום",
#         "קנייה",
#         "חיוב",
#         "זכות"
#     ]
#     negative_phrases = [
#         "חיוב קודם"
#     ]

#     for phrase in negative_phrases:
#         if phrase in raw_text:
#             score -= 8
#             raw_text = raw_text.replace(phrase, "")
#             text_str = raw_text.lower()

#     for signal in positive_signals:
#         if signal in text_str:
#             score += 2
   
#     return score


# uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# if uploaded_file: 
#     text = uploaded_file.getvalue().decode("utf-8-sig")
#     raw_lines = text.splitlines()
    
#     sections = split_into_sections(raw_lines)

#     all_tables = []

#     for section in sections:
#         lines = section["lines"]
#         if len(lines) < 2:
#             continue

#         preview = pd.DataFrame(lines)

#         best_score = float("-inf")
#         best_index = None

#         for i, row in preview.iterrows():
#             score = score_header_row(row.tolist())
#             if score > best_score:
#                 best_score = score
#                 best_index = i

#             header = lines[best_index].split(",")   
#             header = [col.strip() for col in header]
#             header = [col if col != "" else f"unnamed_{i}" for i, col in enumerate(header)]

#             rows = []
#             for line in lines[best_index + 1:]:
#                 split_line = line.split(",")
#                 trimmed_line = split_line[:len(header)]
#                 rows.append(trimmed_line)
            
#             df = pd.DataFrame(rows, columns = header)
#             all_tables.append(df)

#         data = pd.concat(all_tables, ignore_index=True)

#     data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")
#     for col in data.columns:
#      data[col] = data[col].astype(str)

#     if 'תאריך' in data.columns:
#         data['תאריך'] = (
#             data['תאריך']
#             .astype(str)              
#             .str.strip()
#             .str.replace('\xa0', '', regex=False)  
#             .str.replace('\u200f', '', regex=False)
#             .str.replace('"', '', regex=False)      
#         )
#         data['תאריך'] = pd.to_datetime(data['תאריך'], dayfirst=True, errors='coerce')
#     st.subheader("Preview of your data")
#     st.dataframe(data.head(50))

# # TESTING OF SCORING

# def print_test():
#     test_rows = [
#         ["תאריך", "פרטים", "חובה", "זכות"],   # should be HIGH
#         ["01/01/2024", "שופרסל", "120", ""],  # should be LOW
#         ["חיוב קודם", "", "", ""],            # should be LOW
#     ]

#     for row in test_rows:
#         print(score_header_row(row))

# print_test()
# # Schema for transaction data
#     # {
#     #  "merchant": "rami levy",
#     #  "amount": 50.00,
#     #  "date": "05-02-2001",
#     #  "category": null || "groceries",
#     #  "source": "account XXXX-3456 || april_statement_creditcard"
#     # }
