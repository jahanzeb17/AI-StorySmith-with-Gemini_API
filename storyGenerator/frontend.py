import streamlit as st 
import requests

API_URL = "http://127.0.0.1:8000/generate"

st.set_page_config(
    page_title="AI Story Generator",
    page_icon="📚",
    layout="wide"
)

st.header("🤖 AI-Powered Story Generator", divider="rainbow")
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
    
    # Display estimated reading time
    estimated_words = story_length * 15
    reading_time = max(1, estimated_words // 200)  # 200 words per minute
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

# Map creativity levels to temperature values
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
    
    # Validation
    if not char_name.strip():
        st.error("Please enter a character name")
        st.stop()
    if not char_type.strip():
        st.error("Please enter the character type")
        st.stop()
    if not char_persona.strip():
        st.error("Please describe the character's personality")
        st.stop()
    if not char_location.strip():
        st.error("Please enter the story location")
        st.stop()
    if not story_premise:
        st.error("Please select at least one story theme")
        st.stop()

    with st.spinner("🎨 Crafting your story... This may take a moment"):
        try:
            # Make API request
            response = requests.post(API_URL, json={
                "char_name": char_name,
                "char_type": char_type,
                "char_persona": char_persona,
                "char_location": char_location,
                "story_length": story_length,
                "story_premise": story_premise,
                "temperature": temperature
            }, timeout=60)  # 60 second timeout

            if response.status_code == 200:
                result = response.json()
                
                # Success message
                st.success("Your story has been generated!")
                
                # Display metadata
                if "metadata" in result:
                    metadata = result["metadata"]
                    with st.expander("📊 Story Information"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Character", metadata["character"])
                        with col2:
                            st.metric("Length", metadata["length"])
                        with col3:
                            st.metric("Creativity", f"{metadata['temperature']:.1f}")
                        st.write(f"**Themes:** {', '.join(metadata['premises'])}")
                
                # Display the story
                if "response" in result:
                    st.divider()
                    st.markdown("## 📖 Your Generated Story")
                    st.markdown(result["response"])
                    
                    # Download button
                    story_text = f"Title: Story of {char_name}\n\n{result['response']}"
                    st.download_button(
                        "📥 Download Story as Text File",
                        story_text,
                        file_name=f"story_{char_name.lower().replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Unexpected response format")
                    
            else:
                # Handle API errors
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', 'Unknown error occurred')
                except:
                    error_message = f'HTTP {response.status_code} Error'
                
                st.error(f"Error generating story: {error_message}")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please make sure the FastAPI server is running on http://127.0.0.1:8000")
        except requests.exceptions.Timeout:
            st.error("Request timed out. The story generation took too long. Please try again with a shorter story length.")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {str(e)}")
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