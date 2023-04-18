import streamlit as st
import streamlit_pandas as sp
import os
import base64

pd = sp.pd

# Function to split the data
def split_data(file):
    df = pd.read_excel(file)
    col = df["itemdescription"]
    new_cols = col.str.split("/", expand=True)
    new_cols.rename(columns={0: "manufacturer", 1: "model", 2: "model number", 3: "storage capacity", 4: "color", 5: "carrier", 6: "network lock status", 7: "grade"}, inplace=True)
    df = pd.concat([df, new_cols], axis=1)

    # Remove columns with duplicate names
    df = df.loc[:, ~df.columns.duplicated()]

    # Add new columns with their respective values
    df["QUANTITY"] = 1
    df["UOM"] = "Units"
    df["TAX"] = ""

    # Rearrange columns in the desired order
    df = df[["itemdescription", "QUANTITY", "UOM", "itemdescription", "Unit_Selling_Price", "TAX", "manufacturer", "model", "carrier", "type", "trackingnumber", "grade", "lpn", "model number", "storage capacity", "color", "network lock status", "itemnbr", "serialnumber", "Warehouse", "ordernbr"]]
    
    # Rename columns as needed
    df.columns = ["PRODUCT", "QUANTITY", "UOM", "DESCRIPTION", "PRICE", "TAX", "manufacturer", "model", "carrier", "type", "trackingnumber", "grade", "lpn", "model number", "storage capacity", "color", "network lock status", "itemnbr", "serialnumber", "Warehouse", "ordernbr"]

    return df

def get_table_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download the output file</a>'
    return href

# Streamlit App
st.title("Data Splitter")

uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "xls"])

if uploaded_file is not None:
    st.write("Selected file:")
    st.write(uploaded_file.name)
    output_filename = os.path.splitext(uploaded_file.name)[0] + "(split).csv"

    if st.button("Split Data"):
        df = split_data(uploaded_file)
        st.write(df.head())
        st.markdown(get_table_download_link(df, output_filename), unsafe_allow_html=True)
else:
    st.write("No file selected.")

