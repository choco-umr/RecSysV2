from argon2 import PasswordHasher
from config import MEMORY_COST, TIME_COST, PARALLELISM, SECRET_KEY, ALGORITHM, EXPIRY_TIME
import uuid
import jwt
import datetime
from sqlalchemy import select
from Database.models import Users

ph = PasswordHasher(memory_cost=int(MEMORY_COST),time_cost=int(TIME_COST),parallelism=int(PARALLELISM)) #according to owasp cheat sheet https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

def hash_password(plain_text_password):
    hashed_password = ph.hash(plain_text_password) #by default uses argon2id
    return hashed_password

def verify_password(hashed_password, plain_text_password):
    try:
        ph.verify(hashed_password, plain_text_password)
        return True
    except Exception:
        return False

def create_jwt_token(USER_ID, USER_TYPE):
    JWT_EXPIRY_TIME = datetime.datetime.now() + datetime.timedelta(minutes=int(EXPIRY_TIME))

    encoded = jwt.encode({"USER_ID": USER_ID, "USER_TYPE": USER_TYPE, "exp": JWT_EXPIRY_TIME}, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

#veryify jwt and get role acess
def verify_jwt_token(jwt_key,db):

    try:
        result = jwt.decode(jwt_key, SECRET_KEY, algorithms=ALGORITHM)
        User_ID_extracted = result["USER_ID"]
        USER_TYPE_extracted = result["USER_TYPE"]

        UserExtract = (
        select(Users).where(Users.USER_ID == User_ID_extracted).where(Users.USER_TYPE == USER_TYPE_extracted).exists()
        )

        final_result = db.execute(select(UserExtract))
        exists_flag = final_result.scalar()

        if exists_flag:
            return USER_TYPE_extracted #either user or researcher
        else:
            #try admin table for later
            print("s")


    except jwt.ExpiredSignatureError:
        raise Exception("expired token")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

def logout_delete_all_cookies(response):
    response.delete_cookie(key="access_token")

    




def generate_userid():
    id = uuid.uuid4()
    return id
#id dupe verification


#try to undrstand the jwt secret key algorthm log cna bi beter eveyrhting else we know payload how to create decode extract data from it etc