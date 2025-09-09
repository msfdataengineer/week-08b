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
HDB_URL = "https://s3.ap-southeast-1.amazonaws.com/table-downloads-ingest.data.gov.sg/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/6f8109f7bce05c219b3825a999cc7f3a02cbc19fe536138a5eaf86bfe6d8711f.csv?AWSAccessKeyId=ASIAU7LWPY2WEO6Y4UQJ&Expires=1757427608&Signature=9vpQC%2FWfA9CtLiV2SGYlvfI%2FM3c%3D&X-Amzn-Trace-Id=Root%3D1-68c02988-7562c8fc3780214f0f91fbc1%3BParent%3D5261c04c148c5b61%3BSampled%3D0%3BLineage%3D1%3A9e07a47d%3A0&response-content-disposition=attachment%3B%20filename%3D%22ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv%22&x-amz-security-token=IQoJb3JpZ2luX2VjEG0aDmFwLXNvdXRoZWFzdC0xIkYwRAIgfkcUHQm1W2qxTP2GixiViAY4IDh5RiwQCoKalN27eVcCIBUUoVQqDS5vBwHGnxnImThNoG15x%2FusbUWSsnLY9M08KrEDCNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQBBoMMzQyMjM1MjY4NzgwIgxSAKqjDHrJoLDulgMqhQOJZEZ8URHDCHyB98SwHYvE57B8A%2BKKiF6W4%2F6h5SJizoVgoGtZWb6EK62IH3UcGGG5tHIrykqc1dmKHcKBuljcfA115kjjcJ6aQ%2FHWSGe3Q1MBNB93FpKm6EDFGTunpmDCFzh%2BJEidwT9Q%2Bxj0Rg7hqRBQQKNly6pMGVseXS5H8f0msPTPMiyMA0A5ZaM4M3GiERSduVv3z1s7%2Fc4UdnX%2Bfo7Ks0xo%2B8RlUBED4IZ2a%2FnnDw1mtFn3b2by0FnO%2BY1SrfSn3NcNAvGhNy3JnYuUIW26LiuEJB8779XsiJWlMyW0IseVhLx%2F0V3cQLVnEhXGOovAcCWOO8Tu4vSO%2FOBonjRz5yyXXEronoW8Fj5H2BKUEI%2BRgulGUAMLWqbfoBN7vcHL1VGo9jEUSimcP0928dbhqddd4gYan63gm5z2%2Fuv1SX3dKvpMM1%2BE0u%2BHBMhMgtURWLGWWCtpkNZpFbF8SJz1hqO2Rnv2PU0B0qzWvNWCtT1AfpE8v2RiyFZEEasuzdGU9TDguoDGBjqeAcgdBo7EPiUVG7UDEisw%2Bk0XFQ1sQ8W4AccKUHELmOLHOuYeCUthAxidStSJ9ioyPbmP9ynmAXXLDtzFLUw064LrzE9upOSGH2hV3o3krZGSsQDQXyT3uYD0poRySLFSG7p4wqQA%2BGoprC98Le5%2F07Z52K%2B7PCzCghqBmEysaFO%2B171XY5K3R0v6ImvfpRdLyHP%2BWQ1VCQyYY4xr2DVg"
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
