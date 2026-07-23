import pdfplumber

import pandas as pd

pdf_path = "your\_file.pdf"

all_rows = []

# 1. Extract Raw Data

with pdfplumber.open(pdf_path) as pdf:

    for page in pdf.pages:

        # Use 'lines' strategy to detect borders, or 'text' if no borders exist

        table = page.extract_table(table_settings={

            "vertical\_strategy": "lines",

            "horizontal\_strategy": "lines",

            "snap\_tolerance": 4,

            "join\_tolerance": 4

        })

        if table:

            # Skip header row if present on every page (adjust index as needed)

            all_rows.extend(table[1:] if page == pdf.pages[0] else table)

            # 2. Convert to DataFrame

            # Replace 'None' with empty strings for easier handling

df = pd.DataFrame(all_rows).fillna('')

# 3. Define the Key Column

# This is the column that should ONLY have data on the first row of an entry

# Usually column 0 (e.g., Invoice ID, Item Code, Date)

key_col_index = 0

# 4. Create a Grouping Key

# Logic: If the key column has text, it's a NEW record (use its index).

# If it's empty, it's a continuation of the previous record.

df['group_id'] = df[key_col_index].apply(lambda x: 1 if x.strip() != '' else 0).cumsum()

# 5. Merge Rows

# Group by the generated ID and combine text columns

def combine_text(series):

# Filter out empty strings and join with a space

    return " ".join([str(x).strip() for x in series if str(x).strip() != ''])

# Apply combination to ALL columns

# For numeric columns that only appear on the first row, you might use 'first' instead

aggregated_df = df.groupby('group_id').agg(lambda x: combine_text(x)).reset_index(drop=True)

# 6. Export to Excel/CSV

aggregated_df.to_excel("cleaned\_data.xlsx", index=False)

print("Extraction complete. File saved as 'cleaned\_data.xlsx'")

'''
Key Logic Explained
•	extract_table Settings: Using "vertical_strategy": "lines" tells pdfplumber to look for actual drawn lines in the PDF. 
    If your PDF has no lines (white space only), change this to "text". 
•	cumsum() Trick: This creates a running count. Every time a row has a valid ID (e.g., "Inv-101"), the count increases 
    by 1. Rows with null IDs get the same count as the row above them. This effectively tags all split rows with the same "Group ID".
•	combine_text: This function iterates through the split rows for a specific group, ignores empty cells, and joins the 
    text with a space. This reconstructs the full description automatically.
'''