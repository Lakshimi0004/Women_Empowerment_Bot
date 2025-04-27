import pandas as pd

# Load your CSV dataset once
jobs_df = pd.read_csv(r'L:\My projects\Women_Job_Chatbot\Backend\app\knowledge_base\job_postings\job_listings.csv')  # Adjust path if needed

def search_jobs(query: str):
    # Simple search: Find jobs whose title contains the query
    filtered_jobs = jobs_df[jobs_df['title'].str.contains(query, case=False, na=False)]
    return filtered_jobs.to_dict(orient="records")
