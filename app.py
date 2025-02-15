import pandas as pd
import streamlit as st
from utils import load_data, issue_book, return_book, get_issued_books

# Page configuration
st.set_page_config(page_title="AISWO LIBRARY MANAGEMENT SYSTEM", layout="wide")

# Custom CSS for Styling
st.markdown("""
<style>
.sidebar .sidebar-content {background-color: #079da4; color: white;}
h1, h2, h3, h4, h5, h6 {color: #079da4;}
.stButton button {background-color: #079da4; color: white; border-radius: 5px;}
.stButton button:hover {background-color: #057a7f;}
.stRadio label {color: blue !important;}
</style>""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.image("logo.png", width=150)
    st.title("AISWO LIBRARY MANAGEMENT SYSTEM")
    page = st.radio("Go to", ["Home", "Issue Book"], key="nav_radio")

# 📌 Home Page - Display Issued Books
if page == "Home":
    st.title("📚 Currently Issued Books")

    # Fetch the latest issued books data
    issued_books = get_issued_books()

    if not issued_books.empty:
        for index, row in issued_books.iterrows():
            book_id = row['BookID']
            with st.container():
                cols = st.columns([1, 3, 2, 2, 2])
                cols[0].write(f"**ID:** {book_id}")
                cols[1].write(f"**Title:** {row['Title']}")
                cols[2].write(f"**Issued To:** {row['IssuedTo']}")

                # Convert IssueDate to datetime for display
                issued_date = pd.to_datetime(row['IssueDate'], errors='coerce')
                cols[3].write(f"**Issued On:** {issued_date.date() if pd.notna(issued_date) else 'N/A'}")

                # Return Book Button
                with cols[4]:
                    if st.button("Return ⏎", key=f"ret_{book_id}_{index}"):
                        return_date = pd.to_datetime("today").date()
                        
                        if return_book(book_id, return_date):
                            st.success(f"Book {book_id} returned!")
                            st.rerun()  # 🔄 Immediately refresh UI after return
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
