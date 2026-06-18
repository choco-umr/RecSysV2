from Database.db import init_db
from contextlib import asynccontextmanager
from fastapi import FastAPI
from Routes.UserRoutes import UserRouter


#initialise the db on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(UserRouter, prefix="/api")



