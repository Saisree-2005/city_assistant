from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Smart City Assistant API")

# Allow Streamlit (or any web client) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict this
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the summarizer *once* at startup
@app.on_event("startup")
def load_model():
    global summarizer
    summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

class SummarizeRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/summarize")
def summarize(req: SummarizeRequest):
    result = summarizer(
        req.text,
        max_length=130,
        min_length=30,
        do_sample=False
    )
    return {"summary": result[0]["summary_text"]}
