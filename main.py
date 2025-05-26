from fastapi import FastAPI
from models.user import create_users_table
from models.movies import create_movies_table
from models.channels import create_channels_table
from routes import user as user_routes
from routes import movies as movie_routes
from routes import channels as channel_routes
from routes import advert

app = FastAPI()

create_users_table()
create_movies_table()
create_channels_table()


app.include_router(user_routes.router)
app.include_router(movie_routes.router)
app.include_router(channel_routes.router)
app.include_router(advert.router)
