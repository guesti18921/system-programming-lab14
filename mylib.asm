section .data
    ; Ключ для XOR-шифрования
    encryption_key db 0x5A

section .text
    ; Экспортируем функцию для вызова из Python
    global asm_encrypt

; asm_encrypt(char* data, int length)
; RDI — адрес буфера
; RSI — длина буфера
asm_encrypt:
    ; При нулевой или отрицательной длине завершаем работу
    cmp rsi, 0
    jle .done

    ; RCX — индекс обрабатываемого байта
    xor rcx, rcx

.loop:
    ; RIP-относительная адресация для позиционно-независимого кода
    mov al, [rel encryption_key]

    ; Изменяем текущий байт буфера операцией XOR
    xor byte [rdi + rcx], al

    ; Переходим к следующему байту
    inc rcx
    cmp rcx, rsi
    jl .loop

.done:
    ret