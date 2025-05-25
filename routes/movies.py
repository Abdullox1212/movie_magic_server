from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from models import movies as movie_model
from typing import List, Dict, Optional

router = APIRouter(tags=["Movies"])

# Pydantic modellar
class MovieCreate(BaseModel):
    movie_link: str
    caption: str

class MovieResponse(BaseModel):
    id: int
    movie_code: str
    movie_link: str
    caption: str

class MovieCodesResponse(BaseModel):
    movie_codes: List[str]
    message: Optional[str] = None

# Xatolik xabarlari
MOVIE_NOT_FOUND = "Bunday kino topilmadi."
MOVIE_ADDED = "Kino muvaffaqiyatli qo'shildi!"
NO_MOVIES = "Hozircha kinolar ro'yxati bo'sh"

@router.post(
    "/movies",
    status_code=status.HTTP_201_CREATED,
    summary="Yangi kino qo'shish (6 xonali kod avtomatik)"
)
async def create_movie(movie: MovieCreate):
    try:
        movie_code = movie_model.insert_movie(
            movie.movie_link,
            movie.caption
        )
        return {
            "message": "Kino muvaffaqiyatli qo'shildi",
            "movie_code": movie_code  # Masalan: "123456"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Kino qo'shishda xatolik: {str(e)}"
        )

@router.get(
    "/movies/all_codes",
    response_model=MovieCodesResponse,
    summary="Barcha kinolar kodlarini olish"
)
async def get_all_movies_codes():
    """
    Bazadagi barcha kinolarning kodlarini qaytaradi.
    Agar kinolar bo'lmasa, bo'sh ro'yxat qaytadi.
    """
    try:
        codes = movie_model.get_all_movies_codes()
        return MovieCodesResponse(
            movie_codes=codes,
            message=NO_MOVIES if not codes else None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server ichki xatosi: {str(e)}"
        )

@router.get(
    "/movies",
    response_model=List[MovieResponse],
    summary="Barcha kinolarni olish"
)
async def get_all_movies():
    """
    Bazadagi barcha kinolarni to'liq ma'lumotlari bilan qaytaradi.
    """
    return movie_model.get_all_movies()

@router.get(
    "/movies/{code}",
    response_model=MovieResponse,
    responses={404: {"description": MOVIE_NOT_FOUND}},
    summary="Kod bo'yicha kino ma'lumotlarini olish"
)
async def get_movie(code: str):
    """
    Berilgan kodga mos kino ma'lumotlarini qaytaradi.
    
    Parameters:
    - code: Qidirilayotgan kinoning kodi
    """
    movie = movie_model.get_movie_by_code(code)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=MOVIE_NOT_FOUND
        )
    return movie