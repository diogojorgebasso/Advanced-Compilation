extern printf, atoi

section .data

x : dq 0
y : dq 0

argv : dq 0
fmt_init: db "%d", 10, 0

global main
section .text

main:
push rbp
mov [argv], rsi


mov rbx, [argv]
mov rdi, [rbx + 8]
call atoi
mov [x], rax
mov rbx, [argv]
mov rdi, [rbx + 16]
call atoi
mov [y], rax

loop0:
    mov rax, [x]
    cmp rax, 0
    jz end0
    
        mov rax, [x]
        push rax
        mov rax, 1
        mov rbx, rax
        sub rax, rbx
        
mov [x], rax; 

        mov rax, [y]
        push rax
        mov rax, 1
        mov rbx, rax
        add rax, rbx
        
mov [y], rax
jmp loop0
    end0:
        nop
        
mov rax, [y]

mov rdi, fmt_init
mov rsi, rax
xor rax, rax
call printf

pop rbp 
ret
