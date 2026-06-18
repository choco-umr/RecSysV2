from argon2 import PasswordHasher
from config import MEMORY_COST, TIME_COST, PARALLELISM, SECRET_KEY, ALGORITHM, EXPIRY_TIME
import uuid
import jwt
import datetime
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

    ph.verify(hashed_password, plain_text_password)

def generate_userid():
    id = uuid.uuid4()
    return id
#id dupe verification

def create_jwt_token(USER_ID, USER_TYPE):
    JWT_EXPIRY_TIME = datetime.datetime.now() + datetime.timedelta(minutes=int(EXPIRY_TIME))
    encoded = jwt.encode({"USER_ID": USER_ID, "USER_TYPE": USER_TYPE, "exp": JWT_EXPIRY_TIME}, SECRET_KEY, ALGORITHM)
    return encoded

def verify_jwt_token(jwt_key):
    #expiry time logic here
    result = jwt.decode(jwt_key, SECRET_KEY, algorithms=ALGORITHM)
    print(result)
    return result


#try to undrstand the jwt secret key algorthm log cna bi beter eveyrhting else we know payload how to create decode extract data from it etc