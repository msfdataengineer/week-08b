import os
import json
import pandas as pd
from helper_functions import llm

# HDB dataset URL
HDB_URL = "https://raw.githubusercontent.com/BlueSkyLT/siteselect_sg/refs/heads/main/dataset/hdb.csv"

# Load HDB dataset safely
try:
    df_hdb = pd.read_csv(HDB_URL)
except Exception as e:
    print("Error loading HDB CSV:", e)
    df_hdb = pd.DataFrame()

# Normalise column names to lower_case for easier access
df_hdb.columns = [c.strip().lower() for c in df_hdb.columns]

# Build dictionary: flat_type -> list of details
flat_type_n_details = {}
if not df_hdb.empty:
    for _, row in df_hdb.iterrows():
        ft = row.get("flat_type")
        if pd.isna(ft):
            continue
        details = {
            "block_no": row.get("blk_no"),
            "street": row.get("street"),
            "year_completed": row.get("year_completed"),
            "total_dwelling_units": row.get("total_dwelling_units"),
            "planning_area": row.get("planning_area"),
        }
        flat_type_n_details.setdefault(ft, []).append(details)


def identify_flat_types(user_message):
    """
    Use LLM to identify relevant flat types from user queries.
    """
    delimiter = "####"

    system_message = f"""
    You will be provided with user queries about HDB flats. \
    The query will be enclosed in the pair of {delimiter}.

    Decide if the query is relevant to any flat types
    in the Python dictionary below, where the key is `flat_type`.

    {list(flat_type_n_details.keys())}

    If relevant flat type(s) are found, output a list of dictionaries
    where each dictionary contains:
    1) flat_type
    2) details (list of matching blocks for that flat type)

    If no relevant flat types are found, output [].

    Ensure the response contains only JSON list of dicts, no extra text.
    """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_message}{delimiter}"},
    ]

    response_str = llm.get_completion_by_messages(messages)
    response_str = response_str.replace("'", "\"")
    try:
        flat_type_response = json.loads(response_str)
    except json.JSONDecodeError:
        flat_type_response = []
    return flat_type_response


def get_flat_details(list_of_relevant_flats: list[dict]):
    """
    Given a list of relevant flat types, return the full details.
    """
    details_list = []
    for item in list_of_relevant_flats:
        ft = item.get("flat_type")
        if ft in flat_type_n_details:
            details_list.extend(flat_type_n_details[ft])
    return details_list


def generate_response_based_on_flat_details(user_message, flat_details):
    """
    Generate a customer-friendly response using flat details.
    """
    delimiter = "####"

    system_message = f"""
    Follow these steps to answer user queries about HDB flats.
    The query will be delimited with {delimiter}.

    Step 1:{delimiter} Identify relevant flat types from query.
    Step 2:{delimiter} Use the details of those flats below:
    {flat_details}
    Step 3:{delimiter} Generate a friendly, factually accurate response.
    Include block, street, year built, planning area, and dwelling unit details where useful.
    Make the response informative and helpful for decision-making.
    """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_message}{delimiter}"},
    ]

    response = llm.get_completion_by_messages(messages)
    response = response.split(delimiter)[-1]  # take final response part
    return response


def process_user_message(user_input):
    """
    Master function to process user query:
    1. Identify flat types
    2. Fetch flat details
    3. Generate response
    """
    relevant_flats = identify_flat_types(user_input)
    print("Relevant flat types:", relevant_flats)

    flat_details = get_flat_details(relevant_flats)
    reply = generate_response_based_on_flat_details(user_input, flat_details)

    return reply, flat_details
