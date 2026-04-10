# load api key
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Validate API key exists
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file. Please add it.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# testcase generation

def generate_test_cases(feature_description, model="gpt-3.5-turbo"):
    prompt = f"""
    Generate detailed test cases for the following feature:

    Feature: {feature_description}

    Include:
    1. Analyze requirement
    2. Generate scenarios
    3. Generate test cases
    4. Add edge cases
    5. Expected Results for each test case
    """
    # Advance Prompt:
    prompt = f"""
    You are a senior QA engineer.

    Generate detailed and structured test cases for the following feature:

    Feature:
    {feature}

    Instructions:
    - Cover positive, negative, and edge cases
    - Include boundary conditions
    - Consider real-world scenarios

    Format strictly as:

    Test Case ID:
    Scenario:
    Preconditions:
    Test Steps:
    Expected Result:
    Priority:
    Test Type (Functional/Negative/Edge):

    Also ensure:
    - Clear and professional QA language
    - No vague steps
    """

    # API Running 
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating test cases: {str(e)}"


# Example usage
if __name__ == "__main__":
    try:
        feature = input("Enter feature description: ")
        output = generate_test_cases(feature)

        print("\nGenerated Test Cases:\n")
        print(output)
    except KeyboardInterrupt:
        print("\nExited by user.")
    except Exception as e:
        print(f"Error: {str(e)}")
