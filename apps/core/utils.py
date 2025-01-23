import bcrypt

def encrypt(password):

    salt = bcrypt.gensalt()

    encrypted_password = bcrypt.hashpw(password.encode('utf-8'),salt)
    return encrypted_password.decode('utf-8')