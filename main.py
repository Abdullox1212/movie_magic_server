from fastapi import FastAPI
from models.user import create_users_table
from models.movies import create_movies_table
from models.channels import create_channels_table
from routes import user as user_routes
from routes import movies as movie_routes
from routes import channels as channel_routes
from routes import advert
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Yoki ['*'] - barcha uchun
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_users_table()
create_movies_table()
create_channels_table()


app.include_router(user_routes.router)
app.include_router(movie_routes.router)
app.include_router(channel_routes.router)
app.include_router(advert.router)
