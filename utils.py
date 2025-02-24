import pandas as pd
import os

# ✅ Update this path with your actual Google Drive path
GOOGLE_DRIVE_PATH = "https://drive.google.com/drive/folders/15VB3zFFaOHG0ii4h81qlEdFyi_xaQMGK?usp=drive_link"  

CSV_FILE_LIBRARY = os.path.join(GOOGLE_DRIVE_PATH, "library_data.csv")
CSV_FILE_REGISTRATION = os.path.join(GOOGLE_DRIVE_PATH, "registration_newuser.csv")

# Ensure the directory exists
if not os.path.exists(GOOGLE_DRIVE_PATH):
    os.makedirs(GOOGLE_DRIVE_PATH, exist_ok=True)

# 📌 Load Library Data
def load_library_data():
    """Load issued books data from Google Drive CSV."""
    if os.path.exists(CSV_FILE_LIBRARY):
        try:
            return pd.read_csv(CSV_FILE_LIBRARY, parse_dates=['IssueDate', 'ReturnDate'])
        except Exception as e:
            print(f"❌ Error reading library CSV: {str(e)}")
    return pd.DataFrame(columns=['BookID', 'Title', 'IssuedTo', 'IssueDate', 'ReturnDate'])

# 📌 Save Library Data
def save_library_data(df):
    """Save the updated book records to Google Drive CSV."""
    try:
        df.to_csv(CSV_FILE_LIBRARY, index=False, encoding="utf-8-sig")
    except Exception as e:
        print(f"❌ Error saving library data: {str(e)}")

# 📌 Issue a Book
def issue_book(book_id, title, issued_to, issue_date):
    """Issue a new book, ensuring unique BookID."""
    df = load_library_data()
    if book_id in df['BookID'].astype(str).values:
        print("⚠️ Error: Book ID already exists!")
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
