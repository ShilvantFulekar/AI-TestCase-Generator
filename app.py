import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OPENAI_API_KEY not found in .env file. Please add it.")
    st.stop()

client = OpenAI(api_key=api_key)

# Function to generate test cases
def agentic_test_generator(feature_description, model="gpt-3.5-turbo"):
    """Generate test cases using OpenAI API"""
    prompt = f"""
    Generate detailed test cases for the following feature:

    Feature: {feature_description}

    Include:
    - Test Case ID
    - Test Scenario
    - Steps
    - Expected Result
    
    Format the output clearly with proper numbering and structure.
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error generating test cases: {str(e)}"


# Streamlit UI
st.set_page_config(page_title="AI Test Case Generator", layout="wide")
st.title("🤖 AI Test Case Generator (Agentic AI)")
st.markdown("Generate comprehensive test cases using OpenAI GPT")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    model = st.selectbox(
        "Select Model",
        ["gpt-3.5-turbo"],
        help="Choose the AI model to use"
    )

# Main content
feature = st.text_area(
    "Enter Feature Description",
    height=150,
    placeholder="Example: User login with email and password, with 2FA support"
)

col1, col2 = st.columns([1, 4])

if col1.button("🚀 Generate Test Cases", use_container_width=True):
    if not feature.strip():
        st.warning("⚠️ Please enter a feature description first!")
    else:
        with st.spinner("⏳ Generating test cases... Please wait..."):
            result = agentic_test_generator(feature, model=model)

        st.subheader("✅ Generated Test Cases")
        st.markdown(result)

        # Add download button
        st.download_button(
            label="📥 Download as Text",
            data=result,
            file_name="test_cases.txt",
            mime="text/plain"
        )

if col2.button("ℹ️ About", use_container_width=True):
    st.info("""
    ### About AI Test Case Generator
    This tool uses OpenAI's GPT to automatically generate comprehensive test cases 
    for your software features. Simply describe your feature and get detailed test 
    scenarios with steps and expected results.
    """)
