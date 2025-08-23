import streamlit as st 
import os
from dotenv import load_dotenv
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





st.header("🤖 AI-StorySmith", divider="rainbow")
st.subheader("✨ Create Amazing Stories with AI")
st.markdown("*Powered by Advanced Language Models*")
st.write("**Developer: Jahanzeb**")

# Create two columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Story Details")
    
    char_name = st.text_input(
        "Character Name:", 
        placeholder="e.g., Mitten, Aurora, Captain Zara",
        help="Enter the main character's name"
    )
    
    char_type = st.text_input(
        "Character Type:", 
        placeholder="e.g., Cat, Wizard, Robot, Princess",
        help="What kind of character is this?"
    )
    
    char_persona = st.text_area(
        "Character Personality:", 
        placeholder="e.g., Friendly, curious, brave, mysterious, witty",
        help="Describe the character's personality traits",
        height=100
    )
    
    char_location = st.text_input(
        "Story Location:", 
        placeholder="e.g., Enchanted Forest, Mars Colony, Medieval Castle",
        help="Where does the story take place?"
    )

with col2:
    st.subheader("⚙️ Story Settings")

    story_length = st.slider(
        "Story Length (sentences):",
        min_value=10,
        max_value=500,
        value=50,
        step=10,
        help="Choose how many sentences your story should have"
    )
    
    estimated_words = story_length * 15
    reading_time = max(1, estimated_words // 200)
    st.info(f"📖 Estimated: ~{estimated_words} words, ~{reading_time} min read")
    
    story_premise = st.multiselect(
        "Story Theme(s):",
        ["Love", "Adventure", "Mystery", "Horror", "Comedy", "Sci-Fi", 
         "Fantasy", "Thriller", "Drama", "Action", "Slice of Life", "Historical"],
        help="Select one or more themes for your story"
    )
    
    creative_control = st.select_slider(
        "Creativity Level:",
        options=["Very Low", "Low", "Medium", "High", "Very High"],
        value="Medium",
        help="Higher creativity = more unexpected and creative story elements"
    )

temperature_map = {
    "Very Low": 0.2,
    "Low": 0.4,
    "Medium": 0.6,
    "High": 0.8,
    "Very High": 0.95
}
temperature = temperature_map[creative_control]

st.divider()

if st.button("Generate My Story", type="primary", use_container_width=True):
    
    with st.spinner("🎨 Crafting your story... This may take a moment"):
        try:
            prompt = get_llm_prompt(
                char_name,
                char_type,
                char_persona,
                char_location,
                story_length,
                story_premise,
            )

            
            result = get_llm_response(prompt, temperature)
                
            st.success("Your story has been generated!")

            if result:
                st.markdown("## 📖 Your Generated Story")
                st.write(result)
                
                story_text = f"Title: Story of {char_name}\n\n{result}"
                st.download_button(
                    "📥 Download Story as Text File",
                    story_text,
                    file_name=f"story_{char_name.lower().replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            else:
                st.error("Unexpected response format")
                    
            
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

# Sidebar with tips
with st.sidebar:
    st.markdown("## 💡 Story Writing Tips")
    st.markdown("""
    - **Character Name**: Choose something memorable
    - **Personality**: Mix 2-3 contrasting traits for depth
    - **Location**: Be specific for richer details
    - **Themes**: Combine 2-3 themes for complexity
    - **Length**: 50-100 sentences work well for most stories
    """)
    
    st.markdown("## 🎯 Creativity Levels")
    st.markdown("""
    - **Very Low**: Predictable, safe stories
    - **Low**: Slightly creative with familiar elements  
    - **Medium**: Balanced creativity and coherence
    - **High**: Creative with unexpected twists
    - **Very High**: Highly creative and unpredictable
    """)