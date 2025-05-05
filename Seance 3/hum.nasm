extern printf

section .data

hello: db 'h', 'e', "llo world", 10, "%d", 10, "%d", 0
x : dd 42   

global main

section .text

main:
push rbp        ; base pointer
xor rax,rax     ; zera o registrador rax
mov rdi, hello  ; rdi = hello
mov rcx, 5

mov rsi, [x]
add rsi, 5

call printf 
pop rbp
ret 