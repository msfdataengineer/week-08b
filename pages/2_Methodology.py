import streamlit as st
import pandas as pd
from graphviz import Digraph

# region <--------- Page Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="Methodology"
)
# endregion

st.title("Methodology 🛠️")

st.markdown("""
This page explains the **data flows and implementation details** of the HDB Explorer app.
It covers the two main use cases:
1. Chat with Information
2. Intelligent Search
""")

# ----------------------
# Flowchart for Chat with Information
# ----------------------
st.subheader("Use Case 1: Chat with Information")
dot_chat = Digraph()
dot_chat.node("A", "User Input Query")
dot_chat.node("B", "Streamlit App Form Submission")
dot_chat.node("C", "Process User Message")
dot_chat.node("D", "Identify Relevant Flat Types\n(from HDB Dataset)")
dot_chat.node("E", "Fetch Flat Details")
dot_chat.node("F", "Generate AI Response\n(OpenAI)")
dot_chat.node("G", "Display Response + Flat Details Table")

dot_chat.edges(["AB", "BC", "CD", "DE", "EF", "FG"])
st.graphviz_chart(dot_chat)

st.markdown("""
**Explanation:**
- User submits a natural language query about HDB flats.
- The app identifies relevant flat types using the dataset.
- Details are fetched and AI generates a user-friendly response.
- Response and flat details are displayed as a table.
""")

# ----------------------
# Flowchart for Intelligent Search
# ----------------------
st.subheader("Use Case 2: Intelligent Search")
dot_search = Digraph()
dot_search.node("A", "User Selects Filters")
dot_search.node("B", "Streamlit App Form Submission")
dot_search.node("C", "Apply Filter Criteria on HDB Dataset")
dot_search.node("D", "Return Matching Flat Details")
dot_search.node("E", "Display Results Table")
dot_search.node("F", "Optional: Map Visualization")

dot_search.edges(["AB", "BC", "CD", "DE", "EF"])
st.graphviz_chart(dot_search)

st.markdown("""
**Explanation:**
- User selects structured filters (flat type, planning area, etc.).
- App applies filter logic on HDB dataset.
- Matching flats are displayed as a table.
- Optionally, map visualization shows flat locations.
""")

# ----------------------
# Display HDB Dataset as Table
# ----------------------
st.subheader("Full HDB Dataset Used in the App")
HDB_URL = "https://raw.githubusercontent.com/BlueSkyLT/siteselect_sg/refs/heads/main/dataset/hdb.csv"
try:
    df_hdb = pd.read_csv(HDB_URL)
    st.dataframe(df_hdb)
except Exception as e:
    st.error(f"Error loading HDB dataset: {e}")

st.markdown("""
**Notes:**
- The dataset includes flat type, block number, street, year completed, total units, and planning area.
- This table demonstrates the raw data that powers the app.
""")
