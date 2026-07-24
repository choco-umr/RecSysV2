from argon2 import PasswordHasher
from config import MEMORY_COST, TIME_COST, PARALLELISM, SECRET_KEY, ALGORITHM, EXPIRY_TIME
import uuid
import jwt
import datetime
from sqlalchemy import select
from Database.models import Users, Researchers, Admins
from fastapi import HTTPException
from .exceptions import *
ph = PasswordHasher(memory_cost=int(MEMORY_COST),time_cost=int(TIME_COST),parallelism=int(PARALLELISM)) #according to owasp cheat sheet https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
from fastapi import UploadFile

def hash_password(plain_text_password):
    hashed_password = ph.hash(plain_text_password) #by default uses argon2id
    return hashed_password

def verify_password(hashed_password, plain_text_password):
    try:
        ph.verify(hashed_password, plain_text_password)
        return True
    except Exception:
        return False

def create_jwt_token(USER_ID):
    JWT_EXPIRY_TIME = datetime.datetime.now() + datetime.timedelta(minutes=int(EXPIRY_TIME))
    encoded = jwt.encode({"USER_ID": USER_ID, "exp": JWT_EXPIRY_TIME}, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


#verifies JWT Token and returns table name from where user is found
def RBAC(request, db):

    #hecking for valid JWT
    token = request.cookies.get("access_token")
    if not token:
            raise JWTNotFound()
    
    try:
        result = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = result["USER_ID"]

        for table in (Users, Researchers, Admins):
            exists_flag = db.execute(
                select(
                    select(table)
                    .where(table.USER_ID == user_id)
                    .exists()
                )
            ).scalar()
            #return table name where user is found
            if exists_flag:
                return table.__name__

        raise UserNotFound()
    
    #to accept the many possible PyJWT jwt exceptions here - https://pyjwt.readthedocs.io/en/stable/api.html hence no specific HTTPexception
    except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )


def check_existing_jwt_token(request):
     #checking if user is already logged in
    token = request.cookies.get("access_token")
    if token:
            raise JWTFound()
    

def logout_delete_all_cookies(response):
    response.delete_cookie(key="access_token")

def generate_userid():
    id = uuid.uuid4()
    return id


def FileValidator(file: UploadFile,max_size_bytes: int = 2 * 1024 * 1024 * 1024) -> None: #2gb
    
    if not file.filename:
        raise HTTPException(
            status_code=422,
            detail="Filename is required."
        )

    if not file.filename.lower().endswith(".csv"):
        raise InvalidFiletype()

    file.file.seek(0, 2)  # move to end
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > max_size_bytes:
        raise InvalidFilesize()