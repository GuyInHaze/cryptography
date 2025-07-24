from PIL import Image

def encrypt_text_to_image(text: str, input_image_path: str, output_image_path: str = "encoded_image.png"):
    """
    Прячет текст в изображении (младшие биты пикселей).
    :param text: Текст для шифрования.
    :param input_image_path: Путь к исходному изображению.
    :param output_image_path: Путь для сохранения изображения с текстом.
    """
    img = Image.open(input_image_path)
    pixels = img.load()
    
    # Преобразуем текст в бинарный вид
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    binary_text += '00000000'  # Маркер конца текста (NULL-терминатор)
    
    if len(binary_text) > img.width * img.height * 3:
        raise ValueError("Текст слишком большой для изображения!")
    
    index = 0
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j][:3]  # Берем только RGB (игнорируем альфа-канал)
            
            # Меняем младшие биты
            if index < len(binary_text):
                r = (r & 0xFE) | int(binary_text[index])
                index += 1
            if index < len(binary_text):
                g = (g & 0xFE) | int(binary_text[index])
                index += 1
            if index < len(binary_text):
                b = (b & 0xFE) | int(binary_text[index])
                index += 1
            
            pixels[i, j] = (r, g, b)
            
            if index >= len(binary_text):
                break
        if index >= len(binary_text):
            break
    
    img.save(output_image_path)
    print(f"Текст скрыт в {output_image_path}")

def decrypt_text_from_image(encoded_image_path: str) -> str:
    """
    Извлекает текст из изображения.
    :param encoded_image_path: Путь к изображению с зашифрованным текстом.
    :return: Расшифрованный текст.
    """
    img = Image.open(encoded_image_path)
    pixels = img.load()
    
    binary_text = ""
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j][:3]
            
            # Извлекаем младшие биты
            binary_text += str(r & 1)
            binary_text += str(g & 1)
            binary_text += str(b & 1)
    
    # Разбиваем бинарную строку на байты
    text = ""
    for i in range(0, len(binary_text), 8):
        byte = binary_text[i:i+8]
        if byte == "00000000":  # Конец текста
            break
        text += chr(int(byte, 2))
    
    return text
