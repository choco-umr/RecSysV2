import logging
import os
import sys

_this_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_this_dir)
for _path in (_project_root, _this_dir):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from Database.db import init_db

from Routes.UserRoutes import user_router as user_router
from Routes.GlobalRoutes import global_router as global_router
from Routes.ResearcherRoutes import researcher_router as researcher_router
from Routes.AdminRoutes import admin_router as admin_router
from Routes.FrontendHelperRoutes import frontend_helper_router as frontend_helper_router

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s() - '%(message)s'",
    force=True)


# initialise the db on startup
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
app.include_router(global_router, prefix="/api", tags=["Global"])
app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(researcher_router, prefix="/api", tags=["Researchers"])
app.include_router(admin_router, prefix="/api", tags=["Admin"])
app.include_router(frontend_helper_router, prefix="/api", tags=["FrontendHelper"])


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