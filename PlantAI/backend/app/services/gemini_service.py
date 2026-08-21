import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from PIL import Image


# -----------------------------------
# Load environment variables
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(
    BASE_DIR / ".env"
)


# -----------------------------------
# Get Gemini API key
# -----------------------------------

api_key = os.getenv(
    "GEMINI_API_KEY"
)

if not api_key:

    raise RuntimeError(
        "GEMINI_API_KEY was not found "
        "in backend/.env"
    )


# -----------------------------------
# Create Gemini client
# -----------------------------------

client = genai.Client(
    api_key=api_key
)


# -----------------------------------
# Analyze plant image
# -----------------------------------

def analyze_plant(
    image_path: str
):

    image = Image.open(
        image_path
    ).convert("RGB")


    prompt = """
You are PlantAI, an AI plant disease
detection assistant.

Analyze the uploaded plant leaf image.

Identify:

1. Plant name
2. Disease name
3. Confidence score
4. Symptoms
5. Treatment
6. Prevention

Return ONLY valid JSON.

Use exactly this format:

{
    "plant": "plant name",
    "disease": "disease name or Healthy",
    "confidence": 0,
    "symptoms": "short description",
    "treatment": "short treatment advice",
    "prevention": "short prevention advice"
}

Rules:

- confidence must be a number between 0 and 100.
- If the image is not a plant leaf, return:
  "plant": "Unknown"
  "disease": "Unable to identify"
- Do not use Markdown.
- Do not add text outside the JSON.
"""


    # -----------------------------------
    # Call Gemini
    # -----------------------------------

    response = client.models.generate_content(

        model="gemini-3.6-flash",

        contents=[
            prompt,
            image
        ]
    )


    # -----------------------------------
    # Get response text
    # -----------------------------------

    text = response.text.strip()


    # -----------------------------------
    # Remove Markdown code fences
    # -----------------------------------

    if text.startswith("```"):

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        text = text.strip()


    # -----------------------------------
    # Convert JSON string to Python dict
    # -----------------------------------

    result = json.loads(
        text
    )


    return result