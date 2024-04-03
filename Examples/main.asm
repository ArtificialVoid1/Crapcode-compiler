;this is what main.cr compiles to

section .data 
  greet: db "hello!" , 10
  name: db "my name is shane" , 10
  math: db "1 + 1 = 2!" , 10
  questionpt1: db "what do " , 10
  questionpt2: db "you like?" , 10
section .text 
  global _start 
_start: 
  mov rax, 1 
  mov rdi, 1 
  mov rsi, greet 
  mov rdx, 7 
  syscall 
  mov rax, 1 
  mov rdi, 1 
  mov rsi, name 
  mov rdx, 17 
  syscall 
  mov rax, 1 
  mov rdi, 1 
  mov rsi, math 
  mov rdx, 11 
  syscall 
  mov rax, 1 
  mov rdi, 1 
  mov rsi, questionpt1 
  mov rdx, 9 
  syscall 
  mov rax, 1 
  mov rdi, 1 
  mov rsi, questionpt2 
  mov rdx, 10 
  syscall 
  mov rax, 60 
  mov rdi, 0 
  syscall
