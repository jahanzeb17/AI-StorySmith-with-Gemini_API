from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from backend.user_input import User_Input
from backend.main import get_llm_prompt, get_llm_response


app = FastAPI(title="AI Story Generator", description="Generate creative stories using AI")

@app.get("/")
def home():
    return {"message": "Welcome to AI Story Generator API"}

@app.get("/health")
def health():
    return {"status": "OK", "message": "API is running successfully"}

@app.post("/generate")
def generate_story(data: User_Input):
    try:
        # validation
        if not data.char_name.strip():
            raise HTTPException(status_code=400, detail="Character name cannot be empty")
        if not data.char_type.strip():
            raise HTTPException(status_code=400, detail="Character type cannot be empty")
        if not data.char_persona.strip():
            raise HTTPException(status_code=400, detail="Character persona cannot be empty")
        if not data.char_location.strip():
            raise HTTPException(status_code=400, detail="Character location cannot be empty")
        if not data.story_premise:
            raise HTTPException(status_code=400, detail="At least one story premise must be selected")

        prompt = get_llm_prompt(
            data.char_name,
            data.char_type,
            data.char_persona,
            data.char_location,
            data.story_length, 
            data.story_premise
        )

        response = get_llm_response(prompt, data.temperature)

        return JSONResponse(
            status_code=200, 
            content={
                "response": response,
                "metadata": {
                    "character": data.char_name,
                    "length": f"{data.story_length} sentences",
                    "premises": data.story_premise,
                    "temperature": data.temperature
                }
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"error": f"Internal server error: {str(e)}"}
        )
