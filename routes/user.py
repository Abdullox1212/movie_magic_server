from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from models import user as user_model

router = APIRouter(tags=["Users"])

# Pydantic modellar
class UserCreate(BaseModel):
    id: int
    full_name: str
    username: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    subscribed: bool

class UserExistsResponse(BaseModel):
    exists: bool

class SubscriptionStatus(BaseModel):
    subscribed: bool

class UsersIdResponse(BaseModel):
    users_ids: List[int]

class MessageResponse(BaseModel):
    message: str    

class AdminStatus(BaseModel):
    is_admin: bool

class AdminUser(BaseModel):
    id: int
    full_name: str
    username: str    

# Xatolik xabarlari
USER_NOT_FOUND = "Foydalanuvchi topilmadi"
USER_ADDED = "Foydalanuvchi muvaffaqiyatli qo'shildi"
SUBSCRIPTION_UPDATED = "Obuna holati yangilandi"

@router.post("/users", response_model=dict)
async def create_user(user: UserCreate):
    """
    Yangi foydalanuvchini ID bilan birga qo'shish
    
    Parameters:
    - id: Foydalanuvchi IDsi (raqam)
    - full_name: Foydalanuvchi to'liq ismi
    - username: Foydalanuvchi nomi
    
    Returns:
    - message: Natija xabari
    """
    try:
        user_model.insert_user(
            user_id=user.id,
            full_name=user.full_name,
            username=user.username
        )
        return {
            "message": "Foydalanuvchi muvaffaqiyatli qo'shildi",
            "user_id": user.id
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Xatolik yuz berdi: {str(e)}"
        )

@router.get(
    "/users",
    response_model=List[UserResponse],
    summary="Barcha foydalanuvchilarni olish"
)
async def get_users():
    """
    Bazadagi barcha foydalanuvchilarni ro'yxatini qaytaradi.
    """
    return user_model.get_all_users()

@router.get(
    "/users/{user_id}/exists",
    response_model=UserExistsResponse,
    summary="Foydalanuvchi mavjudligini tekshirish"
)
async def check_user_exists(user_id: int):
    """
    Foydalanuvchi IDsi bo'yicha mavjudligini tekshiradi.
    
    Parameters:
    - user_id: Tekshiriladigan foydalanuvchi IDsi
    
    Returns:
    - exists: True - agar foydalanuvchi mavjud bo'lsa, False - aks holda
    """
    exists = user_model.get_user(user_id)
    return {"exists": exists}

@router.get(
    "/users/{user_id}/subscribed",
    response_model=SubscriptionStatus,
    summary="Foydalanuvchi obuna holatini tekshirish"
)
async def is_user_subscribed(user_id: int):
    """
    Foydalanuvchining obuna holatini tekshirish.
    
    Parameters:
    - user_id: Foydalanuvchi IDsi
    """
    subscribed = user_model.is_subscribed(user_id)
    if subscribed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=USER_NOT_FOUND
        )
    return {"subscribed": subscribed}

@router.put(
    "/users/{user_id}/subscription",
    response_model=MessageResponse,
    summary="Foydalanuvchi obuna holatini yangilash"
)
async def update_subscription(user_id: int, status: bool):
    """
    Foydalanuvchi obuna holatini yangilash.
    
    Parameters:
    - user_id: Foydalanuvchi IDsi
    - status: Yangi obuna holati (True/False)
    """
    try:
        user_model.update_subscription_status(user_id, status)
        return {"message": SUBSCRIPTION_UPDATED}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Obuna holatini yangilashda xatolik: {str(e)}"
        )

@router.get(
    "/users/ids",
    response_model=UsersIdResponse,
    summary="Barcha foydalanuvchilar IDlarini olish"
)
async def get_all_users_ids():
    """
    Bazadagi barcha foydalanuvchilar IDlarini qaytaradi.
    """
    users_id = user_model.get_all_users_ids()
    return {"users_ids": users_id}



#ADMIN ROUTES
@router.put(
    "/users/{user_id}/admin",
    response_model=dict,
    summary="Foydalanuvchi admin statusini o'zgartirish"
)
async def set_admin(user_id: int, status: AdminStatus):
    """
    Foydalanuvchiga admin huquqini berish/olish
    
    Parameters:
    - user_id: Foydalanuvchi IDsi
    - is_admin: True - admin qilish, False - adminlikdan chiqarish
    """
    try:
        user_model.set_admin_status(user_id, status.is_admin)
        return {"message": "Admin statusi muvaffaqiyatli o'zgartirildi"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Xatolik yuz berdi: {str(e)}"
        )

@router.get(
    "/users/admins",
    response_model=List[AdminUser],
    summary="Barcha admin foydalanuvchilarni olish"
)
async def get_admin_users():
    """
    Barcha admin foydalanuvchilarni ro'yxatini qaytaradi
    """
    return user_model.get_admins()