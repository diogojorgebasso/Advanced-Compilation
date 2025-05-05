extern printf, atoi

section .data

fmt : db "%d\n", 0
hello: db "hello world", 10, "%d", 10, "%d", 0
x : dd 42   

global main

section .text

main:
push rbp         ; base pointer

mov rbx, [rsi+8] ; offset de 8 bytes.
mov rdi, rbx
call atoi
mov [x], rax

xor rax,rax     ; zera o registrador rax
mov rdi, hello  ; rdi = hello
mov rsi, [x]
add rsi, 5
call printf 

pop rbp
ret 