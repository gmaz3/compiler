# -*- coding: utf-8 -*-

from lex import *
from parse import *

print("Test del file lexer.py")

# entrada = "LET foobar = 123"
# fuente = Lexer(entrada)

# while fuente.peek() != '\0':
#     print(fuente.curChar)
#     fuente.nextChar()

cadena = "program factorial\n{\n\t# decalrations #\n\tdeclare x;\n\tdeclare i, fact;\n\n\n\t# main #\n\tinput(x);\n\tfact:=1;\n\ti:=1;\n\twhile(-x<=-i)\n\t{\n\t\tfact:=fact*i;\n\t\ti:=i+1;\n\t};\n\tprint(fact);\n}."

print ("----------------------\n" + cadena + "\n----------------------")

## Test cadena

# for i in cadena:
#     code = str(ord(i))
#     print(i + ":\t" + code)

lexer = Lexer(cadena)
parser = Parser(lexer)

## Test del lexer

# token = lexer.getToken()
# while token[0] != "EOF":
#     print(token[0])
#     token = lexer.getToken()

print("##########")

parser.program()

print("Parsing complete.")
