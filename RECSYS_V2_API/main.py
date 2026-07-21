from Database.db import init_db
from contextlib import asynccontextmanager
from fastapi import FastAPI
from Routes.UserRoutes import UserRouter
from Routes.TestingRoutes import TestingRouter
from Routes.GlobalRoutes import GlobalRouter


#initialise the db on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(UserRouter, prefix="/api", tags=["Users"])
app.include_router(TestingRouter, prefix="/api", tags=["Testing"])
app.include_router(GlobalRouter, prefix="/api", tags=["Global"])