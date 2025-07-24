import sys
from typing import Callable
sys.path.append('C:/Users/nick/Desktop/cryptography/utils')

from utils.doublezigzagencryption import DoubleZigzagCipher
from utils.encode_into_image_and_decode import encrypt_text_to_image, decrypt_text_from_image
from utils.irreversible_encryption import hash_string
from utils.qrcode_encoder import encrypt_string_to_qr
from utils.qrcode_decoder import decrypt_qr_to_string
from utils.reversible_encryption import encrypt_text, decrypt_text

class CryptoUtils:
    hash_string = staticmethod(hash_string)
    image_encrypt = staticmethod(encrypt_text_to_image)
    image_decrypt = staticmethod(decrypt_text_from_image)
    qr_encode = staticmethod(encrypt_string_to_qr)
    qr_decode = staticmethod(decrypt_qr_to_string)
    encrypt_text = staticmethod(encrypt_text)
    decrypt_text = staticmethod(decrypt_text)


def get_input(prompt: str, validator: Callable = None):
    while True:
        try:
            value = input(prompt).strip()
            if validator and not validator(value):
                raise ValueError
            return value
        except ValueError:
            print("Некорректный ввод. Попробуйте снова.")

def hash_menu():
    print("\n Выберите алгоритм хеширования:")
    print("1. SHA-256")
    print("2. SHA-1")
    print("3. MD5")
    print("4. BLAKE2b")
    choice = get_input("Ваш выбор (1-4): ", lambda x: x in ["1", "2", "3", "4"])
    
    algorithms = {"1": "sha256", "2": "sha1", "3": "md5", "4": "blake2b"}
    text = get_input("Введите текст для хеширования: ")
    
    hashed = CryptoUtils.hash_string(text, algorithms[choice])
    print(f"\nРезультат хеширования ({algorithms[choice].upper()}):")
    print(hashed)   
     
def steganography_menu():
    action = get_input("Выберите действие (1 - скрыть текст, 2 - извлечь текст): ",
                      lambda x: x in ["1", "2"])
    
    if action == "1":
        text = get_input("Введите текст для скрытия: ")
        image_path = get_input("Введите путь к изображению: ")
        output_path = get_input("Введите путь для сохранения (по умолчанию encoded.png): ") or "encoded.png"
        try:
            CryptoUtils.image_encrypt(text, image_path, output_path)
            print(f"Текст скрыт в изображении {output_path}")
        except Exception as e:
            print("Ошибка:", str(e))
    else:
        image_path = get_input("Введите путь к изображению с скрытым текстом: ")
        try:
            text = CryptoUtils.image_decrypt(image_path)
            print("\nИзвлеченный текст:")
            print(text)
        except Exception as e:
            print("Ошибка:", str(e))

def qr_menu():
    action = get_input("Выберите действие (1 - создать QR, 2 - прочитать QR): ", 
                      lambda x: x in ["1", "2"])
    
    if action == "1":
        text = get_input("Введите текст для кодирования в QR: ")
        output = get_input("Введите имя файла для сохранения (по умолчанию qr_code.png): ") or "qr_code.png"
        CryptoUtils.qr_encode(text, output)
        print(f"QR-код сохранен как {output}")
    else:
        image_path = get_input("Введите путь к QR-коду: ")
        decoded_text = CryptoUtils.qr_decode(image_path)
        print("\nДекодированный текст:")
        print(decoded_text)

def double_zigzag_menu():
    action = get_input("Выберите действие (1 - шифрование, 2 - дешифрование): ",
                     lambda x: x in ["1", "2"])
    
    key = get_input("Введите ключ шифрования: ")
    cipher = DoubleZigzagCipher(key)
    
    if action == "1":
        text = get_input("Введите текст для шифрования: ")
        file_path = get_input("Введите путь для сохранения (по умолчанию encrypted.zz): ") or "encrypted.zz"
        cipher.encrypt_to_file(text, file_path)
        print(f"Текст успешно зашифрован и сохранён в {file_path}")
    else:
        file_path = get_input("Введите путь к зашифрованному файлу: ")
        try:
            decrypted = cipher.decrypt_from_file(file_path)
            print("\nРасшифрованный текст:")
            print(decrypted)
        except FileNotFoundError:
            print("Ошибка: файл не найден")
        except Exception as e:
            print(f"Ошибка дешифрования: {str(e)}")

def show_menu():
    print("\n Меню криптографических методов ")
    print("1. Хеширование строки (SHA-256, MD5 и др.)")
    print("2. Стеганография (скрытие текста в изображении)")
    print("3. Генерация QR-кода и его чтение")
    print("4. Шифрование методом 'Двойной зигзаг'")
    print("0. Выход")

def main():
    print(" Криптографическая программа ")
    
    while True:
        show_menu()
        choice = get_input("Выберите метод (0-4): ", 
                         lambda x: x in ["0", "1", "2", "3", "4"])
        
        if choice == "0":
            print("Выход из программы.")
            sys.exit()
        elif choice == "1":
            hash_menu()
        elif choice == "2":
            steganography_menu()
        elif choice == "3":
            qr_menu()
        elif choice == "4":
            double_zigzag_menu()
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()