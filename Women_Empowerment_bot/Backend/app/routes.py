from fastapi import APIRouter
from pydantic import BaseModel
from app.chatbot import generate_response
from app.chatbot import search_jobs_endpoint
from app.mentorbot import search_mentorship_programs_endpoint
from app.jobsearch import search_jobs 

router = APIRouter()

# Define the request body structure
class ChatRequest(BaseModel):
    message: str

class JobSearchRequest(BaseModel):
    query: str

@router.post("/chat")
def chat_endpoint(chat_request: ChatRequest):
    user_message = chat_request.message
    bot_response = generate_response(user_message)
    print(bot_response)
    return {"response": bot_response}

@router.post("/search_jobs")
def job_search_endpoint(job_request: JobSearchRequest):
    query = job_request.query
    matched_jobs = search_jobs_endpoint(query)
    return {"response": matched_jobs}

@router.post("/mentorship")
def job_search_endpoint(job_request: JobSearchRequest):
    query = job_request.query
    matched_jobs = search_mentorship_programs_endpoint(query)
    return {"response": matched_jobs}