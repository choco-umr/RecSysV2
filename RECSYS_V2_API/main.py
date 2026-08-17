from Database.db import init_db
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routes.UserRoutes import UserRouter
from Routes.TestingRoutes import TestingRouter
from Routes.GlobalRoutes import GlobalRouter
from Routes.ResearcherRoutes import ResearcherRouter
from Routes.AdminRoutes import AdminRouter
from Routes.FrontendHelperRoutes import FrontendHelperRouter
import logging
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s() - '%(message)s'",
    force=True)


#initialise the db on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(GlobalRouter, prefix="/api", tags=["Global"])
app.include_router(UserRouter, prefix="/api", tags=["Users"])
app.include_router(ResearcherRouter, prefix="/api", tags=["Researchers"])
app.include_router(AdminRouter, prefix="/api", tags=["Admin"])
app.include_router(TestingRouter, prefix="/api", tags=["Testing"])
app.include_router(FrontendHelperRouter, prefix="/api", tags=["FrontendHelper"])



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    messages = [
        f"{error['loc'][-1]}: {error['msg']}"
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"success": False, "errors": messages}
    )
