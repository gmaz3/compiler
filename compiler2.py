# -*- coding: utf-8 -*-

from lex import *
from parse import *
import sys

def main():
    print("Compiler C-imple")
    
    # if len(sys.argv) != 2:
    #     sys.exit("Error: Compiler needs source file as argument.")
    # with open(sys.argv[1], 'r') as inputFile:
    #     source = inputFile.read()
    
    file = open("ex5.cimp","r")
    
    source = file.read()
        
    lexer = Lexer(source)
    parser = Parser(lexer)
    
    # print ("----------------------\n" + source + "\n----------------------")
    
    parser.activateTreeView()
    parser.program() # Start the parser
    print("Parsing complete.")
    
main()# -*- coding: utf-8 -*-

