import streamlit as st
import pandas as pd
import unicodedata 
import re

st.title("Please upload your financial statement in CSV form to get started!")

EXPECTED_HEADERS = [ 
    "תאריך",  "הפעולה", "פרטים","אסמכתא" ,"חובה" , "זכות" , "יתרה בש''ח" , "תאריך ערך", "חיוב לתאריך", "שם בית עסק"
]

def normalize_string(s):
    s = str(s)
    s = s.strip()                
    s = s.replace("\u200f", "")     
    s = s.replace("\xa0", "")      
    s = s.replace('"', '')        
    s = unicodedata.normalize('NFKC', s)  
    return s

def is_section_header(line):
    line = line.strip()

    if not line:
        return False
    if "\t" in line:
        return False
    if len(line) > 60:
        return False
    if re.search(r"[א-תA-Za-z]",line):
        return True
    return False

def split_into_sections(lines):
    sections = []
    current_section = {"name": "unknown", "lines": []}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if is_section_header(line): # if we encounter a section header
            if current_section["lines"]: # if "lines": in current_section has any collected rows
                sections.append(current_section) # add the last section to the sections array
            current_section = { # clear current section now and start new section
                "name" : line,
                "lines" : []
            }
        else:
            current_section["lines"].append(line) # otherwise store this line inside the current section's line array
    # the loop has finished
    if current_section["lines"]: # if the current section has any collected rows
        sections.append(current_section) # then add this last current section to the sections array
    return sections # return all the sections

def score_header_row(row):
    print("DEBUG ROW:", row)
    raw_text = normalize_string(" ".join(normalize_string(x) for x in row))
    text_str = raw_text.lower()
    score = 0

    if 4 <= len(row) <= 10:
        score += 1

    positive_signals = [
       "תאריך",
        "אסמכתא",
        "עסק",
        "סכום",
        "קנייה",
        "חיוב",
        "זכות"
    ]
    negative_phrases = [
        "חיוב קודם"
    ]

    for phrase in negative_phrases:
        if phrase in raw_text:
            score -= 8
            raw_text = raw_text.replace(phrase, "")
            text_str = raw_text.lower()

    for signal in positive_signals:
        if signal in text_str:
            score += 2
   
    return score


uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file: 
    text = uploaded_file.getvalue().decode("utf-8-sig")
    raw_lines = text.splitlines()
    preview = pd.read_csv(pd.io.common.StringIO(text), header=None, dtype=str)

    best_score = float("-inf")
    best_index = None

    for i, row in preview.iterrows():
        score = score_header_row(row.tolist())
        if score > best_score:
            best_score = score
            best_index = i

    data = pd.read_csv(pd.io.common.StringIO(text), header=best_index, dtype=str)

    data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")
    for col in data.columns:
     data[col] = data[col].astype(str)

    if 'תאריך' in data.columns:
        data['תאריך'] = (
            data['תאריך']
            .astype(str)              
            .str.strip()
            .str.replace('\xa0', '', regex=False)  
            .str.replace('\u200f', '', regex=False)
            .str.replace('"', '', regex=False)      
        )
        data['תאריך'] = pd.to_datetime(data['תאריך'], dayfirst=True, errors='coerce')
    st.subheader("Preview of your data")
    st.dataframe(data.head(50))

# TESTING OF SCORING

def print_test():
    test_rows = [
        ["תאריך", "פרטים", "חובה", "זכות"],   # should be HIGH
        ["01/01/2024", "שופרסל", "120", ""],  # should be LOW
        ["חיוב קודם", "", "", ""],            # should be LOW
    ]

    for row in test_rows:
        print(score_header_row(row))

print_test()
# Schema for transaction data
    # {
    #  "merchant": "rami levy",
    #  "amount": 50.00,
    #  "date": "05-02-2001",
    #  "category": null || "groceries",
    #  "source": "account XXXX-3456 || april_statement_creditcard"
    # }