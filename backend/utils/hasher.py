import hashlib, base64


def hash_string(username):
    salted = username+"salt"
    hash = hashlib.md5(salted.encode('UTF-8')).digest()
    participant_code = base64.urlsafe_b64encode(hash).decode('ascii')
    return participant_code[:-2]
