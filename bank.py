import streamlit as st
import pandas as pd
import pdfplumber

# Function to extract text from PDF
def extract_pdf_data(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        pages = pdf.pages
        data = []
        for page in pages:
            table = page.extract_table()
            if table:
                data.extend(table)
        return data

# Streamlit UI
st.title("Bank Transaction Viewer")

# Upload PDF file
uploaded_file = st.file_uploader("Upload your Bank Statement (PDF)", type="pdf")

if uploaded_file is not None:
    # Extract data from PDF
    transaction_data = extract_pdf_data(uploaded_file)
    
    # Convert extracted data into a pandas DataFrame
    df = pd.DataFrame(transaction_data[1:], columns=transaction_data[0])
    
    # Display the transaction data in a table
    st.dataframe(df)
    
    # Add sorting and filtering functionality
    sorted_df = df.sort_values(by="Date", ascending=False)  # Sort by date as an example
    st.dataframe(sorted_df)
    
    # Search functionality
    search_term = st.text_input("Search transactions:")
    if search_term:
        search_results = df[df['Description'].str.contains(search_term, case=False)]
        st.dataframe(search_results)
