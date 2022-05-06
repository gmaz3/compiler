# -*- coding: utf-8 -*-

from intercodgen import *
import re

def main(*argv):
    print("Test")

    a = IntermediateCode()
    
    a.addQuad("0", None, None, None)
    a.addQuad("1", None, None, None)
    a.addQuad("2", None, None, None)
    a.addQuad("3", None, None, None)
    a.addQuad("4", None, None, None)
    a.addQuad("5", None, None, None)
    a.addQuad("6", None, None, None)

    a.slideQuads(3, 5)
    
    print(a.quads)

    # variables = []
    
    # variables.append("fibonacci")
    # variables.append("factorial")
    # variables.append("porcamadona")
    # variables.append("fibonacci")

    
    # print(variables)
    # print(len(variables))
        
    # nm = variables.count("fibonacci")
    
    # if (nm) == 0:
    #     print("No encontrado\n")
    # else:
    #     print("Encontrado\t" + str(nm) + " veces")

    
    # main.addVariable("var1")
    
    # a = contextStack[-1]
    
    # a.addVariable("var2")
    
    # main_vars = main.vars
    # a_vars = a.vars
    
    # print("Main vars:")
    # print(main_vars)
    # print("A vars:")
    # print(a_vars)
    
    a = IntermediateCode()
    a.addQuad("x","d","d","t")
        
        
main()