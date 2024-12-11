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
                # Append the extracted table data
                data.extend(table)
        return data

# Streamlit UI
st.title("Bank Transaction Viewer")

# Upload PDF file
uploaded_file = st.file_uploader("Upload your Bank Statement (PDF)", type="pdf")

if uploaded_file is not None:
    # Extract data from PDF
    transaction_data = extract_pdf_data(uploaded_file)
    
    # Check if any data was extracted
    if not transaction_data:
        st.error("No data found in the PDF. Please check the file format or structure.")
    else:
        # Print the extracted data for debugging (optional)
        st.write("Extracted Data:", transaction_data)
        
        # Check if we have data and headers
        headers = transaction_data[0] if transaction_data else []
        rows = transaction_data[1:] if len(transaction_data) > 1 else []
        
        # Create DataFrame if headers and rows are valid
        if headers and rows:
            df = pd.DataFrame(rows, columns=headers)
            st.dataframe(df)
        else:
            st.error("Failed to extract table data. Please check the structure of the PDF.")
    
    # Add sorting and filtering functionality
    if 'df' in locals():
        sorted_df = df.sort_values(by="Date", ascending=False)  # Example sorting by date
        st.dataframe(sorted_df)

        # Search functionality
        search_term = st.text_input("Search transactions:")
        if search_term:
            search_results = df[df['Description'].str.contains(search_term, case=False)]
            st.dataframe(search_results)
