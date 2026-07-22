from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
#from Security.security import verify_jwt_token
from Database.db import get_db

TestingRouter = APIRouter(prefix='/TestingRoutes')

# @TestingRouter.post("/user_jwt_data_test")
# async def test_jwt_user_relative_data(request: Request, db: Session = Depends(get_db)):
#     token = request.cookies.get("access_token")
#     decode_token = verify_jwt_token(token, db)
#     return decode_token
    
#     #generate s jwt token wiht the users UserID and UserType
#     #redirect to relevant dashboard function

#commented out testing will happen later