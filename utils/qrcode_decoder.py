from pyzbar.pyzbar import decode
from PIL import Image

def decrypt_qr_to_string(image_path: str) -> str:
    """Декодирует QR-код обратно в строку."""
    img = Image.open(image_path)
    decoded_data = decode(img)
    if decoded_data:
        return decoded_data[0].data.decode("utf-8")
    else:
        return "QR-код не распознан!"