import sys
import os
import importlib
import pandas as pd
import streamlit as st

# Ensure `utils.py` is correctly imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import utils
importlib.reload(utils)  # Force reload the module

from utils import issue_book, register_user, return_book, get_issued_books

# Page configuration
st.set_page_config(page_title="AISWO LIBRARY MANAGEMENT SYSTEM", layout="wide")

# Sidebar Navigation
with st.sidebar:
    st.image("Logo.png", width=150)
    st.title("AISWO LIBRARY MANAGEMENT SYSTEM")
    page = st.radio("Go to", ["Home", "Issue Book", "Registration"], key="nav_radio")

# 📌 Home Page - Display Issued Books
if page == "Home":
    st.title("📚 Currently Issued Books")

    issued_books = get_issued_books()

    if not issued_books.empty:
        st.write("Here are the books currently issued:")
        for index, row in issued_books.iterrows():
            book_id = row['BookID']
            with st.container():
                cols = st.columns([1, 3, 2, 2, 2])
                cols[0].write(f"**ID:** {book_id}")
                cols[1].write(f"**Title:** {row['Title']}")
                cols[2].write(f"**Issued To:** {row['IssuedTo']}")

                issued_date = pd.to_datetime(row['IssueDate'], errors='coerce')
                cols[3].write(f"**Issued On:** {issued_date.date() if pd.notna(issued_date) else 'N/A'}")

                with cols[4]:
                    if st.button("Return ⏎", key=f"ret_{book_id}_{index}"):
                        return_date = pd.to_datetime("today").date()
                        
                        if return_book(book_id, return_date):
                            st.success(f"Book {book_id} returned!")
                            st.rerun()
    else:
        st.write("No books are currently issued.")

# 📌 Issue Book Page
elif page == "Issue Book":
    st.title("📖 Issue New Book")

    with st.form("issue_form"):
        book_id = st.text_input("Book ID", key="book_id")
        title = st.text_input("Title", key="title")
        issued_to = st.text_input("Issued To", key="issued_to")
        issue_date = st.date_input("Issue Date", key="issue_date")

        if st.form_submit_button("Issue Book"):
            if issue_book(book_id, title, issued_to, issue_date):
                st.success("✅ Book issued successfully!")
            else:
                st.error("⚠ Error: Book ID already exists!")

# 📌 Registration
elif page == "Registration":
    st.title("📝 Register New User")
    with st.form("reg_form"):  
        full_name = st.text_input("Full Name", key="full_name")
        classname = st.text_input("Class", key="classname")
        date_of_birth = st.date_input("Date of Birth", key="date_of_birth")
        address = st.text_input("Address", key="address")
        phone_number = st.text_input("Phone Number", key="phone_number")
        email = st.text_input("Email Address", key="email")

        if st.form_submit_button("Register"):
            if register_user(full_name, classname, date_of_birth, address, phone_number, email):
                st.success("✅ User registered successfully!")
            else:
                st.error("⚠ Error: User already exists!")
