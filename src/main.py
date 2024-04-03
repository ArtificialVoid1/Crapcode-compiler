
class config:
  entrypoint = "main"
  extension = "cr"
  debug_mode = False


class Token:
  def __init__(self, name: str, type: str, value):
    self.name = name
    self.type = type
    self.value = value
  def __eq__(self, other):
    if other.__class__ == Token:
      return self.name == other.name
  def __str__(self):
    return f"Token(name: {self.name},\n type: {self.type},\nvalue: {self.value}\n)"

def format(code: list[str]):
  variables = []
  codefinal = []

  for line in code:
    if line == '' or line.startswith('#'):
      continue
    elif line.startswith("var"):
      variables.append(line)
    else:
      codefinal.append(line)
      
  return [variables, code]

def tokenize(codeTable):
  if config.debug_mode == True:
    print(codeTable)
  vars = []
  code = []
  #variables
  for line in codeTable[0]:
    words = line.split(' ')
    for word in words:
      if word == '':
        words.remove(word)
    # var, name, =, value
    finalstr = ''
    if words[3].startswith('\"') or words[3].startswith('\''):
      for word in range(3, len(words)):
        finalstr += words[word] + ' '
    newtoken = Token(words[1], 'variable', finalstr)
    vars.append(newtoken)
  #code
  for line in codeTable[1]:

    if line.startswith('print'):
      parameter = line.split('(')[1].split(')')[0]
      newtoken = Token('print', 'function', [parameter, vars[vars.index(Token(parameter, 'variable', ''))]])
      code.append(newtoken)

  return [vars, code]
    
    

def generate(tokenized_code):
  code = "section .data \n"

  if config.debug_mode == True:
    print(tokenized_code)

  for token in tokenized_code[0]:
    code += f"  {token.name}: db {token.value}, 10\n"

  code += "section .text \n  global _start \n_start: \n"

  for token in tokenized_code[1]:
    if token.name == 'print':
      tokenlen = len(token.value[1].value.replace('\"', '').replace('\'', ''))
      code += f"  mov rax, 1 \n  mov rdi, 1 \n  mov rsi, {token.value[0]} \n  mov rdx, {tokenlen} \n  syscall \n"

  code += "  mov rax, 60 \n  mov rdi, 0 \n  syscall"

  return code

#open input file
file = open(config.entrypoint + "." + config.extension, "r").read().split("\n")

#format code
formatted_code = format(file)

#tokenize code
tokenized_code = tokenize(formatted_code)

#generate assembly
generated_code = generate(tokenized_code)
#create new file for output
output_file = open(config.entrypoint + ".asm", "w")
#write generated code to file
output_file.write(generated_code)
