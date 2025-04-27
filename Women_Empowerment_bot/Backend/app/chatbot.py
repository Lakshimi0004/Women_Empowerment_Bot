# filename: app.py

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
class JobSearchRequest(BaseModel):
    user_query: str

class ChatRequest(BaseModel):
    user_query: str

# ---- Existing Chatbot functionality ---- #
def generate_response(user_input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = (
        "This is a chatbot application regarding women empowerment. "
        "Answer the user's question smartly and concisely without copying from any source.\n\n"
        f"User Query: {user_input}"
    )
    response = model.generate_content(prompt)
    return response.text

# ---- New Job Search functionality (from testing.py) ---- #

# CSV File
CSV_FILE = r'L:\My projects\Women_Job_Chatbot\Backend\app\knowledge_base\job_postings\job_listings.csv'

def load_jobs():
    return pd.read_csv(CSV_FILE)

def extract_location(query: str, locations):
    for location in locations:
        if location.lower() in query.lower():
            return location
    return None

def search_jobs_in_csv(query: str):
    df = load_jobs()
    all_locations = df['location'].dropna().unique()

    location_in_query = extract_location(query, all_locations)

    keywords = [word.lower() for word in re.findall(r'\w+', query) if word.lower() not in [
        'job', 'jobs', 'in', 'at', 'for', 'remote', 'full-time', 'internship', 'part-time', 'manner', 'opportunity'
    ]]

    if not keywords:
        return pd.DataFrame()

    matched = df[
        df['title'].str.lower().apply(lambda x: any(kw in x for kw in keywords))
    ]

    if location_in_query:
        matched = matched[matched['location'].str.lower() == location_in_query.lower()]

    return matched

def generate_job_response(jobs_df, user_input):
    model = genai.GenerativeModel('gemini-1.5-flash')

    if jobs_df.empty:
        return "I'm sorry, but I couldn't find any jobs matching your query."

    jobs_text = "\n".join([
        f"- **{row['title']}** at *{row['company']}* ({row['location']}) [{row['job_type']}]"
        for index, row in jobs_df.iterrows()
    ])

    prompt = (
        "You are a helpful career chatbot specialized in assisting women to find the right job or internship opportunities.\n\n"
        "User's Query: " + user_input + "\n\n"
        "Available job/internship opportunities:\n"
        f"{jobs_text}\n\n"
        "Write a warm, encouraging response suggesting these jobs to the user. Avoid copying the list directly — instead, convey the options in a friendly and motivating way."
    )

    response = model.generate_content(prompt)
    return response.text.strip()

# ---- API Endpoints ---- #

# # ✨ New Job Search Chatbot Endpoint
# @app.post("/search_jobs")
def search_jobs_endpoint(request):
    matched_jobs = search_jobs_in_csv(request)

    if matched_jobs.empty:
        return {"response": "Sorry, no jobs found matching your query."}

    smart_response = generate_job_response(matched_jobs, request)
    return smart_response
    # return {
    #     "response": smart_response,
    #     "matched_jobs": matched_jobs.to_dict(orient="records")
    # }
