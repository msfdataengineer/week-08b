# Streamlit app entrypoint
import streamlit as st
import pandas as pd
from logics.customer_query_handler import process_user_message
from helper_functions.utility import check_password  

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="HDB Explorer"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("HDB Explorer 🏢")

# Check if the password is correct.  
if not check_password():  
    st.stop()

form = st.form(key="form")
form.subheader("Ask about HDB Flats")

user_prompt = form.text_area("Enter your query here", height=200)

if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")

    st.divider()

    # Get AI response and details
    response, flat_details = process_user_message(user_prompt)
    st.write(response)

    st.divider()

    # Show raw details if found
    if flat_details:
        st.subheader("Matching Flats Information")
        df = pd.DataFrame(flat_details)
        st.dataframe(df)
    else:
        st.info("No matching flats found for your query.")
