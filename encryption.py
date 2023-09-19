from cryptography.fernet import Fernet

def encrypt_key(key: str, encryption_key: str) -> str:
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.encrypt(key.encode()).decode()

def decrypt_key(encrypted_key: str, encryption_key: str) -> str:
    cipher_suite = Fernet(encryption_key)
    return cipher_suite.decrypt(encrypted_key.encode()).decode()
