import json
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client()  # Automatically reads GEMINI_API_KEY from env

MODEL_NAME = "gemini-2.5-flash"  # Use an available Gemini model

def extract_skills_experience(text: str):
    prompt = f"""
    Extract the skills and years of experience required from the following job description.

    Return strictly in JSON format with fields:
    {{
    "skills": [ "skill1", "skill2", ... ],
    "experience": "only the years of experience mentioned. Normalize it to a clear format such as '3 years', '3-5 years', '5+ years'. 
                    Capture all possible expressions including: 
                    - numeric ranges ('3-5 years', '3 to 5 yrs'),
                    - minimum/at least ('at least 3 years', 'minimum 5 yrs exp'),
                    - plus signs ('5+ years'),
                    - words ('five years experience'),
                    - overview sections ('Experience Required: 5 years').
                    If multiple mentions exist, select the most specific or highest value.
                    If no mention is found, return an string as Not Mentioned."
    }}

    Job Description:
    {text}
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )

        content = response.text.strip()
        print("Raw Gemini output:", content)  

        # Extract JSON block only
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            content = match.group(0)

        result = json.loads(content)
        return result

    except Exception as e:
        print("Gemini API error:", e)
        return {"skills": [], "experience": ""}
    