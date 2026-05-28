from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google import genai
import os
import json
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI App
app = FastAPI()

# Gemini Client Setup
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


class QuestionResponse(BaseModel):
    role: str = Field(..., description="The interview role selected by the user")
    question: str = Field(..., description="The interview question (AI or Local Backup)")
    source: str = Field(..., description="Where the question came from: 'AI' or 'Local Backup'")

class AnswerPayload(BaseModel):
    role: str = Field(..., description="The interview role")
    question: str = Field(..., description="The question that was asked")
    answer: str = Field(..., min_length=10, description="User's answer, at least 10 characters")




@app.get("/")
def home():
    return {"message": "AI Mock Interview API Running"}

@app.get("/question/{role}", response_model=QuestionResponse)
def get_question(role: str):
    # 1. Pehle AI (Gemini) se try karenge
    try:
        prompt = f"You are an expert technical interviewer. Ask a single, direct, and relevant interview question for a {role} position. Do not provide any introduction, greetings, or answers. Just give the question."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # Agar AI successfully chal gaya
        return {
            "role": role,
            "question": response.text.strip(),
            "source": "AI"
        }
    
    # 2. Agar AI fail hua (Rate limit 429 ya koi bhi error aaya), toh Fallback chalega
    except Exception as e:
        print(f"AI Failed (Using Fallback JSON). Error: {str(e)}") # Server logs ke liye
        
        try:
            # Current file (main.py) ka exact rasta nikalna
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "questions.json")
            
            # Local JSON file se data read karna
            with open(file_path, "r") as f:
                local_questions = json.load(f)
            
            if role in local_questions and local_questions[role]:
                # Randomly ek question select karna us role ke liye
                backup_question = random.choice(local_questions[role])
                
                return {
                    "role": role,
                    "question": backup_question,
                    "source": "Local Backup"
                }
            else:
                raise HTTPException(status_code=404, detail="Role not found in local backup.")
                
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="AI failed and local questions.json file is missing.")

@app.post("/submit")
def submit_answer(payload: AnswerPayload):
    # Abhi ke liye bas success message aur answer wapas bhej rahe hain
    return {
        "message": "Answer successfully received by backend!",
        "received_answer": payload.answer
    }