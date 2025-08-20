from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.caption_service import generate_hashtags_logic
from app.schemas.caption import CaptionRequestProperty, ModelNameOption
from PIL import Image
from pillow_heif import register_heif_opener
from io import BytesIO

router = APIRouter()

register_heif_opener()


@router.post("/")
async def generate_hashtags(
    model_name: ModelNameOption = Form(...),
    language: str = Form(...),
    tone: str = Form(...),
    context: str = Form(""),
    file: UploadFile = File(...)
):
    image_bytes = await file.read()

    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"خطا در باز کردن تصویر: {e}")

    request = CaptionRequestProperty(
        model_name=model_name,
        language=language,
        tone=tone,
        context=context or None
    )

    hashtags = generate_hashtags_logic(request, image)
    return {"hashtags": hashtags}
