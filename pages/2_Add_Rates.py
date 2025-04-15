import streamlit as st
import pandas as pd

st.title("Match Exchange Rates to Either Import or Exchange Data")

st.write("""
⚠️ **Do not miss these columns in both datasets**  
- **Currency code**  
- **Rate**  
- **Date (mm/dd/yyy**
""")

# Upload dataset 1
dataset1_file = st.file_uploader("**Upload Exchange Rates**", type=["csv", "xlsx"])
# Upload dataset 2
dataset2_file = st.file_uploader("**Upload Either Import or Export Dataset**", type=["csv", "xlsx"])

df1 = None
df2 = None

# Process dataset 1
if dataset1_file:
    if dataset1_file.name.endswith('.csv'):
        df1 = pd.read_csv(dataset1_file)
    else:
        xls1 = pd.ExcelFile(dataset1_file)
        sheet1_name = st.selectbox("Select sheet for Exchange Rates", xls1.sheet_names, key="sheet1")
        df1 = pd.read_excel(xls1, sheet_name=sheet1_name)

# Process dataset 2
if dataset2_file:
    if dataset2_file.name.endswith('.csv'):
        df2 = pd.read_csv(dataset2_file)
    else:
        xls2 = pd.ExcelFile(dataset2_file)
        sheet2_name = st.selectbox("Select sheet for Dataset 2", xls2.sheet_names, key="sheet2")
        df2 = pd.read_excel(xls2, sheet_name=sheet2_name)

# When both datasets are loaded
if df1 is not None and df2 is not None:
    # Standardize column names to lowercase
    df1.columns = df1.columns.str.lower()
    df2.columns = df2.columns.str.lower()

    # Convert 'date' columns to datetime, then format as mm/dd/yyyy
    df1['date'] = pd.to_datetime(df1['date'], errors='coerce').dt.strftime('%m/%d/%Y')
    df2['date'] = pd.to_datetime(df2['date'], errors='coerce').dt.strftime('%m/%d/%Y')

    st.subheader("Exchange rates Preview")
    st.write(df1.head())

    st.subheader("Dataset 2 Preview")
    st.write(df2.head())

    # Merge datasets on 'currency code' and 'date'
    merged_df = pd.merge(df2, df1[['rate', 'currency code', 'date']], on=['currency code', 'date'], how='left')

    st.subheader("✅Merged Data with Rate")
    st.write(merged_df)

    # Option to download result
    csv = merged_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Merged Data as CSV",
        data=csv,
        file_name='merged_data.csv',
        mime='text/csv'
    )
