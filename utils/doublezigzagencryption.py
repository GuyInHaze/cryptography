import random

class DoubleZigzagCipher:
    def __init__(self, secret_key: str = None):
        """
        Инициализация шифра с секретным ключом.
        Если ключ не указан, генерируется случайный.
        """
        self.key = secret_key or self._generate_random_key()
        
    def _generate_random_key(self) -> str:
        """Генерирует случайный ключ из 32 символов"""
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()') for _ in range(32))
    
    def _zigzag_shuffle(self, text: str, direction: int) -> str:
        """Зигзагообразное перемешивание символов"""
        if len(text) <= 1:
            return text
            
        result = []
        left, right = 0, len(text) - 1
        
        while left <= right:
            if direction > 0:
                # Прямой зигзаг: сначала левый, потом правый символ
                if left <= right:
                    result.append(text[left])
                if left != right:
                    result.append(text[right])
            else:
                # Обратный зигзаг: сначала правый, потом левый символ
                if left <= right:
                    result.append(text[right])
                if left != right:
                    result.append(text[left])
            left += 1
            right -= 1
        
        return ''.join(result)
    
    def _xor_transform(self, text: str, key_part: str) -> str:
        """Применяет XOR преобразование с частью ключа"""
        key_cycle = (key_part * (len(text) // len(key_part) + 1))[:len(text)]
        return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(text, key_cycle))
    
    def _bit_permutation(self, text: str) -> str:
        """Выполняет обратимую битовую перестановку"""
        result = []
        for char in text:
            # Разделяем байт на две 4-битные части и меняем их местами
            byte = ord(char)
            high, low = (byte >> 4) & 0x0F, byte & 0x0F
            # Инвертируем младшие 2 бита в каждой части
            high = (high & 0b1100) | ((~high) & 0b0011)
            low = (low & 0b1100) | ((~low) & 0b0011)
            # Собираем обратно
            result.append(chr((low << 4) | high))
        return ''.join(result)
    
    def encrypt(self, plaintext: str) -> str:
        """Шифрует текст"""
        if not plaintext:
            return plaintext
            
        # Этап 1: XOR с первой половиной ключа
        stage1 = self._xor_transform(plaintext, self.key[:len(self.key)//2])
        
        # Этап 2: Прямое зигзагообразное перемешивание
        stage2 = self._zigzag_shuffle(stage1, 1)
        
        # Этап 3: Битовая перестановка
        stage3 = self._bit_permutation(stage2)
        
        # Этап 4: XOR со второй половиной ключа
        stage4 = self._xor_transform(stage3, self.key[len(self.key)//2:])
        
        # Этап 5: Обратное зигзагообразное перемешивание
        stage5 = self._zigzag_shuffle(stage4, -1)
        
        return stage5
    
    def decrypt(self, ciphertext: str) -> str:
        """Дешифрует текст"""
        if not ciphertext:
            return ciphertext
            
        # Обратный этап 5: Прямое зигзагообразное перемешивание
        stage5 = self._zigzag_shuffle(ciphertext, 1)
        
        # Обратный этап 4: XOR со второй половиной ключа
        stage4 = self._xor_transform(stage5, self.key[len(self.key)//2:])
        
        # Обратный этап 3: Битовая перестановка (обратима сама себе)
        stage3 = self._bit_permutation(stage4)
        
        # Обратный этап 2: Обратное зигзагообразное перемешивание
        stage2 = self._zigzag_shuffle(stage3, -1)
        
        # Обратный этап 1: XOR с первой половиной ключа
        stage1 = self._xor_transform(stage2, self.key[:len(self.key)//2])
        
        return stage1
    
    def encrypt_to_file(self, plaintext: str, file_path: str) -> None:
        """Шифрует текст и сохраняет в файл"""
        encrypted = self.encrypt(plaintext)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(encrypted)
    
    def decrypt_from_file(self, file_path: str) -> str:
        """Читает и дешифрует данные из файла"""
        with open(file_path, 'r', encoding='utf-8') as f:
            encrypted = f.read()
        return self.decrypt(encrypted)