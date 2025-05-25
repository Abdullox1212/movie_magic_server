import os
import requests
from models.user import get_active_users

TELEGRAM_BOT_TOKEN = "7219600368:AAFXrydsxc_29P9C35OVNLovAjr0seDi2sI"

def send_advert_with_photo_file(photo_path: str, caption: str):
    """
    Lokal fayldan rasm yuborish
    
    Args:
        photo_path: Rasm faylining lokal joylashuvi (masalan: "images/reklama.jpg")
        caption: Rasmga izoh
    """
    if not os.path.exists(photo_path):
        raise ValueError("Rasm fayli topilmadi")
    
    active_users = get_active_users()
    success_count = 0
    
    for user_id in active_users:
        try:
            with open(photo_path, 'rb') as photo_file:
                response = requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
                    data={
                        'chat_id': user_id,
                        'caption': caption
                    },
                    files={
                        'photo': photo_file
                    }
                )
                if response.status_code == 200:
                    success_count += 1
        except Exception as e:
            print(f"Xatolik {user_id} ga yuborishda: {str(e)}")
    
    return {
        "total_users": len(active_users),
        "success": success_count,
        "failed": len(active_users) - success_count
    }