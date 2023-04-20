import streamlit as st
import streamlit_pandas as sp
import os
import base64
import io

pd = sp.pd

# Function to split the data
def split_data(file):
    df = pd.read_excel(file)
    col = df["itemdescription"]
    warehouse_value = df.loc[0, "Warehouse"]
    
    # Replace '.' with '/' to handle both cases
    col = col.str.replace(".", "/", regex=False)
    
    if warehouse_value == "TX1":
        st.write("Warehouse TX1 Recognized, creating template...")
        new_cols = col.str.split("/", expand=True)
        new_cols.rename(columns={0: "manufacturer", 1: "model", 2: "model number", 3: "storage capacity", 4: "color", 5: "carrier", 6: "network lock status", 7: "grade"}, inplace=True)

    elif warehouse_value == "APPLE AS IS":
        st.write("Warehouse APPLE AS IS Recognized, creating template...")
        new_cols = col.str.split("/", expand=True)
        new_cols.rename(columns={0: "manufacturer", 1: "model", 2: "model number", 3: "storage capacity", 4: "color", 5: "carrier", 6: "grade"}, inplace=True)
        new_cols['network lock status'] = new_cols['carrier']

    elif warehouse_value == "SAMSUNG":
        st.write("Warehouse SAMSUNG Recognized, creating template...")
        new_cols = col.str.split("/", expand=True)
        new_cols.rename(columns={0: "manufacturer", 1: "model", 2: "model number", 3: "storage capacity", 4: "color", 5: "carrier", 6: "grade"}, inplace=True)
        new_cols['network lock status'] = new_cols['carrier']
    
    elif warehouse_value == "TARGET":
        st.write("Warehouse TARGET Recognized, creating template...")
        new_cols = col.str.split("/", expand=True)
        new_cols.rename(columns={0: "manufacturer", 1: "model", 2: "model number", 3: "storage capacity", 4: "color", 5: "grade"}, inplace=True)
        new_cols['network lock status'] = " "
        new_cols['carrier'] = " "
      
    elif warehouse_value == "W03-ATT":
        st.write("Warehouse W03-ATT Recognized, creating template...")
        new_cols = col.str.split("/", expand=True)
        new_cols.rename(columns={0: "manufacturer", 1: "model", 2: "model number", 3: "storage capacity", 4: "color", 5: "carrier", 6: "grade"}, inplace=True)
        new_cols['network lock status'] = new_cols['carrier']
      
    elif warehouse_value == "W07-USCC":
        st.write("Warehouse W07-USCC Recognized, creating template...")
        new_cols = col.str.split("/", expand=True)
        new_cols.rename(columns={0: "manufacturer", 1: "model", 2: "model number", 3: "storage capacity", 4: "color", 5: "carrier", 6: "grade"}, inplace=True)
        new_cols['network lock status'] = new_cols['carrier']
    
    elif warehouse_value == "W08-GGL":
        st.write("Warehouse W08-GGL Recognized, creating template...")
        new_cols = col.str.split("/", expand=True)
        new_cols.rename(columns={0: "manufacturer", 1: "model", 2: "model number", 3: "storage capacity", 4: "color", 5: "carrier", 6: "grade"}, inplace=True)
        new_cols['network lock status'] = new_cols['carrier']
    else:
        st.write("Warehouse not recognized, creating template...")
        new_cols = col.str.split("/", expand=True)
        new_cols.rename(columns={0: "manufacturer", 1: "model", 2: "model number", 3: "storage capacity", 4: "color", 5: "carrier", 6: "network lock status", 7: "grade"}, inplace=True)

    # Concatenate the new columns with the original dataframe
    df = pd.concat([df, new_cols], axis=1)

    # Remove columns with duplicate names
    df = df.loc[:, ~df.columns.duplicated()]

    # Add new columns with their respective values
    df["QUANTITY"] = 1
    df["UOM"] = "Units"
    df["TAX"] = "0"

    # Rearrange columns in the desired order
    df = df[["itemdescription", "QUANTITY", "UOM", "itemdescription", "Unit_Selling_Price", "TAX", "manufacturer", "model", "carrier", "type", "trackingnumber", "grade", "lpn", "model number", "storage capacity", "color", "network lock status", "itemnbr", "serialnumber", "Warehouse", "ordernbr"]]
    
    # Rename columns as needed
    df.columns = ["PRODUCT", "QUANTITY", "UOM", "DESCRIPTION", "PRICE", "TAX", "manufacturer", "model", "carrier", "type", "trackingnumber", "grade", "lpn", "model number", "storage capacity", "color", "network lock status", "itemnbr", "serialnumber", "Warehouse", "ordernbr"]

    replacements = {
        "APPL": "Apple",
        "SAMS": "Samsung",
        "UNL": "Unlocked",
        "GGL": "Google",
    }

    columns_to_replace = [
        "PRODUCT",
        "DESCRIPTION",
        "manufacturer",
        "carrier",
        "network lock status",
    ]

    for col_name in columns_to_replace:
        df[col_name] = df[col_name].replace(replacements, regex=True)

    return df

def get_table_download_link(df, filename):
    excel_file = io.BytesIO()
    writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="Sheet1")
    writer.save()
    excel_file.seek(0)
    b64 = base64.b64encode(excel_file.read()).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'

# Streamlit App
st.title("Data Splitter")

uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "xls"])

if uploaded_file is not None:
    st.write("Selected file:")
    st.write(uploaded_file.name)
    output_filename = os.path.splitext(uploaded_file.name)[0] + "(split).xlsx"

    if st.button("Split Data"):
        df = split_data(uploaded_file)
        st.write(df.head())
        st.markdown(get_table_download_link(df, output_filename), unsafe_allow_html=True)
else:
    st.write("No file selected.")
