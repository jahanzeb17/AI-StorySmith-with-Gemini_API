import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def load_model():
    return ChatGroq(
        model="llama-3.3-70b-versatile"
    )

def get_llm_prompt(
        char_name, 
        char_type, 
        char_persona,
        char_location,
        story_length, 
        story_premise
    ):
    
    if isinstance(story_premise, list):
        premise_str = ", ".join(story_premise)
    else:
        premise_str = story_premise
    
    template = """You are a creative storyteller. Write an engaging story with approximately {story_length} sentences based on the following details:

    Character Details:
    - Name: {character_name}
    - Type: {character_type}
    - Personality: {character_persona}
    - Location: {character_location}
    - Story Theme(s): {story_premise}

    Story Structure Requirements:
    - Create a compelling narrative with a clear beginning, middle, and end
    - Include character development and engaging dialogue
    - Build tension and resolution appropriate to the themes
    - Write approximately {story_length} sentences total
    - Ensure the story flows naturally and maintains reader interest
    - Include vivid descriptions of the setting and characters

    Make the story creative, engaging, and well-paced. Focus on quality storytelling rather than strict chapter divisions."""

    prompt = ChatPromptTemplate.from_template(template)

    formatted_prompt = prompt.format(
        story_length=story_length,
        character_name=char_name,
        character_type=char_type,
        character_persona=char_persona,
        character_location=char_location,
        story_premise=premise_str
    )

    return formatted_prompt

def get_llm_response(prompt, temperature):
    model = load_model()
    model.temperature = temperature
    response = model.invoke(prompt)
    
    return response.content