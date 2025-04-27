from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Women Empowerment and Job Finder Chatbot",
    description="A chatbot to support women empowerment and help find jobs.",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uvicorn main:app --reload

# Include routes
app.include_router(router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Women Empowerment & Job Finder Chatbot!"}
