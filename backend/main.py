import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Code Converter API")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("WARNING: GEMINI_API_KEY environment variable not set. Real conversions will fail.")

class ConversionRequest(BaseModel):
    code: str
    source_language: str
    target_language: str

class ConversionResponse(BaseModel):
    converted_code: str
    message: str = "Success"

@app.post("/api/convert", response_model=ConversionResponse)
async def convert_code(request: ConversionRequest):
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        # Mock response if no key is provided, so the UI can still be tested
        return ConversionResponse(
            converted_code=f"// Mock converted {request.target_language} code\n// Please set GEMINI_API_KEY in backend/.env for real conversions\n\n{request.code}",
            message="Mock conversion successful (API Key missing)"
        )
    
    # Configure inside the request in case it was just loaded
    genai.configure(api_key=api_key)
    
    prompt = f"""
You are an expert programmer. Convert the following {request.source_language} code into {request.target_language} code.
Ensure the logic remains the same, but use the idioms and standard conventions of {request.target_language}.
Please ONLY provide the code. Do NOT wrap it in Markdown codeblocks (like ```python). Just return the raw code.

Here is the source code:
{request.code}
"""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Clean up Markdown block if the model included it despite instructions
        if text.startswith("```"):
            lines = text.split("\n")
            if len(lines) > 2 and lines[0].startswith("```") and lines[-1] == "```":
                text = "\n".join(lines[1:-1])
        
        return ConversionResponse(converted_code=text)
    except Exception as e:
        print(f"Conversion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "api_key_configured": bool(API_KEY)}

# Serve frontend static files
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
