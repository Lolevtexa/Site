import random, string

def generate_temp_username(length=8):
    return "user_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_temp_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return "".join(random.choices(chars, k=length))
