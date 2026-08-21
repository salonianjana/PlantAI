from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid

from backend.app.services.gemini_service import analyze_plant


router = APIRouter(
    prefix="/api",
    tags=["Prediction"]
)


# Folder where uploaded images are temporarily stored
UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    # -----------------------------------
    # 1. Check file type
    # -----------------------------------

    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/jpg",
        "image/webp"
    ]

    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid file type. "
                "Please upload JPG, PNG or WEBP."
            )
        )


    # -----------------------------------
    # 2. Create unique filename
    # -----------------------------------

    file_name = (
        f"{uuid.uuid4()}_{file.filename}"
    )

    file_path = (
        UPLOAD_DIR / file_name
    )


    # -----------------------------------
    # 3. Save uploaded image temporarily
    # -----------------------------------

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as e:

        print(
            "FILE SAVE ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Could not save uploaded image."
        )


    # -----------------------------------
    # 4. Send image to Gemini
    # -----------------------------------

    try:

        print(
            "Analyzing image with Gemini..."
        )

        result = analyze_plant(
            str(file_path)
        )

        print(
            "Gemini result:",
            result
        )


        # -----------------------------------
        # 5. Return prediction
        # -----------------------------------

        return {
            "success": True,
            "prediction": result
        }


    # -----------------------------------
    # 6. Show actual Gemini error
    # -----------------------------------

    except Exception as e:

        print(
            "GEMINI ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


    # -----------------------------------
    # 7. Delete image after processing
    # -----------------------------------

    finally:

        if file_path.exists():

            try:

                file_path.unlink()

                print(
                    "Temporary image deleted."
                )

            except Exception as e:

                print(
                    "DELETE ERROR:",
                    repr(e)
                )