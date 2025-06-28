# app.py

import streamlit as st
from utils import extract_text_from_pdf, get_text_by_page
import os
import re


# ------------------------ Streamlit Setup ------------------------
st.set_page_config(page_title="📄 PDF Report Analyzer", layout="centered")
st.markdown(
    """
    <h1 style='text-align: center; margin-top: -80px; color: #FF073A; text-shadow: 0 0 2px #FFD700, 0 0 4px #FFD700, 0 0 8px #FFD700;'>
        📄&nbsp;&nbsp;&nbsp;&nbsp;PDF Report&nbsp;&nbsp;Analyzer
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='text-align: center;
        color: #00BFFF;'>
        <h4>Instructions : Upload a PDF and ask questions like:</h4>
        <h5>What is on page 2?</h5>
        <h5>Find TypeScript</h5>
        <h5>Find Mentor or Find Author</h5>
        <h5>Page 3</h5>
        <br>
        <h5><em>🔍 Search query depends on the material inside the document body</em></h5>
    </div>
    """,
    unsafe_allow_html=True
)



# ------------------------ Upload New PDF File ------------------------

st.markdown(
    """
    <h4 style='text-align: left;
            color: #FF073A;
            font-size: 26px;
            text-shadow: 0 0 2px #FFD700;'>
        📤 Upload a new PDF file from your computer:
    </h4>
    """,
    unsafe_allow_html=True
)


uploaded_file = st.file_uploader("📤", type=["pdf"])

if uploaded_file:
    file_path = os.path.join("uploads", uploaded_file.name)
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"✅ File saved to: `{file_path}`")

    with st.spinner("Reading PDF..."):
        full_text, total_pages = extract_text_from_pdf(file_path)

    st.success(f"PDF loaded with {total_pages} pages.")

    # ------------------------ Search Input ------------------------
    st.markdown(
    """
    <h4 style='text-align: left;
            color: #00BFFF;
            font-size: 26px;
            text-shadow: 0 0 2px #FFD700;'>
        🔍 Ask a question about the uploaded PDF:
    </h4>
    """,
    unsafe_allow_html=True
)

    query = st.text_input(" 🔍 ")

    if query:
        if "page" in query.lower():
            match = re.search(r"page\s*(\d+)", query.lower())
            if match:
                page_num = int(match.group(1))
                result = get_text_by_page(file_path, page_num)

                st.markdown(
    f"""
    <h3 style="
        color: #FF073A;
        text-shadow: 0 0 0px #FFDB58, 0 0 1px #FFDB58, 0 0 2px #FFDB58;
        font-weight: bold;
        ">
        📄 Page {page_num} Content
    </h3>
    """,
    unsafe_allow_html=True
)

                st.markdown(
    f"""
    <div style="
        font-size: 24px;
        font-weight: normal;
        color: #FF073A !important;
        text-shadow: 0 0 2px #FF073A, 0 0 4px #FF073A, 0 0 6px #FF073A;
        padding: 10px;
    ">
        ❄️ {result if result else "❌ Page not found or empty."}
    </div>
    """,
    unsafe_allow_html=True
)

            else:
                st.warning("Please specify a valid page number like 'page 2'.")
        else:
            matches = [line for line in full_text.split('\n') if query.lower() in line.lower()]

            st.markdown(
    f"""
    <div style='text-align: left;'>
        <span style="
            font-size: 30px;
            color: #FFDB58;
            font-weight: bold;
            text-shadow: 0 0 3px #FF073A, 0 0 6px #FF073A;
        ">
            🔎 Matches for '{query}'
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

            if matches:
                for match in matches:
                    st.markdown(
                        f"<p style='font-size: 30px; color: #39FF14;'>{match}</p>",
                        unsafe_allow_html=True
                    )
            else:
                st.info("No matching results found.")

# ------------------------ OPTIONAL: Select from Saved Files ------------------------

st.markdown("---")  # Horizontal line separator

# 📁 Ensure the uploads/ directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 📄 List all existing PDFs in uploads folder
saved_pdfs = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]

st.markdown(
    """
    <h4 style='text-align: left;
            color: #FF073A;
            font-size: 26px;
            text-shadow: 0 0 2px #FFD700;'>
        📂 Or select a saved PDF file from folder below:
    </h4>
    """,
    unsafe_allow_html=True
)

# 📂 Let user choose from previously uploaded PDFs
selected_pdf = st.selectbox("📄", ["Select file if it is saved !"] + saved_pdfs)

if selected_pdf != "Select file if it is saved !":
    selected_file_path = os.path.join(UPLOAD_DIR, selected_pdf)
    st.success(f"📄 Selected PDF: {selected_pdf}")

    # 📖 Extract text and count pages
    with st.spinner("Reading PDF..."):
        full_text, total_pages = extract_text_from_pdf(selected_file_path)

    st.success(f"PDF loaded with {total_pages} pages.")

    st.markdown(
    """
    <h4 style='text-align: left;
            color: #00BFFF;
            font-size: 26px;
            text-shadow: 0 0 2px #FFD700;'>
        🔍 Ask a question about the saved PDF:
    </h4>
    """,
    unsafe_allow_html=True
)

    # 🔍 Input field for search query (from selected file)
    query = st.text_input("🔍")

    if query:
        if "page" in query.lower():
            match = re.search(r"page\s*(\d+)", query.lower())
            if match:
                page_num = int(match.group(1))
                result = get_text_by_page(selected_file_path, page_num)

                st.markdown(
    f"""
    <h3 style="
        color: #FF073A;
        text-shadow: 0 0 0px #FFDB58, 0 0 1px #FFDB58, 0 0 2px #FFDB58;
        font-weight: bold;
        ">
        📄 Page {page_num} Content
    </h3>
    """,
    unsafe_allow_html=True
)

                st.markdown(
    f"""
    <div style="
        font-size: 24px;
        font-weight: normal;
        color: #FF073A !important;
        text-shadow: 0 0 2px #FF073A, 0 0 4px #FF073A, 0 0 6px #FF073A;
        padding: 10px;
    ">
        ❄️ {result if result else "❌ Page not found or empty."}
    </div>
    """,
    unsafe_allow_html=True
)

            else:
                st.warning("Please specify a valid page number like 'page 2'.")
        else:
            matches = [line for line in full_text.split('\n') if query.lower() in line.lower()]

            st.markdown(
    f"""
    <div style='text-align: left;'>
        <span style="
            font-size: 30px;
            color: #FFDB58;
            font-weight: bold;
            text-shadow: 0 0 5px #FF073A, 0 0 10px #FF073A;
        ">
            🔎 Matches for '{query}'
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

            if matches:
                for match in matches:
                    st.markdown(
                        f"<p style='font-size: 30px; color: #39FF14;'>{match}</p>",
                        unsafe_allow_html=True
                    )
            else:
                st.info("No matching results found.")

# ------------------------ 🔚 Always-Visible Footer ------------------------
st.markdown(
    """
    <hr>
    <div style='text-align: center; font-size: 18px; color: #00FF7F;'>
        👨‍🏫 <strong>Mentor:</strong> <span style='color: #FFD700;'>Ameen Alam</span> <br>
        🧑‍💻 <strong>Author:</strong> <span style='color: #1E90FF;'>Azmat Ali</span>
    </div>
    """,
    unsafe_allow_html=True
)


# 90 , 197