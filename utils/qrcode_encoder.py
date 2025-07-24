import qrcode
from PIL import Image

def encrypt_string_to_qr(data: str, output_file: str = "qr_code.png"):
    """
    Генерирует QR-код из строки и сохраняет его в файл.

    :param data: Строка для шифрования в QR-код.
    :param output_file: Имя файла для сохранения QR-кода (по умолчанию "qr_code.png").
    """
    # Создаем объект QRCode
    qr = qrcode.QRCode(
        version=1,  # Уровень масштабирования (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Уровень коррекции ошибок (L, M, Q, H)
        box_size=10,  # Размер каждого "бокса" в пикселях
        border=4,     # Толщина белой рамки (в боксах)
    )
    
    # Добавляем данные
    qr.add_data(data)
    qr.make(fit=True)
    
    # Создаем изображение QR-кода
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Сохраняем в файл
    img.save(output_file)
    print(f"QR-код сохранен в {output_file}")