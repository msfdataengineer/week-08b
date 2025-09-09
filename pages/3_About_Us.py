import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="About HDB Explorer"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About HDB Explorer 🏢")

st.write("""
The **HDB Explorer** is an interactive platform that helps users explore Singapore's HDB flats.
It leverages AI to answer queries about flat types, locations, sizes, and completion years.
""")

with st.expander("Project Scope"):
    st.write("""
- Provide a user-friendly way to explore HDB flat details.
- Allow natural language queries about flat types, locations, and sizes.
- Support individuals, families, or researchers looking for housing information.
""")

with st.expander("Objectives"):
    st.write("""
- Simplify access to detailed HDB flat information.
- Offer AI-powered answers to user queries.
- Display flat details clearly using tables and optional future map views.
""")

with st.expander("Data Sources"):
    st.write("""
- HDB Flat Dataset from [GitHub](https://github.com/BlueSkyLT/siteselect_sg/blob/main/dataset/hdb.csv)
- Publicly available HDB housing information
""")

with st.expander("Features"):
    st.write("""
1. **AI-Powered Search** – Ask questions like *"Show me 3-room flats in Jurong"*.
2. **Flat Details Viewer** – See block number, street, planning area, year completed, and total units.
3. **Password-Protected Access** – Secures the app for authorised users.
4. **Future Enhancements** – Interactive map view, more filters, and improved query handling.
""")

with st.expander("How to use this App"):
    st.write("""
1. Enter your query about HDB flats in the text area.
2. Click the 'Submit' button.
3. The app will generate an AI-assisted response with relevant flat details.
4. Scroll down to view the matching flat information in the table.
""")
