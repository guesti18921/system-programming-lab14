import ctypes
import os

# Явная загрузка библиотеки
lib_path = os.path.abspath("./libmylib.so")

print(f"[ПРОГРАММА] Загружаем внешнюю ассемблерную библиотеку: {lib_path}")

try:
    my_asm_lib = ctypes.CDLL(lib_path)
except OSError as e:
    print(f"[КРИТИЧЕСКАЯ ОШИБКА]: Не удалось загрузить .so. Проверьте пути. Данные: {e}")
    exit(1)

print("[УСПЕХ] Библиотека спроецирована в память процесса.")

# Подготавливаем изменяемый буфер байтов
secret_data = "System Programming 2026"
binary_buffer = bytearray(secret_data.encode('utf-8'))
buffer_len = len(binary_buffer)

# Получаем указатель на буфер
c_buffer = (ctypes.c_char * buffer_len).from_buffer(binary_buffer)

print(f"\nИсходная строка в памяти: '{secret_data}'")
print(f"Сырые байты до обработки:  {list(binary_buffer)}")

# Первый вызов — шифрование
print("\n[ПРОЦЕССОР] Передаем управление в libmylib.so -> функция asm_encrypt...")
my_asm_lib.asm_encrypt(c_buffer, buffer_len)

print(f"Сырые байты после шифрования (XOR): {list(binary_buffer)}")
print(f"Зашифрованная строка в консоли:     '{binary_buffer.decode('utf-8', errors='ignore')}'")

# Повторный XOR восстанавливает данные
print("\n[ПРОЦЕССОР] Повторный вызов asm_encrypt для расшифровки...")
my_asm_lib.asm_encrypt(c_buffer, buffer_len)

print(f"Байты после повторного XOR:         {list(binary_buffer)}")
print(f"Восстановленная строка:            '{binary_buffer.decode('utf-8')}'")