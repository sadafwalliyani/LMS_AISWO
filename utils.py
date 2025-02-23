import pandas as pd
import os
import streamlit as st

# Define a writable storage location
CSV_DIR = "./data"
CSV_FILE_LIBRARY = os.path.join(CSV_DIR, "library_data.csv")
CSV_FILE_REGISTRATION = os.path.join(CSV_DIR, "registration_newuser.csv")

# Ensure the directory exists
if not os.path.exists(CSV_DIR):
    try:
        os.makedirs(CSV_DIR, exist_ok=True)
    except PermissionError:
        CSV_FILE_LIBRARY = os.path.join("/tmp", "library_data.csv")
        CSV_FILE_REGISTRATION = os.path.join("/tmp", "registration_newuser.csv")

# 📌 Load Library Data
def load_library_data():
    """Load issued books data from CSV."""
    if os.path.exists(CSV_FILE_LIBRARY):
        try:
            df = pd.read_csv(CSV_FILE_LIBRARY, parse_dates=['IssueDate', 'ReturnDate'])
        except Exception as e:
            st.error(f"❌ Error reading library CSV: {str(e)}")
            df = pd.DataFrame(columns=['BookID', 'Title', 'IssuedTo', 'IssueDate', 'ReturnDate'])
    else:
        df = pd.DataFrame(columns=['BookID', 'Title', 'IssuedTo', 'IssueDate', 'ReturnDate'])
        save_library_data(df)

    df['ReturnDate'] = pd.to_datetime(df['ReturnDate'], errors='coerce')
    return df

# 📌 Save Library Data
def save_library_data(df):
    """Save the updated book records to CSV."""
    try:
        df.to_csv(CSV_FILE_LIBRARY, index=False, encoding="utf-8-sig")
    except Exception as e:
        st.error(f"❌ Error saving library data: {str(e)}")

# 📌 Issue a Book
def issue_book(book_id, title, issued_to, issue_date):
    """Issue a new book, ensuring unique BookID."""
    df = load_library_data()
    if book_id in df['BookID'].astype(str).values:
        st.error("⚠️ Error: Book ID already exists!")
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

# 📌 Return a Book
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

# 📌 Get Issued Books
def get_issued_books():
    """Fetch books that are issued but not yet returned."""
    df = load_library_data()
    return df[(df['IssuedTo'].notna()) & (df['ReturnDate'].isna())]

# 📌 Load Registration Data
def load_registration_data():
    """Load user registration data from CSV."""
    if os.path.exists(CSV_FILE_REGISTRATION):
        try:
            df = pd.read_csv(CSV_FILE_REGISTRATION)
        except Exception as e:
            st.error(f"❌ Error reading registration CSV: {str(e)}")
            df = pd.DataFrame(columns=['Full Name', 'Class', 'Date of Birth', 'Address', 'Phone Number', 'Email'])
    else:
        df = pd.DataFrame(columns=['Full Name', 'Class', 'Date of Birth', 'Address', 'Phone Number', 'Email'])
        save_registration_data(df)
    
    return df

# 📌 Save Registration Data
def save_registration_data(df):
    """Save the updated user registration records to CSV."""
    try:
        df.to_csv(CSV_FILE_REGISTRATION, index=False, encoding="utf-8-sig")
    except Exception as e:
        st.error(f"❌ Error saving registration data: {str(e)}")

# 📌 Register User
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
