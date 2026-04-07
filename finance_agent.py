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

    data['חובה'] = data['חובה'].str.replace(",", '', regex=True).astype(float)
    data['זכות'] = data['זכות'].str.replace(',', '', regex=True).astype(float)
    data['אסמכתא'] = data['אסמכתא'].astype(float)

    data['תאריך'] = (
        data['תאריך']
        .astype(str)                 # ensure it's string
        .str.strip()                 # remove leading/trailing spaces
        .str.replace('\xa0', '', regex=False)   # non-breaking spaces
        .str.replace('\u200f', '', regex=False) # right-to-left marks
        .str.replace('"', '', regex=False)      # remove quotes
    )
    data['תאריך'] = pd.to_datetime(data['תאריך'], dayfirst=True, errors='coerce')
    data['year_month'] = data['תאריך'].dt.to_period('M')
    monthly_spending = data.groupby('year_month')['חובה'].sum().reset_index()
    monthly_spending['year_month'] = monthly_spending['year_month'].astype(str)

    st.subheader("Preview of your data")
    st.dataframe(data.head(50))

    st.subheader("Columns detected")
    st.write(data.columns)

    st.subheader("Total Spending per Month")
    st.line_chart(
        data=monthly_spending.set_index('year_month')['חובה']
    )
