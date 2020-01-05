import string
import random

signe = '/?#><!-'

def pw_gen(size = 8, chars=string.ascii_letters + string.digits + signe):
    p = ''.join(random.choice(chars) for c in range(size))
    return p

def pw_gen_num(size = 8, chars=string.digits):
    p = ''.join(random.choice(chars) for c in range(size))
    return p
