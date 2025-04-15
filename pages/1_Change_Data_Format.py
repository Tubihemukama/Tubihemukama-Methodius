import streamlit as st
import pandas as pd

# Streamlit app title
st.title("📊 Wide to Long Data Reshaper for Currency Rates")

# File uploader
uploaded_file = st.file_uploader("📥 Upload a CSV or Excel file", type=['csv', 'xlsx'])

# Cached function to load data
@st.cache_data
def load_data(uploaded_file, sheet=None):
    if uploaded_file.name.endswith('.xlsx'):
        return pd.read_excel(uploaded_file, sheet_name=sheet)
    else:
        return pd.read_csv(uploaded_file)

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1]
    st.write(f"📄 Uploaded file: `{uploaded_file.name}` ({file_extension.upper()})")

    # If Excel, let user pick a sheet
    if file_extension == 'xlsx':
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        sheet = st.selectbox("Select a sheet", sheet_names)
        df = load_data(uploaded_file, sheet)
    else:
        df = load_data(uploaded_file)

    st.subheader("📝 Original Data Preview")
    st.dataframe(df.head())

    # Check required columns exist
    required_cols = ['No.', 'CURRENCY', 'CODE']
    if all(col in df.columns for col in required_cols):
        # Convert from wide to long
        df_long = pd.melt(
            df,
            id_vars=required_cols,
            var_name='Month_Year',
            value_name='Rate'
        )

        # Clean 'Month_Year' column
        df_long['Month_Year'] = df_long['Month_Year'].astype(str).str.strip()
        df_long['Month_Year'] = df_long['Month_Year'].str.replace(r"([A-Za-z]+)'", r"\1 '", regex=True)

        # Convert 'Month_Year' to datetime safely
        df_long['Month_Year'] = pd.to_datetime(df_long['Month_Year'], errors='coerce')

        # Warn if any date parsing issues
        if df_long['Month_Year'].isnull().any():
            st.warning("⚠️ Some dates could not be parsed and are set as NaT.")

        # Rename columns
        df_long.rename(
            columns={
                'No.': 'ID',
                'CODE': 'CURRENCY CODE',
                'Month_Year': 'date'
            },
            inplace=True
        )

        st.subheader("📊 Reshaped Data (Long Format)")
        st.dataframe(df_long.head())

        # Optional: Show full data
        if st.checkbox("Show all reshaped data"):
            st.dataframe(df_long)

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
