from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import google.generativeai as genai
import os
import re

# Initialize FastAPI app
app = FastAPI()

# Setup Gemini API Key
api_key = 'AIzaSyDLC4VdgUAxLoSC8Leb-efJ2p1BTH6E5xI'
os.environ['API_KEY'] = api_key
genai.configure(api_key=os.environ["API_KEY"])

# ---- Request Models ---- #
class MentorshipRequest(BaseModel):
    user_query: str

# ---- Mentorship Program functionality ---- #

# CSV File for Mentorship Programs
CSV_FILE_MENTORSHIP = r'L:\My projects\Women_Job_Chatbot\Backend\app\knowledge_base\Mentorship_posting\mentorship_programs.csv'

def load_mentorship_programs():
    return pd.read_csv(CSV_FILE_MENTORSHIP)

# Extract field from query (e.g., "Finance", "Design", etc.)
def extract_field(query: str, fields):
    for field in fields:
        if field.lower() in query.lower():
            return field
    return None

def search_mentorship_programs(query: str):
    df = load_mentorship_programs()
    all_fields = df['field'].dropna().unique()

    field_in_query = extract_field(query, all_fields)

    keywords = [word.lower() for word in re.findall(r'\w+', query) if word.lower() not in [
        'mentorship', 'program', 'in', 'for', 'opportunity', 'about', 'more'
    ]] 

    if not keywords:
        return pd.DataFrame()

    matched = df[
        df['program_name'].str.lower().apply(lambda x: any(kw in x for kw in keywords))
    ]

    if field_in_query:
        matched = matched[matched['field'].str.lower() == field_in_query.lower()]

    return matched

def generate_mentorship_response(programs_df, user_input):
    model = genai.GenerativeModel('gemini-1.5-flash')

    if programs_df.empty:
        return "I'm sorry, but I couldn't find any mentorship programs matching your query."

    programs_text = "\n".join([
        f"- **{row['program_name']}** in *{row['field']}* led by {row['mentor_name']}:\n"
        f"  *Description:* {row['description']}"
        for index, row in programs_df.iterrows()
    ])

    prompt = (
        "You are a helpful mentorship chatbot specialized in assisting individuals to find the right mentorship programs.\n\n"
        "User's Query: " + user_input + "\n\n"
        "Available mentorship programs:\n"
        f"{programs_text}\n\n"
        "Write a short and friendly response suggesting these mentorship programs to the user. Be encouraging, provide mentor names and short descriptions, and avoid listing the programs directly."
    )

    response = model.generate_content(prompt)
    return response.text.strip()

# ---- API Endpoints ---- #

@app.post("/search_mentorship_programs")
def search_mentorship_programs_endpoint(request: MentorshipRequest):
    matched_programs = search_mentorship_programs(request)

    if matched_programs.empty:
        return {"response": "Sorry, no mentorship programs found matching your query."}

    smart_response = generate_mentorship_response(matched_programs, request)
    return {"response": smart_response}


# prompt = "show me the mentorship program of Finance field."
# print(search_mentorship_programs_endpoint(prompt))