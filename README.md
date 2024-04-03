
# what is this compiler?

This compiler compiles a crappy coding language to assembly code. It’s called crapcode because it only supports variables and print statements. However this makes for good compilers as it’s so simple.

# How does it work?

It starts by opening the file and reading its contents. Next it formats it using the `format()` function. This formatting puts variables at the start and removes unwanted lines (comments and empty lines). Next the code gets tokenized in the `tokenize()` function where each variable gets put in a token which stores `name`, `type`, and `value`. These tokens make generating assembly much easier as it’s a lot easier to work with. Lastly in the `generate()` function assembly code is generated and written to the output file.

## class reference

### Token

the token class is used to orginize code into a more manageable form. instead of storing it as a string, tokens are better because it takes less work to get data from them.

### Token(self, name: str, type: str, value)

```python
newToken = Token(
  name,
  type,
  value
)
```

| Parameter | Description |
| :-------- |:------------|
| name(`str`) | a name for the token, used for variable names and function names|
| type(`str`) | a general type so the generate function can determine what type of line its generating|
| value(`any`) | a value for token, used for variable values and function parameters|

## crapcode

### how to use the compiler

its very simple. inside `main.py` there is a class called `config`

```python
class config:
  entrypoint = "main"
  extension = "cr"
  debug_mode = False
```
#### entrypoint
```python
config.entrypoint #str (default: "main")
```
entrypoint is the name of the file it will read

#### extension
```python
config.extension #str (default: "cr")
```

this is the extension it reads. so if there is no file with the proper name and extension it will return an error.

#### debug_mode
```python
config.debug_mode #bool (default: False)
```

this is a little mode to print out some of the tables to make sure the compiler is reading files correctly

### how to write crapcode

crapcode is really crappy, so alot of things you are used to in code wont work. no \n's!

a variable in crapcode may look like
```crystal
var A = "Hello World!"
```

likewise you can print it by doing
```js
print(A)
```

the full script looking like
```crystal
var A = "Hello World!" 
#this is how you comment

print(A)
```

## assembly output

this outputs to a .asm file (x86 assembly code), this file will have the same name as the entrypoint. so if your original file is `main.cr` then the output will be `main.asm`. 

### how does assembly code print?

when you write `print(A)` in crapcode and compile it, there is a preset thing it outputs

```assembly
  mov rax, 1
  mov rdi, 1
  mov rsi, <var name>
  mov rdx, <var len>
  syscall
```

`mov` transfers a value into a register, the `rax`, `rsi` are registers. `rax` represents the command 1:`sys_write`, `rdi` represents the file mode 1:`stdout`, and `rsi` is our content to print.

so when you write
```crystal
print(A)
```
it converts to a token
```python
print = Token(
  name= "print",
  type= "function",
  value= [A, Atoken]
)
```
which is then converted to assembly code

```assembly
section .text
  global _start

_start:
  mov rax, 1
  mov rdi, 1
  mov rsi, "Hello!"
  mov rdx, 6
  syscall
```
so why doesnt this work?

first of all there is no exit case, which is written as

```assembly
_start:
  mov rax, 60
  mov rdi, 0
  syscall
```

also we need to put our variable in. this is done through the .data section

```assembly
section .data
  varname: db "Hello World!", 10
```

for clarification the `, 10` at the end acts as a `\n`

all together we have some crapcode written as...
```crystal
var A = "Hello World!"

print(A)
```

that then converts to
```python
list_of_tokens = [
  [ #variables
    VarA = Token(
      name='A',
      type='variable',
      value="\"Hello World\""
    )
  ],
  [ #code
    printstmt = Token(
      name='print',
      type='function',
      value=['A', VarA]
    )
  ]
]
```
that lastly generates this assembly code
```assembly
section .data
  A: db "Hello World!", 10

section .text
  global _start
_start:
  mov rax, 1
  mov rdi, 1
  mov rsi, A
  mov rdx, 12
  syscall

  mov rax, 60
  mov rdi, 0
  syscall
```

if you have any other comments or questions post them in the comments for this repl, i will try my best to answer.

if you are on github refer to this repl at (https://replit.com/@sdcsdc0220/Crapcode-compiler?v=1)
if you wish to test your code try this assembly code compiler (https://www.mycompiler.io/new/asm-x86_64)
