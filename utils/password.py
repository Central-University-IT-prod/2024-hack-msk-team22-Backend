import bcrypt
from string import ascii_letters

def encode(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(user_password: str, password: bytes) -> bool:
    return bcrypt.checkpw(user_password.encode('utf-8'), password)


def isOnlyEng(uP):
    c = 0
    symbs = ascii_letters + '0123456789'
    for el in uP:
        if el in symbs:
            c += 1
            
    if c == len(uP):
        return True
    else:
        return False

