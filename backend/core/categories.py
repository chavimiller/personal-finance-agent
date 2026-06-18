import pandas as pd

import unicodedata 
from pathlib import Path



import json
CATEGORY_FILE = Path("vendors.json")




def loading_categories():
    try:
        if CATEGORY_FILE.exists():
            with open(CATEGORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        return {}
    return 

def save_categories(data):
    with open(CATEGORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

CATEGORY_RULES_HE = loading_categories()

st.title("Please upload your bank or credit card statement in CSV form to get started!")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file: 
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
    except Exception:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding="latin1")
    df = df.dropna(axis='columns', how='all')
    
    st.dataframe(df)

    rows = df.values.tolist()

    result = split_data_tables(rows)

    if not isinstance(result, tuple) or len(result) != 2:
        st.error("split_data_tables did not return expected output")
        st.stop()
    
    tables, headers = result
    
    st.write("DEBUG: split complete")

    st.write(f"Total tables found: {len(tables)}")
    st.write(f"Total headers detected: {len(headers)}")
 
    relevant_tables = [t for t in tables if is_transaction_table(t)]

    if relevant_tables:
        st.subheader("Detected transaction tables")
        for i, table in enumerate(relevant_tables):
            st.write(f"Table {i+1}")
            header = table[0]

            table_rows = [
                r[:len(header)]
                for r in table[1:]
                if is_transaction_row(r)
            ]

            table_df = pd.DataFrame(table_rows)
            
            clean_header = [
                str(col).strip() if pd.notna(col) else f"Unnamed_{i}"
                for i, col in enumerate(header[:len(table_df.columns)])
            ]

            table_df.columns = clean_header

            st.dataframe(table_df)

            st.subheader("Categorize Transactions")

            for i, row in table_df.iterrows(): # for each transaction row
                if "שם בית עסק" in table_df.columns:
                    description = str(row["שם בית עסק"])     
                else:
                    description = str(row.iloc[0]) 
                st.write(description)
                category = st.selectbox(
                    f"Category row {i}",
                    options=list(CATEGORY_RULES_HE.keys()) + ["new_category"],
                    key=f"cat_{i}"
                )

                if category == "new_category":
                    new_cat = st.text_input(f"New category name for row {i}", key=f"newcat_{i}")
                else:
                    new_cat = category
                if st.button(f"Save row {i}", key=f"save_{i}"):
                    if new_cat not in CATEGORY_RULES_HE:
                        CATEGORY_RULES_HE = loading_categories()
                    
                    new_cat = new_cat.strip().lower()
                    keyword = re.sub(r"\d+", "", description).strip().lower()

                    CATEGORY_RULES_HE.setdefault(new_cat, [])
                    
                    if keyword not in CATEGORY_RULES_HE[new_cat]:
                        CATEGORY_RULES_HE[new_cat].append(keyword)

                    save_categories(CATEGORY_RULES_HE)
                    st.success(f"Saved to {new_cat}")
    else:

        st.warning("No transaction tables detected :( ")
 



