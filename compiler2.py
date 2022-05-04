# -*- coding: utf-8 -*-

from lex import *
from parse import *
from intercodgen import *
import sys

def main():
    print("Compiler C-imple")
    
    # if len(sys.argv) != 2:
    #     sys.exit("Error: Compiler needs source file as argument.")
    # with open(sys.argv[1], 'r') as inputFile:
    #     source = inputFile.read()
    
    file = open("test.cimp","r")
    
    source = file.read()
        
    lexer = Lexer(source)
    intercod = IntermediateCode()
    parser = Parser(lexer,intercod)
    
    # print ("----------------------\n" + source + "\n----------------------")
    
    # parser.activateTreeView()
    parser.program() # Start the parser
    print("Parsing complete.")
    for i in intercod.quads:
        print(i)
    
main()# -*- coding: utf-8 -*-

