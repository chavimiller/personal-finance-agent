import streamlit as st
import pandas as pd
import unicodedata 

st.title("Please upload your financial statement in CSV form to get started!")

EXPECTED_HEADERS = [ 
    "תאריך",  "הפעולה", "פרטים","אסמכתא" ,"חובה" , "זכות" , "יתרה בש''ח" , "תאריך ערך"
]

def normalize_string(s):
    s = str(s)
    s = s.strip()                
    s = s.replace("\u200f", "")     
    s = s.replace("\xa0", "")      
    s = s.replace('"', '')        
    s = unicodedata.normalize('NFKC', s)  
    return s

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file: 
    raw_data = pd.read_csv(uploaded_file, header=None, dtype=str)
    header_row_index = None

    for i, row in raw_data.iterrows():
        row_values = [normalize_string(c) for c in row]
        if row_values == EXPECTED_HEADERS:
            header_row_index = i
            break
    if header_row_index == None:
        st.error("Could not find expected headers.")  
    else:
        clean_data = pd.read_csv(uploaded_file, header=header_row_index, dtype=str)

        clean_data.columns = clean_data.columns.str.strip().str.lower().str.replace(" ", "_")

        st.subheader("Preview of your data")
        st.dataframe(clean_data.head(50))

        st.subheader("Columns detected")
        st.write(clean_data.columns)