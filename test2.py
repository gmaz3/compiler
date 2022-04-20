# -*- coding: utf-8 -*-

from parse import *

def main():
    print("Test")
    
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
    
    print("Testing Program Class")
    
    contextStack = []
    main = Program("main", [])
    print("sub: " + str(main))
    sub = Program("fibo", ["x", "r"])
    print("sub: " + str(sub))
    
    main.addSubprogram(sub)
    
    
    print(str(main.programs))
    
    if main.checkCallPosible("fibo", 1):
        print("is possible to call functin " + sub.id)
    else:
        print("is not possible to call function " + sub.id)
    # contextStack.append(main)
    
    # main.addVariable("var1")
    
    # a = contextStack[-1]
    
    # a.addVariable("var2")
    
    # main_vars = main.vars
    # a_vars = a.vars
    
    # print("Main vars:")
    # print(main_vars)
    # print("A vars:")
    # print(a_vars)
    
    a = "adios"
    a = a[0:-2]
        
        
main()