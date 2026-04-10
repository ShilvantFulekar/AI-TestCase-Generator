# Agentic AI (Multi-Step System)
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def call_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response['choices'][0]['message']['content']


# Agent 1: Requirement Analyzer
def analyze_requirement(feature):
    prompt = f"Break down the feature into modules and key functionalities:\n{feature}"
    return call_openai(prompt)


# Agent 2: Scenario Generator
def generate_scenarios(analysis):
    prompt = f"Generate detailed test scenarios based on:\n{analysis}"
    return call_openai(prompt)


# Agent 3: Test Case Generator
def generate_test_cases(scenarios):
    prompt = f"""
    Generate structured test cases from these scenarios:

    {scenarios}

    Format:
    Test Case ID, Scenario, Steps, Expected Result, Priority
    """
    return call_openai(prompt)


# Agent 4: Validator (🔥 Powerful)
def validate_test_cases(test_cases):
    prompt = f"""
    Review and improve these test cases:
    - Add missing edge cases
    - Improve clarity
    - Remove duplicates

    {test_cases}
    """
    return call_openai(prompt)


# MAIN AGENT FLOW
def agentic_test_generator(feature):
    analysis = analyze_requirement(feature)
    scenarios = generate_scenarios(analysis)
    test_cases = generate_test_cases(scenarios)
    final_output = validate_test_cases(test_cases)

    return final_output


# Run
feature = input("Enter feature: ")
result = agentic_test_generator(feature)

print("\nFinal Test Cases:\n")
print(result)