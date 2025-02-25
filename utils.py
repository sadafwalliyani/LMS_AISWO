import pandas as pd
import os
import streamlit as st

# Define persistent CSV file paths in the /workspaces directory
CSV_FILE_LIBRARY = '/workspaces/LMS_AISWO/library_data.csv'
CSV_FILE_REGISTRATION = '/workspaces/LMS_AISWO/registration_newuser.csv'

# Debug: Print CSV file paths
st.write(f"Library CSV path: {CSV_FILE_LIBRARY}")
st.write(f"Registration CSV path: {CSV_FILE_REGISTRATION}")

# Library Data Functions
def load_library_data():
    """Load issued books data from CSV."""
    if os.path.exists(CSV_FILE_LIBRARY):
        try:
            df = pd.read_csv(CSV_FILE_LIBRARY, parse_dates=['IssueDate', 'ReturnDate'])
            st.write("Library data loaded successfully!")
        except Exception as e:
            st.error(f"Error reading library CSV: {str(e)}")
            df = pd.DataFrame(columns=['BookID', 'Title', 'IssuedTo', 'IssueDate', 'ReturnDate'])
        
        df['ReturnDate'] = pd.to_datetime(df['ReturnDate'], errors='coerce')
        return df
    
    st.write("Library CSV not found. Creating a new one...")
    df = pd.DataFrame(columns=['BookID', 'Title', 'IssuedTo', 'IssueDate', 'ReturnDate'])
    df.to_csv(CSV_FILE_LIBRARY, index=False, encoding='utf-8-sig')
    return df

def save_library_data(df):
    """Save the updated book records to CSV."""
    st.write("Saving library data...")
    df.to_csv(CSV_FILE_LIBRARY, index=False, encoding='utf-8-sig')
    st.write("Library data saved successfully!")

def issue_book(book_id, title, issued_to, issue_date):
    """Issue a new book, ensuring unique BookID."""
    df = load_library_data()
    if book_id in df['BookID'].astype(str).values:
        st.error("Error: Book ID already exists!")
        return False
    
    new_entry = pd.DataFrame([{
        'BookID': book_id,
        'Title': title,
        'IssuedTo': issued_to,
        'IssueDate': issue_date,
        'ReturnDate': pd.NaT
    }])
    
    df = pd.concat([df, new_entry], ignore_index=True)
    save_library_data(df)
    return True

def return_book(book_id, return_date):
    """Marks a book as returned and updates the CSV."""
    df = load_library_data()
    
    mask = df['BookID'].astype(str) == str(book_id)
    if mask.any():
        idx = df[mask].index[0]
        
        if pd.isna(df.at[idx, 'ReturnDate']):
            df.at[idx, 'ReturnDate'] = pd.to_datetime(return_date).strftime('%Y-%m-%d')
            save_library_data(df)
            return True
    
    return False

def get_issued_books():
    """Fetch books that are issued but not yet returned."""
    df = load_library_data()
    return df[(df['IssuedTo'].notna()) & (df['ReturnDate'].isna())]

# User Registration Functions
def load_registration_data():
    """Load user registration data from CSV."""
    if os.path.exists(CSV_FILE_REGISTRATION):
        try:
            df = pd.read_csv(CSV_FILE_REGISTRATION)
            st.write("Registration data loaded successfully!")
        except Exception as e:
            st.error(f"Error reading registration CSV: {str(e)}")
            df = pd.DataFrame(columns=['Full Name', 'Class', 'Date of Birth', 'Address', 'Phone Number', 'Email'])
        return df
    
    st.write("Registration CSV not found. Creating a new one...")
    df = pd.DataFrame(columns=['Full Name', 'Class', 'Date of Birth', 'Address', 'Phone Number', 'Email'])
    df.to_csv(CSV_FILE_REGISTRATION, index=False, encoding='utf-8-sig')
    return df

def save_registration_data(df):
    """Save the updated user registration records to CSV."""
    st.write("Saving registration data...")
    df.to_csv(CSV_FILE_REGISTRATION, index=False, encoding='utf-8-sig')
    st.write("Registration data saved successfully!")

def register_user(full_name, classname, date_of_birth, address, phone_number, email):
    """Register a new user."""
    df = load_registration_data()
    new_entry = pd.DataFrame([{
        'Full Name': full_name,
        'Class': classname,
        'Date of Birth': date_of_birth,
        'Address': address,
        'Phone Number': phone_number,
        'Email': email
    }])
    
    df = pd.concat([df, new_entry], ignore_index=True)
    save_registration_data(df)
    return True
