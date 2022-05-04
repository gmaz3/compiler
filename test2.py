# -*- coding: utf-8 -*-

from intercodgen import *
import re

def main(*argv):
    print("Test")
    p = re.compile('t_[0-9]+')
    if p.match('t_43'):
        print("si se acepta")
    else:
        print("no se acepta")
    
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