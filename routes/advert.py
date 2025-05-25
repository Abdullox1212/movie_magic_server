from fastapi import UploadFile, File
from services.advert import send_advert_with_photo_file
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os


router = APIRouter(tags=["Advertisement"])

class AdvertRequest(BaseModel):
    image_url: str
    caption: str

@router.post("/send-advert-file")
async def send_advert_file(
    caption: str,
    photo: UploadFile = File(...)
):
    """
    Fayl orqali reklama yuborish
    
    Parameters:
    - photo: Yuklanadigan rasm fayli
    - caption: Rasmga izoh
    """
    try:
        # Faylni vaqtincha saqlaymiz
        temp_path = f"temp_{photo.filename}"
        with open(temp_path, "wb") as buffer:
            buffer.write(await photo.read())
        
        result = send_advert_with_photo_file(temp_path, caption)
        
        # Vaqtincha faylni o'chiramiz
        os.remove(temp_path)
        
        return {
            "message": "Reklama fayli orqali yuborildi",
            "stats": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fayl yuborishda xatolik: {str(e)}"
        )