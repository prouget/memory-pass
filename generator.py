import string
import random

signe = '/?#><!-'

def pw_gen(size = 8, chars=string.ascii_letters + string.digits + signe):    #+ string.punctuation
    p = ''.join(random.choice(chars) for c in range(size))
    return p
