from argon2 import PasswordHasher
from config import MEMORY_COST, TIME_COST, PARALLELISM
import uuid

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

