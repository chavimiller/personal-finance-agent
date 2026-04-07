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
    data = pd.read_csv(uploaded_file, header=2, dtype=str, encoding='utf-8-sig')

    data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")

    st.subheader("Preview of your data")
    st.dataframe(data.head(50))

    st.subheader("Columns detected")
    st.write(data.columns)