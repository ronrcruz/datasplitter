import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os

# Function to select the excel file
def select_file():
    root.filename = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("Excel files", "*.xlsx"), ("all files", "*.*")))
    file_label.config(text=root.filename)
    root.output_filename = os.path.splitext(root.filename)[0] + "(split).xlsx"
    output_file_label.config(text=root.output_filename)

# Function to select the output file
def select_output_file():
    root.output_filename = filedialog.asksaveasfilename(initialdir = "/", title = "Save as", filetypes = (("Excel files", "*.xlsx"), ("all files", "*.*")), defaultextension=".xlsx")
    output_file_label.config(text=root.output_filename)

# Function to split the data
def split_data():
    df = pd.read_excel(root.filename)
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

    df.to_excel(root.output_filename, index=False)

    
# Create the GUI window
root = tk.Tk()
root.title("Data Splitter")

# Create the file selection button
file_button = tk.Button(root, text="Select File", command=select_file)
file_button.pack()

# Create the label to display the selected file name
file_label = tk.Label(root, text="")
file_label.pack()

# Create the output file selection button
output_file_button = tk.Button(root, text="Select Output File", command=select_output_file)
output_file_button.pack()

# Create the label to display the selected output file name
output_file_label = tk.Label(root, text="")
output_file_label.pack()

# Create the split button
split_button = tk.Button(root, text="Split Data", command=split_data)
split_button.pack()

# Start the GUI event loop
root.mainloop()
