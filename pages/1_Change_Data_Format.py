import streamlit as st
import pandas as pd

# Streamlit app title
st.title("📊 Wide to Long Data Reshaper for Currency Rates")

# File uploader
uploaded_file = st.file_uploader("📥 Upload a CSV or Excel file", type=['csv', 'xlsx'])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1]
    
    # If Excel, let user pick a sheet
    if file_extension == 'xlsx':
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        sheet = st.selectbox("Select a sheet", sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=sheet)
    else:
        df = pd.read_csv(uploaded_file)

    st.subheader("📝 Original Data Preview")
    st.dataframe(df.head())

    # Check required columns exist
    required_cols = ['No.', 'CURRENCY', 'CODE']
    if all(col in df.columns for col in required_cols):
        # Convert from wide to long
        df_long = pd.melt(df, 
                          id_vars=required_cols, 
                          var_name='Month_Year', 
                          value_name='Rate')

        # Clean 'Month_Year' column: remove extra spaces, ensure space before apostrophe
        df_long['Month_Year'] = df_long['Month_Year'].str.strip()
        df_long['Month_Year'] = df_long['Month_Year'].str.replace(r"([A-Za-z]+)'", r"\1 '", regex=True)

        # Convert 'Month_Year' to datetime (auto-detect mixed formats)
        try:
            df_long['Month_Year'] = pd.to_datetime(df_long['Month_Year'], format='mixed')
        except Exception as e:
            st.error(f"Date parsing error: {e}")

        st.subheader("📊 Reshaped Data (Long Format)")
        st.dataframe(df_long.head())

        # Download button for the long format CSV
        csv = df_long.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Long Format CSV",
            data=csv,
            file_name='currency_rates_long.csv',
            mime='text/csv',
        )

    else:
        st.error(f"Uploaded file must contain these columns: {required_cols}")
