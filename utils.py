import pandas as pd
import os
import streamlit as st

CSV_FILE = 'library_data.csv'

def load_data():
    """Load issued books data from CSV."""
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE, parse_dates=['IssueDate', 'ReturnDate'])
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")
            df = pd.DataFrame(columns=['BookID', 'Title', 'IssuedTo', 'IssueDate', 'ReturnDate'])
        
        df['ReturnDate'] = pd.to_datetime(df['ReturnDate'], errors='coerce')
        return df
    
    df = pd.DataFrame(columns=['BookID', 'Title', 'IssuedTo', 'IssueDate', 'ReturnDate'])
    df.to_csv(CSV_FILE, index=False)
    return df

def save_data(df):
    """Save the updated book records to CSV."""
    df.to_csv(CSV_FILE, index=False)

def issue_book(book_id, title, issued_to, issue_date):
    """Issue a new book, ensuring unique BookID."""
    df = load_data()
    if book_id in df['BookID'].astype(str).values:
        return False
    
    new_entry = pd.DataFrame([{
        'BookID': book_id,
        'Title': title,
        'IssuedTo': issued_to,
        'IssueDate': issue_date,
        'ReturnDate': pd.NaT
    }])
    
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    return True

def return_book(book_id, return_date):
    """Marks a book as returned and updates the CSV."""
    df = load_data()
    
    mask = df['BookID'].astype(str) == str(book_id)
    if mask.any():
        idx = df[mask].index[0]
        
        if pd.isna(df.at[idx, 'ReturnDate']):
            df.at[idx, 'ReturnDate'] = pd.to_datetime(return_date).strftime('%Y-%m-%d')
            save_data(df)
            return True
    
    return False

def get_issued_books():
    """Fetch books that are issued but not yet returned."""
    df = load_data()
    return df[(df['IssuedTo'].notna()) & (df['ReturnDate'].isna())]
