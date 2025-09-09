import os
import json
import pandas as pd
from helper_functions import llm

# HDB dataset URL
HDB_URL = "https://s3.ap-southeast-1.amazonaws.com/table-downloads-ingest.data.gov.sg/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/6f8109f7bce05c219b3825a999cc7f3a02cbc19fe536138a5eaf86bfe6d8711f.csv?AWSAccessKeyId=ASIAU7LWPY2WEO6Y4UQJ&Expires=1757427608&Signature=9vpQC%2FWfA9CtLiV2SGYlvfI%2FM3c%3D&X-Amzn-Trace-Id=Root%3D1-68c02988-7562c8fc3780214f0f91fbc1%3BParent%3D5261c04c148c5b61%3BSampled%3D0%3BLineage%3D1%3A9e07a47d%3A0&response-content-disposition=attachment%3B%20filename%3D%22ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv%22&x-amz-security-token=IQoJb3JpZ2luX2VjEG0aDmFwLXNvdXRoZWFzdC0xIkYwRAIgfkcUHQm1W2qxTP2GixiViAY4IDh5RiwQCoKalN27eVcCIBUUoVQqDS5vBwHGnxnImThNoG15x%2FusbUWSsnLY9M08KrEDCNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQBBoMMzQyMjM1MjY4NzgwIgxSAKqjDHrJoLDulgMqhQOJZEZ8URHDCHyB98SwHYvE57B8A%2BKKiF6W4%2F6h5SJizoVgoGtZWb6EK62IH3UcGGG5tHIrykqc1dmKHcKBuljcfA115kjjcJ6aQ%2FHWSGe3Q1MBNB93FpKm6EDFGTunpmDCFzh%2BJEidwT9Q%2Bxj0Rg7hqRBQQKNly6pMGVseXS5H8f0msPTPMiyMA0A5ZaM4M3GiERSduVv3z1s7%2Fc4UdnX%2Bfo7Ks0xo%2B8RlUBED4IZ2a%2FnnDw1mtFn3b2by0FnO%2BY1SrfSn3NcNAvGhNy3JnYuUIW26LiuEJB8779XsiJWlMyW0IseVhLx%2F0V3cQLVnEhXGOovAcCWOO8Tu4vSO%2FOBonjRz5yyXXEronoW8Fj5H2BKUEI%2BRgulGUAMLWqbfoBN7vcHL1VGo9jEUSimcP0928dbhqddd4gYan63gm5z2%2Fuv1SX3dKvpMM1%2BE0u%2BHBMhMgtURWLGWWCtpkNZpFbF8SJz1hqO2Rnv2PU0B0qzWvNWCtT1AfpE8v2RiyFZEEasuzdGU9TDguoDGBjqeAcgdBo7EPiUVG7UDEisw%2Bk0XFQ1sQ8W4AccKUHELmOLHOuYeCUthAxidStSJ9ioyPbmP9ynmAXXLDtzFLUw064LrzE9upOSGH2hV3o3krZGSsQDQXyT3uYD0poRySLFSG7p4wqQA%2BGoprC98Le5%2F07Z52K%2B7PCzCghqBmEysaFO%2B171XY5K3R0v6ImvfpRdLyHP%2BWQ1VCQyYY4xr2DVg"

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
