from PIL import Image
import random


def predict_disease(image_path):

    # Open image to verify that it is valid
    image = Image.open(image_path)

    # Temporary predictions
    diseases = [
        {
            "plant": "Tomato",
            "disease": "Early Blight",
            "confidence": 96.4
        },
        {
            "plant": "Potato",
            "disease": "Late Blight",
            "confidence": 93.7
        },
        {
            "plant": "Apple",
            "disease": "Apple Scab",
            "confidence": 95.2
        },
        {
            "plant": "Healthy",
            "disease": "No Disease Detected",
            "confidence": 98.1
        }
    ]

    result = random.choice(diseases)

    return {
        "plant": result["plant"],
        "disease": result["disease"],
        "confidence": result["confidence"],
        "symptoms": "The model will provide symptoms after training.",
        "treatment": "Treatment information will be added.",
        "prevention": "Prevention information will be added."
    }