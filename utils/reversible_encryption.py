from cryptography.fernet import Fernet

# Генерация ключа (сохраните его!)
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_text(text: str) -> bytes:
    """Шифрует строку в байты."""
    return cipher.encrypt(text.encode())

def decrypt_text(encrypted_data: bytes) -> str:
    """Расшифровывает байты в строку."""
    return cipher.decrypt(encrypted_data).decode()