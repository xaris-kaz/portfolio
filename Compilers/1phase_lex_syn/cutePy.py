# AM: 4778, NAME: Alkiviadis Patras, username: cse94778
# AM: 4679, NAME: Theocharis Kazakidis, username: cse94679

# The following code has been developed in python 3.11.2 and is written in Python's IDLE(Python 3.11 64-bit).
# Each block of code is indented using a single '\t' (tab) character.

import sys

# The acceptable range for numbers is defined by the MAX_NUMBER constant.
MAX_NUMBER = 2**32  #4294967296

# The Token class is defined in accordance with the specifications provided in 'lex.pdf'.
class Token:
  def __init__(self, recognized_string, family, line_number):
    self.recognized_string = recognized_string
    self.family = family
    self.line_number = line_number


# The file name is retrived from the command line arguments.
# The file is opened in read mode with UTF-8 encoding and stored in the "file" variable.
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


# If you desire to evaluate or display the return value exclusively from the lex() function, you may execute the subsequent code provided in the comments. 
# However, please exercise caution. It is imperative to comment out the entire section of code, ranging from "# Syntax Analysis" to the conclusion of the script. 
# Failure to do so will result in the malfunction of the program.
'''
while True:
    ACCESS = lex()
    if ACCESS.family == "EOF":
        print(ACCESS.recognized_string, "\t", "Family: ", ACCESS.family, "\t", "line: ", ACCESS.line_number)
        break
    print(ACCESS.recognized_string, "\t", "Family: ", ACCESS.family, "\t", "line: ", ACCESS.line_number)
'''
# END OF: Lexical Analysis



# Syntax Analysis
def syntax():
  global line_number
  global token
  global ACCESS
  ACCESS = lex()
  line_number = ACCESS.line_number
  token = ACCESS.recognized_string

  def startRule():
    def_main_part()
    call_main_part()

  def def_main_part():
    global ACCESS
    def_main_function()
    while (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'def'):
      def_main_function()

  def def_main_function():    # Testing:  def main_factorial(): #{  .....   #}
    global line_number 
    global token
    global ACCESS

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'def'): 
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "Identifier"):
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
                ACCESS = lex()
                line_number = ACCESS.line_number
                declarations()
                while (ACCESS.family == "Keyword"
                       and ACCESS.recognized_string == 'def'):
                  def_function()
                statements()

                if (ACCESS.family == "GroupSymbol"
                    and ACCESS.recognized_string == '#}'):
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
  
  def def_function():  # Testing:  def main_fibonacci(): #{ ..  def fibonacci(x): #{ ... #} .. #}
    global line_number
    global token
    global ACCESS

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'def'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "Identifier"):
        ACCESS = lex()
        line_number = ACCESS.line_number

        if (ACCESS.family == "GroupSymbol"
            and ACCESS.recognized_string == '('):
          ACCESS = lex()
          line_number = ACCESS.line_number

          id_list()

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

                declarations()
                while (ACCESS.family == "Keyword"
                       and ACCESS.recognized_string == 'def'):
                  def_function()
                statements()

                if (ACCESS.family == "GroupSymbol"
                    and ACCESS.recognized_string == '#}'):
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

  def declarations():
    global ACCESS

    while (ACCESS.family == "Keyword"
           and ACCESS.recognized_string == '#declare'):
      declaration_line_number()

  def declaration_line_number():
    global ACCESS

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == '#declare'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      id_list()

  def id_list():
    global line_number
    global ACCESS

    if (ACCESS.family == "Identifier"):
      ACCESS = lex()
      line_number = ACCESS.line_number

      while (ACCESS.family == "Delimiter" and ACCESS.recognized_string == ','):
        ACCESS = lex()
        line_number = ACCESS.line_number

        if (ACCESS.family == "Identifier"):
          ACCESS = lex()
          line_number = ACCESS.line_number

        else:
          raise ValueError(f"Missing Identifier token after comma(','). Line: {line_number}")

  def statement():
    global line_number
    global ACCESS

    if (ACCESS.family == "Identifier"
        or ACCESS.family == "Keyword" and ACCESS.recognized_string == 'print'
        or ACCESS.family == "Keyword"
        and ACCESS.recognized_string == 'return'):
      simple_statement()
    elif (
        ACCESS.family == "Keyword" and ACCESS.recognized_string == 'if'
        or ACCESS.family == "Keyword" and ACCESS.recognized_string == 'while'):
      structured_statement()
    else:
      raise ValueError(f"Invalid statement. Line: {line_number}")

  def statements():
    global ACCESS

    statement()
    while (
        ACCESS.family == "Identifier"
        or ACCESS.family == "Keyword" and ACCESS.recognized_string == 'print'
        or ACCESS.family == "Keyword" and ACCESS.recognized_string == 'return'
        or ACCESS.family == "Keyword" and ACCESS.recognized_string == 'if'
        or ACCESS.family == "Keyword" and ACCESS.recognized_string == 'while'):
      statement()

  def simple_statement():
    global ACCESS

    if (ACCESS.family == "Identifier"):
      assignment_stat()
    elif (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'print'):
      print_stat()
    elif (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'return'):
      return_stat()

  def structured_statement():
    global ACCESS

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'if'):
      if_stat()
    elif (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'while'):
      while_stat()

  def assignment_stat():
    global ACCESS
    global line_number

    if (ACCESS.family == "Identifier"):
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

                    if (ACCESS.family == "Delimiter"
                        and ACCESS.recognized_string == ';'):
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
          expression()

          if (ACCESS.family == "Delimiter"
              and ACCESS.recognized_string == ';'):
            ACCESS = lex()
            line_number = ACCESS.line_number
          else:
            raise ValueError(f"Missing semicolon ';' after expression in assignment statement. Line: {line_number}")
      else:
        raise ValueError(f"Missing assignment symbol '=' after Identifier token, in assignment statement. Line: {line_number}")
    else:
      raise ValueError(f"Missing Identifier token in assignment statement. Line: {line_number}")

  def print_stat():
    global ACCESS
    global line_number

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'print'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
        ACCESS = lex()
        line_number = ACCESS.line_number

        expression()

        if (ACCESS.family == "GroupSymbol"
            and ACCESS.recognized_string == ')'):
          ACCESS = lex()
          line_number = ACCESS.line_number

          if (ACCESS.family == "Delimiter"
              and ACCESS.recognized_string == ';'):
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

  def return_stat():
    global ACCESS
    global line_number

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'return'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
        ACCESS = lex()
        line_number = ACCESS.line_number

        expression()

        if (ACCESS.family == "GroupSymbol"
            and ACCESS.recognized_string == ')'):
          ACCESS = lex()
          line_number = ACCESS.line_number

          if (ACCESS.family == "Delimiter"
              and ACCESS.recognized_string == ';'):
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
  
  def if_stat():
    global ACCESS
    global line_number

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'if'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
        ACCESS = lex()
        line_number = ACCESS.line_number

        condition()

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

              statements()
              if (ACCESS.family == "GroupSymbol"
                  and ACCESS.recognized_string == '#}'):
                ACCESS = lex()
                line_number = ACCESS.line_number
              else:
                raise ValueError(f"Missing the two block's closing symbols after 'if' statement. Line: {line_number}")
            else:
              statement()

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

                  statements()
                  if (ACCESS.family == "GroupSymbol"
                      and ACCESS.recognized_string == '#}'):
                    ACCESS = lex()
                    line_number = ACCESS.line_number
                  else:
                    raise ValueError(f"Missing the two block's closing symbols after 'if' statement. Line: {line_number}")
                else:
                  statement()
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

  def while_stat():
    global ACCESS
    global line_number

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'while'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
        ACCESS = lex()
        line_number = ACCESS.line_number

        condition()

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

              statements()
              if (ACCESS.family == "GroupSymbol"
                  and ACCESS.recognized_string == '#}'):
                ACCESS = lex()
                line_number = ACCESS.line_number 
              else:
                raise ValueError(f"Missing the two block's closing symbols after 'while' statement. Line: {line_number}")
            else:
              statement()
          else:
            raise ValueError(f"Missing ':' after 'while' statement. Line: {line_number}")
        else:
          raise ValueError(f"Missing right parenthesis ')', not closed after 'while' statement. Line: {line_number}")
      else:
        raise ValueError(f"Missing left parenthesis '(', not opened before 'while' staement. Line: {line_number}")
    else:
      raise ValueError(f"Missing the keyword 'while' in while_statement. Line: {line_number}")

  def expression():
    global ACCESS
    global line_number

    optional_sign()
    term()

    while (ACCESS.family == "AddOperator" and ACCESS.recognized_string == '+'
           or ACCESS.family == "AddOperator"
           and ACCESS.recognized_string == '-'):
      ADD_OP()
      term()

  def term():
    global ACCESS
    global line_number

    factor()

    while (ACCESS.family == "MulOperator" and ACCESS.recognized_string == '*'
           or ACCESS.family == "MulOperator"
           and ACCESS.recognized_string == '//'):
      MUL_OP()
      factor()

  def factor():
    global ACCESS
    global line_number

    if (ACCESS.family == "Number"):
      ACCESS = lex()
      line_number = ACCESS.line_number

    elif (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
      ACCESS = lex()
      line_number = ACCESS.line_number

      expression()

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == ')'):
        ACCESS = lex()
        line_number = ACCESS.line_number
      else:
        raise ValueError(f"Missing right parenthesis ')', after factor's expression. Line: {line_number}")
      
    elif (ACCESS.family == "Identifier"):
      ACCESS = lex()
      line_number = ACCESS.line_number

      idtail()

    else:
      raise ValueError(f"Missing expression or variable in factor's statement. Line: {line_number}")
    
  def idtail():
    global ACCESS
    global line_number

    if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('):
      ACCESS = lex()
      line_number = ACCESS.line_number

      actual_par_list()

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == ')'):
        ACCESS = lex()
        line_number = ACCESS.line_number

  def actual_par_list():
    global ACCESS
    global line_number

    if (ACCESS.family == "Number"
        or ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '('
        or ACCESS.family == "Identifier"):

      expression()

      while (ACCESS.family == "Delimiter" and ACCESS.recognized_string == ','):
        ACCESS = lex()
        line_number = ACCESS.line_number

        expression()

  def optional_sign():
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

  def condition():
    global ACCESS
    global line_number

    bool_term()

    while (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'or'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      bool_term()

  def bool_term():
    global ACCESS
    global line_number

    bool_factor()

    while (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'and'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      bool_factor()

  def bool_factor():
    global ACCESS
    global line_number

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'not'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == '['):
        ACCESS = lex()
        line_number = ACCESS.line_number

        condition()

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

      condition()

      if (ACCESS.family == "GroupSymbol" and ACCESS.recognized_string == ']'):
        ACCESS = lex()
        line_number = ACCESS.line_number

      else:
        raise ValueError(f"Missing right ']', after bool_factor's condition. Line: {line_number}")
    else:

      expression()

      REL_OP()

      expression()

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

  def call_main_part():
    global ACCESS
    global line_number

    if (ACCESS.family == "Keyword" and ACCESS.recognized_string == 'if'):
      ACCESS = lex()
      line_number = ACCESS.line_number

      if (ACCESS.family == "Keyword"
          and ACCESS.recognized_string == '__name__'):
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

                  main_function_call()
                  while (ACCESS.family == "Identifier"):
                    main_function_call()
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

  def main_function_call():
    global line_number
    global ACCESS

    if (ACCESS.family == "Identifier"):
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
syntax()
print("Everything has functioned successfully!")
# END OF: Syntax Analysis

