from Database.db import init_db
from contextlib import asynccontextmanager
from fastapi import FastAPI
from Routes.UserRoutes import UserRouter
from Routes.TestingRoutes import TestingRouter
from Routes.GlobalRoutes import GlobalRouter
from Routes.ResearcherRoutes import ResearcherRouter
from Routes.AdminRoutes import AdminRouter

#initialise the db on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(GlobalRouter, prefix="/api", tags=["Global"])
app.include_router(UserRouter, prefix="/api", tags=["Users"])
app.include_router(ResearcherRouter, prefix="/api", tags=["Researchers"])
app.include_router(AdminRouter, prefix="/api", tags=["Admin"])
app.include_router(TestingRouter, prefix="/api", tags=["Testing"])