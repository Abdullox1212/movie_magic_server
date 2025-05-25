from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import channels as channel_model

router = APIRouter(tags=["Channels"])

class ChannelCreate(BaseModel):
    username: str

@router.post("/channels")
async def add_channel(channel: ChannelCreate):
    """Yangi kanal qo'shish"""
    try:
        channel_model.add_channel(channel.username)
        return {"message": "Kanal muvaffaqiyatli qo'shildi"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/channels/{username}")
async def delete_channel(username: str):
    """Kanalni o'chirish"""
    channel_model.remove_channel(username)
    return {"message": "Kanal muvaffaqiyatli o'chirildi"}

@router.get("/channels")
async def list_channels():
    """Barcha kanallar ro'yxati"""
    channels = channel_model.get_all_channels()
    return {"channels": channels}

@router.get("/channels/{username}/exists")
async def check_channel_exists(username: str):
    """Kanal mavjudligini tekshirish"""
    exists = channel_model.channel_exists(username)
    return {"exists": exists}