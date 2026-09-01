import datetime
import uuid

import jwt
from argon2 import PasswordHasher
from fastapi import HTTPException, UploadFile
from sqlalchemy import select

from Database.models import Users, Researchers, Admins

from .exceptions import *

from config import memory_cost, time_cost, parallelism, secret_key, algorithm, expiry_time, max_file_size

ph = PasswordHasher(memory_cost=int(memory_cost), time_cost=int(time_cost), parallelism=int(parallelism))


def hash_password(plain_text_password):
    hashed_password = ph.hash(plain_text_password)
    return hashed_password


def verify_password(hashed_password, plain_text_password):
    try:
        ph.verify(hashed_password, plain_text_password)
        return True
    except Exception:
        return False


def create_jwt_token(user_id):
    jwt_expiry_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=int(expiry_time))
    encoded = jwt.encode({"USER_ID": user_id, "exp": jwt_expiry_time}, secret_key, algorithm=algorithm)
    return encoded


def RBAC(request, db):
    token = request.cookies.get("access_token")
    if not token:
        raise jwt_not_found()
    try:
        result = jwt.decode(token, secret_key, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        raise expired_jwt()
    except jwt.PyJWTError:
        raise invalid_jwt()
    user_id = result["USER_ID"]
    for table in (Users, Researchers, Admins):
        exists_flag = db.execute(
            select(
                select(table)
                .where(table.USER_ID == user_id)
                .exists()
            )
        ).scalar()
        if exists_flag:
            return {
                "role": table.__name__,
                "user_id": user_id,
            }
    raise user_not_found()


def check_existing_jwt_token(request):
    token = request.cookies.get("access_token")
    if not token:
        return
    try:
        jwt.decode(token, secret_key, algorithms=[algorithm])
    except jwt.PyJWTError:
        return
    raise jwt_found()


def logout_delete_all_cookies(response):
    response.delete_cookie(key="access_token")


def generate_user_id():
    id = uuid.uuid4()
    return id


def generate_interaction_id():
    id = uuid.uuid4()
    return id


def file_validator(file: UploadFile) -> None:  # 2gb
    # filename check
    if not file.filename:
        raise filename_required()

    if not file.filename.lower().endswith(".csv"):
        raise invalid_file_type()

    file.file.seek(0, 2)  # move to end
    file_size = file.file.tell()
    file.file.seek(0)
    print("current file size: ", file_size)
    print("MAX_FILE_SIZE", max_file_size)
    if file_size > int(max_file_size):
        raise invalid_file_size()


# NOTES
"""
- hash_password: uses argon2id by default
- RBAC: returns the table name (role) where the user_id is found
- check_existing_jwt_token: an expired/malformed/invalid token is treated the same as not being logged in, rather than blocking a fresh login
- FileValidator: max file size is 2GB
- Reference: OWASP Password Storage Cheat Sheet (argon2 params) — https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- Reference: OWASP JWT security cheat sheet for password hashing — https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
"""