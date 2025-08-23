from pydantic import BaseModel, Field
from typing import Annotated, List

class User_Input(BaseModel):
    char_name: Annotated[str, Field(..., description="Name of the Character.", examples=['Mitten'])]
    char_type: Annotated[str, Field(..., description="Type of the character.", examples=['Cat'])]
    char_persona: Annotated[str, Field(..., description="Personality of the character", examples=['Friendly, curious, adventurous'])]
    char_location: Annotated[str, Field(..., description="Location where character lives.", examples=['Andromeda Galaxy'])]
    story_length: Annotated[int, Field(..., ge=10, le=500, description="Number of sentences in the story (10-500)")]  # Changed to int
    story_premise: Annotated[List[str], Field(..., description="Select story premise (at least one)")]
    temperature: Annotated[float, Field(..., ge=0.0, le=1.0, description="Creativity level (0.0-1.0)")] = 0.7

