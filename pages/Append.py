import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Append Data Sets")

def load_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file), None
    elif file.name.endswith(('.xls', '.xlsx')):
        xls = pd.ExcelFile(file)
        return None, xls
    else:
        st.error("Unsupported file type!")
        return None, None

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

st.header("Upload Your Datasets")

file1 = st.file_uploader("Upload First Dataset (CSV or Excel)", type=["csv", "xls", "xlsx"], key="file1")
file2 = st.file_uploader("Upload Second Dataset (CSV or Excel)", type=["csv", "xls", "xlsx"], key="file2")

df1, df2 = None, None

if file1:
    csv_df1, xls1 = load_file(file1)
    if xls1:
        sheet1 = st.selectbox(f"Select sheet for {file1.name}", xls1.sheet_names, key="sheet1")
        df1 = xls1.parse(sheet1)
    elif csv_df1 is not None:
        df1 = csv_df1

    st.subheader(f"📄 Preview of {file1.name}")
    show_all_1 = st.checkbox("Show all rows for first dataset", key="show_all_1")
    st.dataframe(df1 if show_all_1 else df1.head())

if file2:
    csv_df2, xls2 = load_file(file2)
    if xls2:
        sheet2 = st.selectbox(f"Select sheet for {file2.name}", xls2.sheet_names, key="sheet2")
        df2 = xls2.parse(sheet2)
    elif csv_df2 is not None:
        df2 = csv_df2

    st.subheader(f"📄 Preview of {file2.name}")
    show_all_2 = st.checkbox("Show all rows for second dataset", key="show_all_2")
    st.dataframe(df2 if show_all_2 else df2.head())

if df1 is not None and df2 is not None:
    if list(df1.columns) == list(df2.columns):
        combined_df = pd.concat([df1, df2], ignore_index=True)
        st.success("✅ Datasets successfully combined!")

        st.subheader("📊 Preview of Combined Dataset")
        show_all_combined = st.checkbox("Show all rows for combined dataset", key="show_all_combined")
        st.dataframe(combined_df if show_all_combined else combined_df.head())

        csv_data = convert_df(combined_df)

        st.download_button(
            label="📥 Download Combined CSV",
            data=csv_data,
            file_name='combined_dataset.csv',
            mime='text/csv',
        )
    else:
        st.error("❌ The two datasets do not have the same column names. Please upload matching datasets.")
else:
    st.info("📂 Please upload both datasets to proceed.")
