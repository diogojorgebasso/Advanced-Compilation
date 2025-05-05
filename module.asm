extern printf, atoi

section .data

DECL_VARS
argv : dq 0
fmt_init: db "%d", 10, 0

global main
section .text

main:
push rbp
mov [argv], rsi

INIT_VARS
COMMANDE
RETOUR

mov rdi, fmt_init
mov rsi, rax
xor rax, rax
call printf

pop rbp 
ret