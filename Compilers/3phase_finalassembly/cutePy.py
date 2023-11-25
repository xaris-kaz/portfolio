# AM: 4778, NAME: Alkiviadis Patras, username: cse94778
# AM: 4679, NAME: Theocharis Kazakidis, username: cse94679

import sys

# The acceptable range for numbers is defined by the MAX_NUMBER constant.
MAX_NUMBER = 2**32

##this class represents token Entities 
class Token:
  def __init__(self, recognized_string, family, line_number):
    self.recognized_string = recognized_string
    self.family = family
    self.line_number = line_number

class Entity: ##This class represents program entities such as functions, variables, parameters and temp variables

  def __init__(self,name, type, offset):
    self.name=str(name)
    self.type=str(type)
    self.offset=int(offset)
    self.start_quad=0
    self.par_list=[]
    self.frame_length=0
    self.par_mode=""

  def setStart_quad(self,x):
    self.start_quad=x

  def getStart_quad(self):
    return self.start_quad

  def setPar_list(self,x):
    self.par_list=x

  def getPar_list(self):
    return self.par_list

  def setFrame_length(self,x):
    self.frame_length=x

  def getFrame_length(self):
    return self.frame_length

  def setPar_mode(self,x):
    self.par_mode=x

  def getPar_mode(self):
    return self.par_mode

class Scope:
  def __init__(self, nesting_level):
    self.entity_list=[]
    self.nesting_level=nesting_level

  def add_entity(self, e):
    self.entity_list.append(e)


# The file name is retrived from the command line arguments.

if len(sys.argv) <= 1:
    print("Try again, you have entered an incorrect command in the terminal. Please use the following format: python3 cutePy_4778_4679.py 'cutePy_file_name' ")
    sys.exit(1)
cutePy_file_name = sys.argv[1]
file = open(cutePy_file_name, 'r', encoding='utf8')


# The alphabet of the CutePy language is defined as lists.
identifier = [
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
  'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
  'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
  't', 'u', 'v', 'w', 'x', 'y', 'z', '_'
]

number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

keyword = [
  'def', 'print', 'input', '#declare', 'if', 'while', 'else', 'return', 'and',
  'or', 'not', 'int', '__name__', '__main__'
]

mulOperator = ['*', '//']

compare = ['<', '>']

relOperator = ['!=', '<=', '>=', '==']

addOperator = ['+', '-']

assignment = ['=']

delimiter = [';', ',', ':', '"']

groupSymbol_without_hashtag = ['(', ')', '[', ']']

groupSymbol_with_hashtag = ['#{', '#}', '#$']

family = [
  "Identifier", "Number", "Keyword", "MulOperator", "RelOperator",
  "AddOperator", "Assignment", "Delimiter", "GroupSymbol"
]


quads = [] ##Array that holds the quads of the intermediate code
temp_vars = [] ##Array that holds to name of the temp variables used 
quad_num = -1 
temp_num = -1

functions_list=[] ##Array that holds function enities declared in the programm
variables_list=[] ##Array that holds user declared variable enities in the programm
temp_scope=[] ##Stack that holds scopes 
final_scope=[] ##Array for all the scopes used in the programm
offset = 12
nesting = 0

asm_commands=[] ##Array that holds the contents of a .asm file
labels=[] ##Array that holds jump labels 



# Lexical Analysis 
line_number = 1

def lex():
  global line_number  # Accessing the variable 'line_number'.
  state = 0
  token = ""

  # The beginning of the 'while' loop in the 'lex' function marks the start of the tokenization process of the input file.
  while state >= 0 and state <= 6:
    char = file.read(1)  # Reading one character at a time from the input file
    token += char  # Appending the character to the token string

    # state 'Start' (state = 0)
    # This state acts like a manager, where some symbols immediately transition to a final state and return a Token object,
    # while other symbols like letters and numbers require additional checks and need to be sent to other states before reaching a final state.
    # However, all symbols are checked in the 'Start' state. If a symbol is invalid, a message is printed to indicate invalid input in the cutePy file.
    if state == 0:
      # If the character is a newline or a carriage return, increment line_number and reset token.
      if char in {'\n', '\r'}:
        line_number += 1
        token = ""

      # If the character is empty, return a token indicating end of file.
      elif char == '':
        return Token("''", 'EOF', line_number)

      # If the character is a whitespace, remove the whitespace from the token string.
      elif token.isspace():
        token = token[:-1]

      # If the token is an addition operator, return a token of type 'AddOperator'.
      elif token in addOperator:  # 'addOperator' => name of list 
        return Token(token, 'AddOperator', line_number)

      # If the token is a group symbol without a hashtag, return a token of type 'GroupSymbol'.
      elif token in groupSymbol_without_hashtag:   # 'groupSymbol_without_hashtag' => name of list 
        return Token(token, 'GroupSymbol', line_number)

      # If the token is a delimiter, return a token of type 'Delimiter'.
      elif token in delimiter:
        return Token(token, 'Delimiter', line_number)

      # If the token is a multiplication operator, return a token of type 'MulOperator'.
      # If the token is a forward slash ('/'), the lexer moves to the 'Division' state (state = 1)
      elif token in mulOperator or token == '/':
        if token == '*':
          return Token(token, 'MulOperator', line_number)
        else:
          state = 1

      # If the token is a valid identifier, move to the 'Identifier' state (state = 2)
      elif token in identifier:
        state = 2

      # If the token is a valid number, move to the 'Number' state (state = 3)
      elif token in number:
        state = 3

      # If the token is a comparison operator or an exclamation point, move to the 'Compare' state (state = 4)
      elif token in compare or token == '!':
        state = 4

      # If the token is an assignment operator, move to the 'Assignment' state (state = 5)
      elif token in assignment:
        state = 5

      # If the token is a hashtag, move to the 'Hashtag' state (state = 6)
      elif token == '#':
        state = 6

      else:
        # The code generates an error message indicating that the input contains an invalid character and prints the line number where the error occurred.
        error_message = f"Invalid input. The character you are trying to type is not recognized in CutePy. Please check your input. Line: {line_number}"
        raise ValueError(error_message)


    # state 'division' (state = 1)
    # This block of code checks if the current token is '/'.
    # If it is, the lexer reads the next character to check if it is also a forward slash '/'.
    # If it is, the lexer returns a MulOperator token
    # Otherwise, it raises a ValueError.
    if state == 1:
      if token == '/':
        next_char = file.read(1)
        if next_char == '/':
          token += next_char
          return Token(token, 'MulOperator', line_number)
        else:
          file.seek(file.tell() - 1)
          raise ValueError(
            f"Invalid input. Please ensure that you have used two forward slashes ('//') to start division. Line: {line_number}"
          )


    # state 'identifier' (state = 2)
    # This block of code checks if the current token is in identifier list or starts with '#'.
    # If it is, the lexer reads the next character and continue adding to token until a non-identifier or a non-number character is encountered.
    # If the next charachter doesn't meet conditions, lexer moves file pointer back one character. 
    # Next lexer checks if the current token is less than 30 charachters and if it is a keyword or an identifier.
    # It returns a Keyword token or an Identifier token, accordingly.
    # Otherwise, it raises an error.
    if state == 2:
      if not token in identifier and token[0] != '#':
        raise ValueError("Invalid input.")
      while True:
        next_char = file.read(1)
        if next_char in identifier or next_char in number:
          token += next_char
        else:
          file.seek(file.tell() - 1)
          if token in keyword:
            return Token(token, 'Keyword', line_number)
          else:
            if token[0] == '_' or token[0] == '#':
              raise ValueError(
                f"Invalid input. Please ensure that you have not used '#' or '_' to start an Identifier token. Line: {line_number}")
            elif len(token) > 30:
              raise ValueError(f"Invalid input. Please ensure that your input identifier falls within the acceptable range of characters. Line: {line_number}")
            else:
              return Token(token, 'Identifier', line_number)


    # state 'number' (state = 3)
    # This block of code checks if the current token is in number list.
    # If it is, lexer reads the next character and continue adding to token until non-number character is encountered.
    # If the next charachter doesn't meet conditions, lexer moves file pointer back one character.
    # Next lexer checks if the current token is a number and doesn't contains letters.
    # if the token meets the above conditions and belongs within the acceptable range for numbers, lexer returns a Number token.
    # Otherwise, it raises an error.
    if state == 3:
      if not token.isdigit():
        raise ValueError("Invalid input.") 
      while True:
        next_char = file.read(1)
        if next_char in identifier:
          raise ValueError(f"Invalid input. Please ensure that you have not used letters in a number. Line: {line_number}")
        if next_char in number:
          token += next_char
        else:
          file.seek(file.tell() - 1)
          if token.isdigit() and int(token) < MAX_NUMBER:
            return Token(token, 'Number', line_number)
          else: 
            raise ValueError(f"Invalid input. Please ensure that your input number falls within the acceptable range of digits. Line: {line_number}")


    # state 'compare' (state = 4)
    # This block of code checks if the current token is in compare list or starts with '!'.
    # If it is, the lexer reads the next character to check if it is '='.
    # if it is, lexer returns a RelOperator token  [>=, <=, !=]
    # If the next charachter isn't '=', lexer moves file pointer back one character. 
    # Next lexer checks if the current token is in compare list, it returns a RelOperator token.
    # Otherwise, it raises an error.    
    if state == 4:
      if token in compare or token == '!':
        next_char = file.read(1)
        if next_char == '=':
          token += next_char
          return Token(token, 'RelOperator', line_number)
        else:
          if token in compare:
            file.seek(file.tell() - 1)
            return Token(token, 'RelOperator', line_number)
          else:
            raise ValueError(
              f"Invalid input. Please ensure that you have used '=' to start the RelOperatot '!='. Line: {line_number}"
            )


    # state 'assignment' (state = 5)
    # This block of code checks if the current token is in assignment list.
    # If it is, the lexer reads the next character to check if it is '='.
    # if it is, lexer returns a RelOperator token  [==]
    # If the next charachter isn't '=', lexer moves file pointer back one character.
    # Next lexer checks if the current token is in assignment list, it returns an Assignment token. 
    if state == 5:
      if token in assignment:
        next_char = file.read(1)
        if next_char == '=':
          token += next_char
          return Token(token, 'RelOperator', line_number)
        else:
          file.seek(file.tell() - 1)
          return Token(token, 'Assignment', line_number)


    # state 'Hashtag' (state = 6)
    # This block of code checks if the current token is '#'.
    # If it is, the lexer reads the next character and checks if it is '{' or '}', it returns GroupSymbol token.
    # Otherwise if the next charachter is '$', lexer adds it to token and reads the next characters and continue adding to token until token ends with '#$'.
    # When lexer reads '#$', doesn't return anything and goes to state = 0 in order to ignored the comments of cutePy's file.
    # Also if lexer reads a next line charachter, it informs the variable line_number and if it reads the end of file, it rises an error. 
    # Next it checks if the current token is '#' and the next charachter is 'd', lexer goes to state 'Identifier' to check if this token is about '#declare'.
    # Otherwise, If the next charachter isn't anything of the above, it moves file pointer back one character and rises an error.
    if state == 6:
      if token == '#':
        next_char = file.read(1)
        if next_char == '{' or next_char == '}':
          token += next_char
          return Token(token, 'GroupSymbol', line_number)
        elif next_char == '$':
          token += next_char
          while True:
            next_next_char = file.read(1)
            if next_next_char == '#' and file.read(1) == '$':
              state = 0
              token = ""
              break
            if next_next_char in {'\n', '\r'}:
              line_number += 1
            if next_next_char == '':
              raise ValueError(f"Invalid input. Please ensure that you have used '#$' to close the comments. Line: {line_number}")
        elif next_char == 'd':
          token += next_char
          state = 2
        else:
          file.seek(file.tell() - 1)
          raise ValueError(f"Invalid input. Please ensure that you have not used only '#' without anything else after that. Line: {line_number}")
  # The end of the 'while' loop in the 'lex' function signals the completion of the tokenization process of the input file.

  return Token(token, 'Unknown', line_number)

# Syntax Analysis
def syntax():
  global functions_list, variables_list, temp_scope, final_scope, offset, nesting
  global line_number
  global token
  global ACCESS
  ACCESS = lex()
  line_number = ACCESS.line_number
  token = ACCESS.recognized_string

  def startRule():
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global_scope=Scope(nesting)
    temp_scope.append(global_scope)
    def_main_part(global_scope)
    call_main_part(global_scope)
    final_scope.append(global_scope)
    temp_scope.pop()

  def def_main_part(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting, quad_num
    global ACCESS
    def_main_function(scope)
    offset+=4
    while (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'def'):
      def_main_function(scope)
      offset+=4


  def def_main_function(scope): 
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global line_number 
    global token
    global ACCESS

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'def'): 
      ACCESS = lex()
      line_number = ACCESS.line_number
      if (ACCESS.family == "Identifier"):
        f_id = ACCESS.recognized_string
        gen_quad("begin_block",f_id,"_","_")
        temp_offset=offset
        main_function=Entity(f_id,"main_function",temp_offset)
        offset=12
        if exists(nesting,main_function)==True:
          raise ValueError(f"Function {f_id} already declared at this scope! Line{line_number}")
        main_function.setStart_quad(quad_num)
        functions_list.append(main_function)
        scope.add_entity(main_function)
        ACCESS = lex()
        line_number = ACCESS.line_number

        if (ACCESS.family == "GroupSymbol"
            and ACCESS.recognized_string == '('):
          ACCESS = lex()
          line_number = ACCESS.line_number

          if (ACCESS.family == "GroupSymbol"
              and ACCESS.recognized_string == ')'):
            ACCESS = lex()
            line_number = ACCESS.line_number

            if (ACCESS.family == "Delimiter"
                and ACCESS.recognized_string == ':'):
              ACCESS = lex()
              line_number = ACCESS.line_number

              if (ACCESS.family == "GroupSymbol"
                  and ACCESS.recognized_string == '#{'):
                nesting+=1
                main_function_scope=Scope(nesting)
                temp_scope.append(main_function_scope)

                ACCESS = lex()
                line_number = ACCESS.line_number
                declarations(main_function_scope)
                while (ACCESS.family == "Keyword"
                       and ACCESS.recognized_string == 'def'):
                  def_function(main_function_scope)
                statements(main_function_scope)

                if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '#}'):
                  gen_quad("end_block",f_id,"_","_")
                  frame_length=(offset-4)-12
                  offset=temp_offset
                  main_function.setFrame_length(frame_length)
                  final_scope.append(main_function_scope)
                  temp_scope.pop()
                  nesting-=1
                  ACCESS = lex()
                  line_number = ACCESS.line_number
                else:
                  raise ValueError(f"Missing the two block's closing symbols after the statements of a main function. In line: {line_number}")
              else:
                raise ValueError(f"Missing the two block's openning symbols before the declarations of a main function. In line: {line_number}")
            else:
              raise ValueError(f"Missing ':' after right and left parenthesis of a main function. In line: {line_number}")
          else:
            raise ValueError(f"Missing right parenthesis ')', not closed after the name of a main function. In line: {line_number}")
        else:
          raise ValueError(f"Missing left parenthesis '(', not opened after the name of a main function. In line: {line_number}")
      else:
         raise ValueError(f"Missing the 'name' of main function. In line: {line_number} after token: {token}")
    else:
      raise ValueError(f"Missing the keyword 'def' at the beginning of the program's block code. In line: {line_number} before token: {token}")
  
  def def_function(scope): 
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting, quad_num
    global line_number
    global token
    global ACCESS

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'def'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "Identifier"):
        f_id = ACCESS.recognized_string
        gen_quad("begin_block",f_id,"_","_")
        temp_offset=offset
        function=Entity(f_id,"function",temp_offset)
        offset=12
        if exists(nesting,function)==True:
          raise ValueError(f"Function {f_id} already declared at this scope! Line{line_number}")
        function.setStart_quad(quad_num)
        functions_list.append(function)
        scope.add_entity(function)
        ACCESS = lex()
        line_number = ACCESS.line_number

        if (ACCESS.family == "GroupSymbol"
            and ACCESS.recognized_string == '('):
          ACCESS = lex()
          line_number = ACCESS.line_number
          nesting+=1
          function_scope=Scope(nesting)
          temp_scope.append(function_scope)
          par_list=id_list("par",function_scope)
          function.setPar_list(par_list)
          if (ACCESS.family == "GroupSymbol"
              and ACCESS.recognized_string == ')'):
            ACCESS = lex()
            line_number = ACCESS.line_number

            if (ACCESS.family == "Delimiter"
                and ACCESS.recognized_string == ':'):
              ACCESS = lex()
              line_number = ACCESS.line_number

              if (ACCESS.family == "GroupSymbol"
                  and ACCESS.recognized_string == '#{'):
                ACCESS = lex()
                line_number = ACCESS.line_number

                declarations(function_scope)
                while (ACCESS.family == "Keyword"
                       and ACCESS.recognized_string == 'def'):
                  def_function(function_scope)
                statements(function_scope)

                if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '#}'):
                  gen_quad("end_block",f_id,"_","_")
                  frame_length=(offset-4)-12
                  offset=temp_offset+4
                  function.setFrame_length(frame_length)
                  final_scope.append(function_scope)
                  temp_scope.pop()
                  nesting-=1
                  ACCESS = lex()
                  line_number = ACCESS.line_number
                else:
                  raise ValueError(f"Missing the two block's closing symbols after the statements of a function. In line: {line_number}")
              else:
                raise ValueError(f"Missing the two block's openning symbols before the declarations of a function. In line: {line_number}")
            else:
              raise ValueError(f"Missing ':' after right and left parenthesis of a function. In line: {line_number}")
          else:
            raise ValueError(f"Missing right parenthesis ')', not closed after the name of a function. In line: {line_number}")
        else:
          raise ValueError(f"Missing left parenthesis '(', not opened after the name of a function. In line: {line_number}")
      else:
        raise ValueError(f"Missing the 'name' of a function. In line: {line_number} before token: {token}")
    else:
      raise ValueError(f"Missing the keyword 'def' at the beginning of the program's block code. In line: {line_number} after {token}")

  def declarations(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS

    while (ACCESS.family == "Keyword"
           and ACCESS.recognized_string == '#declare'):
      declaration_line_number(scope)

  def declaration_line_number(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == '#declare'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      id_list("decl",scope)

  def id_list(caller,scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global line_number
    global ACCESS
    pars=[]

    if caller=="decl":
      id_type="var"
    elif caller == "par":
      id_type="par" 

    if (ACCESS.family == "Identifier"):
      id=ACCESS.recognized_string
      var=Entity(id,id_type,offset)
      offset+=4
      if caller == "decl":
        variables_list.append(var)
        if exists(nesting,var)==True:
          raise ValueError(f"Variable {id} already exists in this scope {line_number}")
      if caller == "par":
        pars.append(var)
        var.setPar_mode("CV")
      scope.add_entity(var)    
      ACCESS = lex()
      line_number = ACCESS.line_number

      while (ACCESS.family == "Delimiter" and ACCESS.recognized_string == ','):
        ACCESS = lex()
        line_number = ACCESS.line_number

        if (ACCESS.family == "Identifier"):
          id=ACCESS.recognized_string
          var=Entity(id,id_type,offset)
          offset+=4
          if caller == "decl":
            variables_list.append(var)
            if exists(nesting,var)==True:
              raise ValueError(f"Variable {id} already exists in this scope {line_number}")
          if caller == "par":
            pars.append(var)
            var.setPar_mode("CV")
          scope.add_entity(var)   
          ACCESS = lex()
          line_number = ACCESS.line_number
        else:
          raise ValueError(f"Missing Identifier token after comma(','). Line: {line_number}")
      return pars  

  def statement(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global line_number
    global ACCESS

    if (ACCESS.family == "Identifier"
        or ACCESS.family == "Keyword" and ACCESS.recognized_string == 'print'
        or ACCESS.family == "Keyword"
        and ACCESS.recognized_string == 'return'):
      simple_statement(scope)
    elif (
        ACCESS.family == "Keyword" and ACCESS.recognized_string == 'if'
        or ACCESS.family == "Keyword" and ACCESS.recognized_string == 'while'):
      structured_statement(scope)
    else:
      raise ValueError(f"Invalid statement. Line: {line_number}")

  def statements(scope):
    global ACCESS

    statement(scope)
    while (
        ACCESS.family == "Identifier"
        or ACCESS.family == "Keyword" and ACCESS.recognized_string == 'print'
        or ACCESS.family == "Keyword" and ACCESS.recognized_string == 'return'
        or ACCESS.family == "Keyword" and ACCESS.recognized_string == 'if'
        or ACCESS.family == "Keyword" and ACCESS.recognized_string == 'while'):
      statement(scope)

  def simple_statement(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS

    if (ACCESS.family == "Identifier"):
      assignment_stat(scope)
    elif (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'print'):
      print_stat(scope)
    elif (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'return'):
      return_stat(scope)

  def structured_statement(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'if'):
      if_stat(scope)
    elif (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'while'):
      while_stat(scope)

  def assignment_stat(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    if (ACCESS.family == "Identifier"):
      var=ACCESS.recognized_string
      if not_exists(var)==False:
        raise ValueError(f"Trying to initialize variable {var} that was never declared. Line {line_number}")
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "Assignment" and ACCESS.recognized_string == '='):
        ACCESS = lex()
        line_number = ACCESS.line_number

        if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'int'):
          ACCESS = lex()
          line_number = ACCESS.line_number

          if (ACCESS.family == "GroupSymbol"
              and ACCESS.recognized_string == '('):
            ACCESS = lex()
            line_number = ACCESS.line_number

            if (ACCESS.family == "Keyword"
                and ACCESS.recognized_string == 'input'):
              ACCESS = lex()
              line_number = ACCESS.line_number

              if (ACCESS.family == "GroupSymbol"
                  and ACCESS.recognized_string == '('):
                ACCESS = lex()
                line_number = ACCESS.line_number

                if (ACCESS.family == "GroupSymbol"
                    and ACCESS.recognized_string == ')'):
                  ACCESS = lex()
                  line_number = ACCESS.line_number

                  if (ACCESS.family == "GroupSymbol"
                      and ACCESS.recognized_string == ')'):
                    ACCESS = lex()
                    line_number = ACCESS.line_number

                    if (ACCESS.family == "Delimiter"and ACCESS.recognized_string == ';'):
                      gen_quad("=","input","_",var)
                      ACCESS = lex()
                      line_number = ACCESS.line_number
                    else:
                      raise ValueError(f"Missing semicolon ';' in assignment statement. Line: {line_number}")
                  else:
                    raise ValueError(f"Missing right parenthesis ')', not closed in assignment statement. Line: {line_number}")
                else:
                  raise ValueError(f"Missing right parenthesis ')', not closed in assignment statement. Line: {line_number}")
              else:
                raise ValueError(f"Missing left parenthesis '(', not opened in assignment statement. Line: {line_number}")
            else:
              raise ValueError(f"Missing the keyword 'input' in assignment statement. Line: {line_number}")
          else:
            raise ValueError(f"Missing left parenthesis '(', not opened in assignment statement. Line: {line_number}")

        else:
          exp=expression(scope)
          if (ACCESS.family == "Delimiter" and ACCESS.recognized_string == ';'):
            gen_quad("=",exp,"_",var)
            ACCESS = lex()
            line_number = ACCESS.line_number
          else:
            raise ValueError(f"Missing semicolon ';' after expression in assignment statement. Line: {line_number}")
      else:
        raise ValueError(f"Missing assignment symbol '=' after Identifier token, in assignment statement. Line: {line_number}")
    else:
      raise ValueError(f"Missing Identifier token in assignment statement. Line: {line_number}")

  def print_stat(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'print'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
        ACCESS = lex()
        line_number = ACCESS.line_number

        exp=expression(scope)

        if (ACCESS.family == "GroupSymbol"
            and ACCESS.recognized_string == ')'):
          ACCESS = lex()
          line_number = ACCESS.line_number

          if (ACCESS.family == "Delimiter" and ACCESS.recognized_string == ';'):
            gen_quad("out",exp,"_","_")
            ACCESS = lex()
            line_number = ACCESS.line_number
          else:
            raise ValueError(f"Missing semicolon ';' after expression in print statement. Line: {line_number}")
        else:
          raise ValueError(f"Missing right parenthesis ')', not closed in print statement. Line: {line_number}")
      else:
        raise ValueError(f"Missing left parenthesis '(', not opened in print statement. Line: {line_number}")
    else:
      raise ValueError(f"Missing the keyword 'print' in print statement. Line: {line_number}")

  def return_stat(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'return'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
        ACCESS = lex()
        line_number = ACCESS.line_number

        exp=expression(scope)

        if (ACCESS.family == "GroupSymbol"
            and ACCESS.recognized_string == ')'):
          ACCESS = lex()
          line_number = ACCESS.line_number

          if (ACCESS.family == "Delimiter" and ACCESS.recognized_string == ';'):
            gen_quad("retv",exp,"_","_")
            ACCESS = lex()
            line_number = ACCESS.line_number
          else:
            raise ValueError(f"Missing semicolon ';' after expression in return statement. Line: {line_number}")
        else:
          raise ValueError(f"Missing right parenthesis ')', not closed in return statement. Line: {line_number}")
      else:
        raise ValueError(f"Missing left parenthesis '(', not opened in return statement. Line: {line_number}")
    else:
      raise ValueError(f"Missing the keyword 'return' in return statement. Line: {line_number}")
  
  def if_stat(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'if'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
        ACCESS = lex()
        line_number = ACCESS.line_number

        bTrue,bFlase=condition(scope)

        if (ACCESS.family == "GroupSymbol"
            and ACCESS.recognized_string == ')'):
          ACCESS = lex()
          line_number = ACCESS.line_number

          if (ACCESS.family == "Delimiter"
              and ACCESS.recognized_string == ':'):
            ACCESS = lex()
            line_number = ACCESS.line_number

            if (ACCESS.family == "GroupSymbol"
                and ACCESS.recognized_string == '#{'):
              ACCESS = lex()
              line_number = ACCESS.line_number
              backpatch(bTrue,next_quad())
              statements(scope)
              temp=make_list(next_quad())
              gen_quad("jump","_","_","_")
              backpatch(bFlase,next_quad())
             
              if (ACCESS.family == "GroupSymbol"
                  and ACCESS.recognized_string == '#}'):
                ACCESS = lex()
                line_number = ACCESS.line_number
              else:
                raise ValueError(f"Missing the two block's closing symbols after 'if' statement. Line: {line_number}")
            else:
              backpatch(bTrue,next_quad())
              statement(scope)
              temp=make_list(next_quad())	
              gen_quad("jump","_","_","_")
              backpatch(bFlase,next_quad())
              backpatch(temp,next_quad())
            if (ACCESS.family == "Keyword"
                and ACCESS.recognized_string == 'else'):
              ACCESS = lex()
              line_number = ACCESS.line_number

              if (ACCESS.family == "Delimiter"
                  and ACCESS.recognized_string == ':'):
                ACCESS = lex()
                line_number = ACCESS.line_number

                if (ACCESS.family == "GroupSymbol"
                    and ACCESS.recognized_string == '#{'):
                  ACCESS = lex()
                  line_number = ACCESS.line_number

                  statements(scope)
                  backpatch(temp,next_quad())
                  if (ACCESS.family == "GroupSymbol"
                      and ACCESS.recognized_string == '#}'):
                    ACCESS = lex()
                    line_number = ACCESS.line_number
                  else:
                    raise ValueError(f"Missing the two block's closing symbols after 'if' statement. Line: {line_number}")
                else:
                  statement(scope)
                  backpatch(temp,next_quad())
              else:
                raise ValueError(f"Missing ':' after 'else' statement. Line: {line_number}")
          else:
            raise ValueError(f"Missing ':' after 'if' statement. Line: {line_number}")
        else:
          raise ValueError(f"Missing right parenthesis ')', not closed after 'if' statement. Line: {line_number}")
      else:
        raise ValueError(f"Missing left parenthesis '(', not opened before 'if' staement. Line: {line_number}")
    else:
      raise ValueError(f"Missing the keyword 'if' in if_statement. Line: {line_number}")

  def while_stat(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'while'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
        start_of_while = next_quad()
        ACCESS = lex()
        line_number = ACCESS.line_number

        bTrue,bFalse=condition(scope)

        if (ACCESS.family == "GroupSymbol"
            and ACCESS.recognized_string == ')'):
          ACCESS = lex()
          line_number = ACCESS.line_number

          if (ACCESS.family == "Delimiter"
              and ACCESS.recognized_string == ':'):
            ACCESS = lex()
            line_number = ACCESS.line_number

            if (ACCESS.family == "GroupSymbol"
                and ACCESS.recognized_string == '#{'):
              ACCESS = lex()
              line_number = ACCESS.line_number
              backpatch(bTrue,next_quad())
              statements(scope)
              gen_quad("jump","_","_",start_of_while)
              backpatch(bFalse,next_quad())
              if (ACCESS.family == "GroupSymbol"
                  and ACCESS.recognized_string == '#}'):
                ACCESS = lex()
                line_number = ACCESS.line_number 
              else:
                raise ValueError(f"Missing the two block's closing symbols after 'while' statement. Line: {line_number}")
            else:
              backpatch(bTrue,next_quad())
              statement(scope)
              gen_quad("jump","_","_",start_of_while)
              backpatch(bFalse,next_quad())
          else:
            raise ValueError(f"Missing ':' after 'while' statement. Line: {line_number}")
        else:
          raise ValueError(f"Missing right parenthesis ')', not closed after 'while' statement. Line: {line_number}")
      else:
        raise ValueError(f"Missing left parenthesis '(', not opened before 'while' staement. Line: {line_number}")
    else:
      raise ValueError(f"Missing the keyword 'while' in while_statement. Line: {line_number}")

  def expression(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    optional_sign()
    temp_term1=term(scope)

    while (ACCESS.family == "AddOperator" and ACCESS.recognized_string == '+'
           or ACCESS.family == "AddOperator"
           and ACCESS.recognized_string == '-'):
      add_opper=ACCESS.recognized_string
      ADD_OP()
      temp_term2=term(scope)
      temp_var=new_temp_var()
      var=Entity(temp_var,"temp_var",offset)
      offset+=4
      scope.add_entity(var)
      gen_quad(add_opper,temp_term1,temp_term2,temp_var)
      temp_term1=temp_var
    return temp_term1  

  def term(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    temp_factor1=factor(scope)

    while (ACCESS.family == "MulOperator" and ACCESS.recognized_string == '*'
           or ACCESS.family == "MulOperator"
           and ACCESS.recognized_string == '//'):
      mul_opper=ACCESS.recognized_string
      MUL_OP()
      temp_factor2=factor(scope)
      temp_var=new_temp_var()
      var=Entity(temp_var,"temp_var",offset)
      offset+=4
      scope.add_entity(var)
      gen_quad(mul_opper,temp_factor1,temp_factor2,temp_var)
      temp_factor1=temp_var
    return temp_factor1  

  def factor(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    if (ACCESS.family == "Number"):
      num=ACCESS.recognized_string
      ACCESS = lex()
      line_number = ACCESS.line_number
      return num

    elif (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
      ACCESS = lex()
      line_number = ACCESS.line_number

      exp=expression(scope)

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == ')'):
        ACCESS = lex()
        line_number = ACCESS.line_number
        return exp
      else:
        raise ValueError(f"Missing right parenthesis ')', after factor's expression. Line: {line_number}")
      
    elif (ACCESS.family == "Identifier"):
      id=ACCESS.recognized_string
      if not_exists(id)==False:
        raise ValueError(f"Variable {id} was never declared")
      ACCESS = lex()
      line_number = ACCESS.line_number

      id=idtail(id,scope)
      return id
    else:
      raise ValueError(f"Missing expression or variable in factor's statement. Line: {line_number}")
    
  def idtail(caller,scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
      ACCESS = lex()
      line_number = ACCESS.line_number

      actual_par_list(scope)

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == ')'):
        temp=new_temp_var()
        tempVar=Entity(temp,"par",offset)
        tempVar.setPar_mode("RET")
        scope.add_entity(tempVar)
        offset+=4
        gen_quad("call",caller,"_","_")
        gen_quad("par",temp,"RET","_")
        ACCESS = lex()
        line_number = ACCESS.line_number
        return temp
    return caller    

  def actual_par_list(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    if (ACCESS.family == "Number"
        or ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('
        or ACCESS.family == "Identifier"):

      temp_exp1=expression(scope)
      gen_quad("par",temp_exp1,"CV","_")
      while (ACCESS.family == "Delimiter" and ACCESS.recognized_string == ','):
        ACCESS = lex()
        line_number = ACCESS.line_number

        temp_exp2=expression(scope)
        gen_quad("par",temp_exp2,"CV","_")

  def optional_sign():
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    if (ACCESS.family == "AddOperator" and ACCESS.recognized_string == '+'
        or ACCESS.family == "AddOperator" and ACCESS.recognized_string == '-'):

      ADD_OP()

  def ADD_OP():
    global ACCESS
    global line_number

    if (ACCESS.family == "AddOperator" and ACCESS.recognized_string == '+'):
      ACCESS = lex()
      line_number = ACCESS.line_number

    elif (ACCESS.family == "AddOperator" and ACCESS.recognized_string == '-'):

      ACCESS = lex()
      line_number = ACCESS.line_number

  def MUL_OP():
    global ACCESS
    global line_number

    if (ACCESS.family == "MulOperator" and ACCESS.recognized_string == '*'):
      ACCESS = lex()
      line_number = ACCESS.line_number

    elif (ACCESS.family == "MulOperator" and ACCESS.recognized_string == '//'):
      ACCESS = lex()
      line_number = ACCESS.line_number

  def condition(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    t1_true,t1_false=bool_term(scope)

    while (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'or'):
      ACCESS = lex()
      line_number = ACCESS.line_number
      backpatch(t1_false,next_quad())
      t2_true,t2_false=bool_term(scope)
      t1_true=merge_lists(t1_true,t2_true)
      t1_false=t2_false
    return t1_true,t1_false
  
  def bool_term(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    f1_true,f1_false=bool_factor(scope)

    while (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'and'):
      ACCESS = lex()
      line_number = ACCESS.line_number
      backpatch(f1_true,next_quad())
      f2_true,f2_false=bool_factor(scope)
      f1_false=merge_lists(f1_false,f2_false)
      f1_true=f2_true
    return f1_true,f1_false

  def bool_factor(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global ACCESS
    global line_number

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'not'):
      ACCESS = lex(scope)
      line_number = ACCESS.line_number

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '['):
        ACCESS = lex(scope)
        line_number = ACCESS.line_number

        bFalse,bTrue=condition(scope)

        if (ACCESS.family == "GroupSymbol"
            and ACCESS.recognized_string == ']'):
          ACCESS = lex()
          line_number = ACCESS.line_number

        else:
          raise ValueError(f"Missing right ']', after bool_factor's condition. Line: {line_number}")
      else:
        raise ValueError(f"Missing right '[', after keyword 'not' in bool_factor. Line: {line_number}")

    elif (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '['):
      ACCESS = lex()
      line_number = ACCESS.line_number

      bTrue,bFalse=condition(scope)

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == ']'):
        ACCESS = lex()
        line_number = ACCESS.line_number

      else:
        raise ValueError(f"Missing right ']', after bool_factor's condition. Line: {line_number}")
    else:

      exp1=expression(scope)
      rel_opper=ACCESS.recognized_string
      REL_OP()
      exp2=expression(scope)
      bTrue=make_list(next_quad())
      gen_quad(rel_opper,exp1,exp2,"_")
      bFalse=make_list(next_quad())
      gen_quad("jump","_","_","_")
    return bTrue,bFalse

  def REL_OP():
    global ACCESS
    global line_number

    if (ACCESS.family == "RelOperator" and ACCESS.recognized_string == '=='):
      ACCESS = lex()
      line_number = ACCESS.line_number

    elif (ACCESS.family == "RelOperator" and ACCESS.recognized_string == '!='):
      ACCESS = lex()
      line_number = ACCESS.line_number

    elif (ACCESS.family == "RelOperator" and ACCESS.recognized_string == '<='):
      ACCESS = lex()
      line_number = ACCESS.line_number

    elif (ACCESS.family == "RelOperator" and ACCESS.recognized_string == '>='):
      ACCESS = lex()
      line_number = ACCESS.line_number

    elif (ACCESS.family == "RelOperator" and ACCESS.recognized_string == '>'):
      ACCESS = lex()
      line_number = ACCESS.line_number
      
    elif (ACCESS.family == "RelOperator" and ACCESS.recognized_string == '<'):
      ACCESS = lex()
      line_number = ACCESS.line_number
      
    else:
      raise ValueError(f"Missing an operator from the following lsit ['==', '!=', '<=', '>=', '>', '<']. Line: {line_number}")

  def call_main_part(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting, quad_num
    global ACCESS
    global line_number

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'if'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "Keyword"
          and ACCESS.recognized_string == '__name__'):
        gen_quad("begin_block", "__main__", "_","_")
        ACCESS = lex()
        line_number = ACCESS.line_number

        if (ACCESS.family == "RelOperator"
            and ACCESS.recognized_string == '=='):
          ACCESS = lex()
          line_number = ACCESS.line_number

          if (ACCESS.family == "Delimiter"
              and ACCESS.recognized_string == '"'):
            ACCESS = lex()
            line_number = ACCESS.line_number

            if (ACCESS.family == "Keyword"
                and ACCESS.recognized_string == '__main__'):
              
              main_function=Entity("__main__","main",0)
              offset+=4
              main_function.setStart_quad(quad_num)
              scope.add_entity(main_function)
              ACCESS = lex()
              line_number = ACCESS.line_number

              if (ACCESS.family == "Delimiter"
                  and ACCESS.recognized_string == '"'):
                ACCESS = lex()
                line_number = ACCESS.line_number

                if (ACCESS.family == "Delimiter"
                    and ACCESS.recognized_string == ':'):
                  ACCESS = lex()
                  line_number = ACCESS.line_number

                  main_function_call(scope)
                  while (ACCESS.family == "Identifier"):
                    main_function_call(scope)
                  gen_quad("halt", "_","_","_")  
                  gen_quad("end_block", "__main__", "_","_")  
                else:
                  raise ValueError(f"Missing ':', in statement of call_main_part. Line: {line_number}")
              else:
                raise ValueError(f"Missing double quotation mark , in statement of call_main_part. Line: {line_number}")
            else:
              raise ValueError(f"Missing keyword '__main__', in statement of call_main_part. Line: {line_number}")
          else:
            raise ValueError(f"Missing double quotation mark , in statement of call_main_part. Line: {line_number}")
        else:
          raise ValueError(f"Missing of rel-operator '==', in statement of call_main_part. Line: {line_number}")
      else:
        raise ValueError(f"Missing keyword '__name__', in statement of call_main_part. Line: {line_number}")
    else:
      raise ValueError(f"Missing keyword 'if', in statement of call_main_part. Line: {line_number}")

  def main_function_call(scope):
    global functions_list, variables_list, temp_scope, final_scope, offset, nesting
    global line_number
    global ACCESS

    if (ACCESS.family == "Identifier"):
      id=ACCESS.recognized_string
      if not_exists(id)==False:
        raise ValueError(f"{id} is not found in program. Line {line_number}")
      gen_quad("call",id,"_","_")
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
        ACCESS = lex()
        line_number = ACCESS.line_number

        if (ACCESS.family == "GroupSymbol"
            and ACCESS.recognized_string == ')'):
          ACCESS = lex()
          line_number = ACCESS.line_number

          if (ACCESS.family == "Delimiter"
              and ACCESS.recognized_string == ';'):
            ACCESS = lex()
            line_number = ACCESS.line_number
          else:
            raise ValueError(f"Missing ';', in statement of main_function_call. Line: {line_number}")
        else:
          raise ValueError(f"Missing ')', in statement of main_function_call. Line: {line_number}")
      else:
        raise ValueError(f"Missing '(', in statement of main_function_call. Line: {line_number}")
    else:
      raise ValueError(f"Missing name/token of Identifier family, in statement of main_function_call. Line: {line_number}")

  startRule()


def gen_quad(op,x,y,z): ##generates a quad 
    global quad_num
    global quads
    quad_num +=1
    quads.append([quad_num,op,x,y,z])

def next_quad(): #returns the number of the next quad 
    global quad_num
    return quad_num+1

def new_temp_var(): #returns a new temp variable 
    global temp_num
    global temp_vars
    temp_num +=1
    temp = "T_"+str(temp_num)
    temp_vars.append(temp)
    return temp

def empty_list(): #returns an empty quads list 
    new_list = []
    return new_list

def make_list(x): #returns a quads list containing x  
    new_list = []
    new_list.append(x)
    return new_list

def merge_lists(l1,l2): #merges two quads lists into one 
    merged_l = l1+l2
    return merged_l

def backpatch(param_list, z): #fills the label z of a quad 
    global quads
    for quad in quads:
      if quad[0] in param_list:
        quad[4]=z

def print_quads(): #prints all created quads in the cmd 
    global quads
    for quad in quads:
      line=str(quad[0])+" "+str(quad[1])+" "+str(quad[2])+" "+str(quad[3])+" "+str(quad[4])
      print(line)        

def int_file(): #creates file that contains the quads 
  file=cutePy_file_name.split(".cpy")
  file=file[0]+".int"
  myfile=open(file,'w')
  for quad in quads:
    myfile.write(str(quad[0])+": "+str(quad[1])+" "+str(quad[2])+" "+str(quad[3])+" "+str(quad[4]))
    myfile.write("\n")
  myfile.close()  

def not_exists(x): #this function is used to ckeck if an entity is declared before used 
  global temp_scope
  for i in temp_scope:
    for j in i.entity_list:
      if j.name==x:
        return True
  return False      

def exists(nesting, x): #this function is used to check if an entity is already declared in a scope 
  global temp_scope
  for i in temp_scope:
    if i.nesting_level==nesting:
      for j in i.entity_list:
        if j.name==x.name:
          return True
  return False       

def print_symbol_table(): #prints the final symbol table in the cmd 
  global final_scope
  for i in final_scope:
    nesting=i.nesting_level
    for j in i.entity_list:
      line="Level :"+str(nesting)+" Entity : "+j.name+", offset: "+str(j.offset)+", type: "+j.type
      if(j.type=="main_function"):
        line=line+", next quad: "+str(j.start_quad)+", frame length: "+str(j.frame_length)
      elif(j.type=="function"):
        line=line+", next quad: "+str(j.start_quad)+", frame length: "+str(j.frame_length)+" parameters: "
        for par in j.par_list:
          line=line+" "+par.name
      elif(j.type=="par"):
        line=line+" parMode: "+j.par_mode      
      print(line)  

def symbol_file(): #creates file that contains the symbol table
  file=cutePy_file_name.split(".cpy")
  file=file[0]+".symb"
  myfile=open(file,'w')
  for i in final_scope:
    nesting=i.nesting_level
    if(nesting==0):
      name="main"
    elif(nesting==1):
      func=functions_list.pop(len(functions_list)-2)
      name=func.name  
    else:
      func=functions_list.pop()
      name=func.name
    myfile.write("Nesting Level: "+str(nesting)+" -- Scope of function "+name+"\n")
    for j in i.entity_list:
      line="    Entity : "+j.name+", offset: "+str(j.offset)+", type: "+j.type
      if(j.type=="main_function"):
        line=line+", next quad: "+str(j.start_quad)+", frame length: "+str(j.frame_length)
      elif(j.type=="function"):
        line=line+", next quad: "+str(j.start_quad)+", frame length: "+str(j.frame_length)+" parameters: "
        for par in j.par_list:
          line=line+" "+par.name
      elif(j.type=="par"):
        line=line+" parMode: "+j.par_mode
      myfile.write(line+"\n")
  myfile.close()  

def gnvlcode(x, cur_level): #writes value of non-local variable to register $t0
  for i in final_scope:
    for j in i.entity_list:
      if j.name == x:
        varscope=i.nesting_level
        varOffset=j.offset

  line = "  lw $t0,-4($sp)\n"            
  for i in range(varscope,cur_level):
    line+=" lw $t0, -4($t0)\n"

  line+= "  add $t0,$t0,-" + str(varOffset) + "\n" 
  return line

def loadvr(v, r, cur_level): #moves value of data from memory to a register 
  varscope=-1
  temp_ent=final_scope[0].entity_list[0]
  for i in final_scope:
    for j in i.entity_list:
      if(j.name==v):
        varscope=i.nesting_level
        temp_ent=j
        break
  if(v.isdigit()):
     code="   li $t"+str(r)+","+str(v)+"      /* loads "+str(v)+" */\n" #loads constants
  elif(varscope==1):
    code="  lw $t"+str(r)+",-"+str(temp_ent.offset)+"($gp)      /* loads "+str(v)+" */\n" #loads global variables
  elif(varscope==cur_level and (temp_ent.type=="temp_var" or temp_ent.type=="var" or (temp_ent.type=="par" and temp_ent.par_mode=="RET"))): #loads temp variables, variable, or return parameters that are in current scope 
    code="    lw $t"+str(r)+",-"+str(temp_ent.offset)+"($sp)      /* loads "+str(v)+" */\n"
  elif(varscope<cur_level and (temp_ent.type=="temp_var" or temp_ent.type=="var" or (temp_ent.type=="par" and temp_ent.par_mode=="RET"))): #loads temp variables, variable, or return parameters that are in lower scope 
    code=gnvlcode(temp_ent.name, cur_level)
    code+="   lw $t"+str(r)+",($t0)      /* loads "+str(v)+" */\n"
  elif(varscope==cur_level and (temp_ent.type=="par" and temp_ent.par_mode=="CV")): #loads pass by refernce parameters in current scope 
    code="    lw $t0,-"+str(temp_ent.offset)+"(sp)\n"
    code+="   lw $t"+str(r)+",($t0)      /* loads "+str(v)+" */\n"
  elif(varscope<cur_level and (temp_ent.type=="par" and temp_ent.par_mode=="CV")): #loads pass by refernce parameters in lower scope
    code=gnvlcode(temp_ent.name, cur_level)
    code+="   lw $t0,($t0)\n"
    code+="   lw $t"+str(r)+",($t0)      /* loads "+str(v)+" */\n"
  else:
    code="error loading "+temp_ent.name+"\n"

  return code  



def storerv(v, r, cur_level): #moves value of data from a register to memory
  varscope=-1
  temp_ent=final_scope[0].entity_list[0]
  for i in final_scope:
    for j in i.entity_list:
      if(j.name==v):
        varscope=i.nesting_level
        temp_ent=j
        break  
  
  if(varscope==1):
    code="    sw $t"+str(r)+",-"+str(temp_ent.offset)+"($gp)      /* strores "+str(v)+" */\n" #stores global variables
  elif(varscope==cur_level and (temp_ent.type=="temp_var" or temp_ent.type=="var" or (temp_ent.type=="par" and temp_ent.par_mode=="RET"))): #stores temp variables, variable, or return parameters that are in current scope 
    code="    sw $t"+str(r)+",-"+str(temp_ent.offset)+"($sp)      /* strores "+str(v)+" */\n"
  elif(varscope<cur_level and (temp_ent.type=="temp_var" or temp_ent.type=="var" or (temp_ent.type=="par" and temp_ent.par_mode=="RET"))): #stores temp variables, variable, or return parameters that are in lower scope 
    code=gnvlcode(temp_ent.name, cur_level)
    code+="   sw $t"+str(r)+",($t0)      /* strores "+str(v)+" */\n"
  elif(varscope==cur_level and (temp_ent.type=="par" and temp_ent.par_mode=="CV")): #stores pass by refernce parameters in current scope 
    code="    lw $t0,-"+str(temp_ent.offset)+"(sp)\n"
    code+="   sw $t"+str(r)+",($t0)      /* strores "+str(v)+" */\n"
  elif(varscope<cur_level and (temp_ent.type=="par" and temp_ent.par_mode=="CV")): #stores pass by refernce parameters in lower scope
    code=gnvlcode(temp_ent.name, cur_level)
    code+="   lw $t0,($t0)\n"
    code+="   sw $t"+str(r)+",($t0)      /* strores "+str(v)+" */\n"
  else:
    code="error storing "+temp_ent.name+"\n"

  return code

def find_labels():
  global labels
  for i in quads:
    if(i[1] in ["<",">","==","!=","<=",">=","jump"] and i[4]!="_"):
      labels.append(i[4]) 

def make_assembly():
  find_labels()
  global labels
  curr_level=0
  for i in quads:
    #print("quad num is "+str(i[0])+" labels is "+''.join(map(str, labels)))
    code=""
    if(i[1]=="+"): #makes assembly code for addition
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
      code+=loadvr(i[2],1,curr_level)
      code+=loadvr(i[3],2,curr_level)
      code+="   add "+"$t3, $t1, $t2      \* "+str(i[4])+"="+str(i[2])+str(i[1])+str(i[3])+" */\n"
      code+=storerv(i[4],3,curr_level)
      asm_commands.append(code)
    elif(i[1]=="-"): #makes assembly code for subtraction
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"     
      code+=loadvr(i[2],1,curr_level)
      code+=loadvr(i[3],2,curr_level)
      code+="   sub "+"$t3, $t1, $t2      \* "+str(i[4])+"="+str(i[2])+str(i[1])+str(i[3])+" */\n"
      code+=storerv(i[4],3,curr_level)
      asm_commands.append(code)
    elif(i[1]=="*"): #makes assembly code for multiplication  
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
      code+=loadvr(i[2],1,curr_level)
      code+=loadvr(i[3],2,curr_level)
      code+="   mull "+"$t3, $t1, $t2      \* "+str(i[4])+"="+str(i[2])+str(i[1])+str(i[3])+" */\n"
      code+=storerv(i[4],3,curr_level)
      asm_commands.append(code)
    elif(i[1]=="//"): #makes assembly code for division  
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
      code+=loadvr(i[2],1,curr_level)
      code+=loadvr(i[3],2,curr_level)
      code+="   div "+"$t3, $t1, $t2      \* "+str(i[4])+"="+str(i[2])+str(i[1])+str(i[3])+" */\n"
      code+=storerv(i[4],3,curr_level)
      asm_commands.append(code)
    elif(i[1]=="<"): #makes assembly code for less than jump
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
      code+=loadvr(i[2],1,curr_level)
      code+=loadvr(i[3],2,curr_level)
      code+="   blt "+"$t1, $t2,"+str(i[4])+"     \* if "+str(i[2])+str(i[1])+str(i[3])+" then jump to "+str(i[4])+" */\n"
      asm_commands.append(code)
    elif(i[1]=="<="): #makes assembly code for less equal jump
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
      code+=loadvr(i[2],1,curr_level)
      code+=loadvr(i[3],2,curr_level)
      code+="   ble "+"$t1, $t2,"+str(i[4])+"     \* if "+str(i[2])+str(i[1])+str(i[3])+" then jump to "+str(i[4])+" */\n"
      asm_commands.append(code)
    elif(i[1]==">"): #makes assembly code for greater than jump
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
      code+=loadvr(i[2],1,curr_level)
      code+=loadvr(i[3],2,curr_level)
      code+="   bgt "+"$t1, $t2,"+str(i[4])+"     \* if "+str(i[2])+str(i[1])+str(i[3])+" then jump to "+str(i[4])+" */\n"
      asm_commands.append(code)
    elif(i[1]==">="): #makes assembly code for greater equal jump
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n" 
      code+=loadvr(i[2],1,curr_level)
      code+=loadvr(i[3],2,curr_level)
      code+="   bge "+"$t1, $t2,"+str(i[4])+"     \* if "+str(i[2])+str(i[1])+str(i[3])+" then jump to "+str(i[4])+" */\n"
      asm_commands.append(code)
    elif(i[1]=="=="): #makes assembly code for equals jump
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
      code+=loadvr(i[2],1,curr_level)
      code+=loadvr(i[3],2,curr_level)
      code+="   beq "+"$t1, $t2,"+str(i[4])+"     \* if "+str(i[2])+str(i[1])+str(i[3])+" then jump to "+str(i[4])+" */\n"
      asm_commands.append(code)
    elif(i[1]=="!="): #makes assembly code for not equals jump
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
      code+=loadvr(i[2],1,curr_level)
      code+=loadvr(i[3],2,curr_level)
      code+="   bne "+"$t1, $t2,"+str(i[4])+"     \* if "+str(i[2])+str(i[1])+str(i[3])+" then jump to "+str(i[4])+" */\n"
      asm_commands.append(code)
    elif (i[1]=="jump" and i[4]!="_"): #makes assembly code for jump to label
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
      code+="    b "+str(i[4])+"     /* jump to "+str(i[4])+" */\n"                                                            
      asm_commands.append(code)
    elif (i[1]=="="): #makes assembly code for value assignment to variable...
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
      if(i[2]=="input"): #...from input
        code+="   li $v0,5\n"
        code+="   ecall\n"
        code+="   move $t0,$v0      /* input("+str(i[4])+") */\n" 
        code+=storerv(0,i[4],curr_level)
        asm_commands.append(code)
      else: #...or other variable
        code+=loadvr(i[2],1,curr_level)
        code+="     /* "+str(i[4])+" = "+str(i[2])+" */\n"
        code+=storerv(i[4],1,curr_level)
        asm_commands.append(code)
    elif(i[1]=="retv"): #makes assembly code for return statement
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
      code+=loadvr(i[2],1,curr_level)
      code+="   lw t0,-8(sp)\n"
      code+="   sw t1,(t0)      /* return("+str(i[2])+") /*\n"
      asm_commands.append(code)
    elif(i[1]=="out"):  #makes assembly code for print statement
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
      code+=loadvr(i[2],0,curr_level)
      code+="   mv $a0, $t0\n"
      code+="   li $a7, 1\n"
      code+="   ecall\n"
      code+="   la $a0,str_nl\n"
      code+="   li $a7,4\n"
      code+="   ecall     /* print("+str(i[2])+") /*\n"
      asm_commands.append(code)
    elif(i[1]=="begin_block"): #makes assembly code for function blocks 
      if(i[2]=="__main__"): #...main function 
        main_framelength=0
        for j in final_scope[0].entity_list:
          if j.type=="main":
            main_framelength=j.framelength
        code="\nj Lmain     /* main block begins */\n"
        code+="   addi sp,sp,"+str(main_framelength)+"\n"
        code+="   move gp,sp\n"
        asm_commands.append(code)     
      else: #... all other functions 
        curr_level+=1
        code="    label : "+i[2]+"      /* "+str(i[2])+" block begins */\n"
        asm_commands.append(code)
    elif(i[1] == "end_block"): #marks endong of function blocks
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
        labels.pop(0)
      if(i[2]=="__main__"):
        code+="/* main block ends */\n\n"
        asm_commands.append(code)
      elif("main" in i[2] and i[2]!="__main__"):
        curr_level-=1
        code+="/* "+str(i[2])+" block ends */\n"
        asm_commands.append(code)
      else:
        curr_level-=1
        code+="      /* "+str(i[2])+" block ends */\n\n"
        asm_commands.append(code)    
    elif(i[1]=="call" and ("main" in i[2] and i[2]!="__main__")):
      code+="   j "+i[2]+"\n"
      asm_commands.append(code)
    elif(i[1]=="call" and "main" not in i[2]):
      code+="   #\n cant call function "+i[2]+"\n\n"
      asm_commands.append(code)
    else:
      if(i[0] in labels):
        code+="label : "+str(i[0])+"\n"
        labels.pop(0)    

def asm_file():
  make_assembly()
  filename = cutePy_file_name.split(".cpy")
  filename=filename[0]+".asm"
  asm_file = open(filename,'w')
  for i in asm_commands:
            asm_file.write(i)

syntax()
print("Everything has functioned successfully!")
# END OF: Syntax Analysis

#print_quads()
int_file()
symbol_file()
asm_file()
##print_symbol_table()
