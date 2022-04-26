# -*- coding: utf-8 -*-

# Used for seeing the compilation as a tree
###########################################
###########################################

index_space = ""

def decreaseIndexSpace():
    global index_space
    index_space = index_space[0:-1]

def increaseIndexSpace():
    global index_space
    index_space = index_space + "\t"


###########################################
###########################################

import sys
from lex import *


class Parameter:
    def __init__(self,par_id, par_type):
        self.id = par_id
        self.type = par_type # True: means is 'in' param, False: means is a 'inout'

# Management of the validity of the function calls and the use of variables
# This class is used in order to check if function calls are correct, for instance we used it to check if the function is already defined
# if the number of parameters in the call is correct. Also when we used a variable if the variable has been defined before.
class Program:
    def __init__(self, identifier, parameters):
        self.id = identifier        # subprogram id
        self.params = []    # subprogram parameters, is a list of Paramenter; there are two types: in(True), inout(False)
        self.vars = []              # variables declared inside the program context
        self.programs = []          # subprograms declared inside the program context

        self.programs.append(self)

        for i in parameters:        # fill vars list up
            self.params.append(i)
            self.vars.append(i.id)

    # Check if var_id is already defined in the program context. true -> is defined; false -> is not defined
    def checkVarDefined(self, var_id):
        return self.vars.count(var_id) != 0

    # Check if is posible to call func_id, with parameters in the func_params list.
    def checkCallPosible(self, func_id, params_type): # params_type is a list with the type of every parameter
        for subprog in self.programs:
            # print(str(subprog))
            if subprog.id == func_id:
                nop = len(subprog.params)
                if nop == len(params_type): #number of parameters
                    # print("es posible hacer la llamada a la funcion " + func_id)
                    for i in range(nop):
                        if subprog.params[i].type != params_type[i]:
                            return False
                    return True

        return False

    # Append variable to defined variables list
    def addVariable(self, var_id):
        if not self.checkVarDefined(var_id):
            self.vars.append(var_id)

    # Append program to defined program list
    def addSubprogram(self, subpr):
        # print("programas de self: " + str(self.programs))
        if not self.checkCallPosible(subpr.id, subpr.params):
            self.programs.append(subpr)


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.curToken  = None  # curToken[0] store token kind, curToken store the token symbol
        self.peekToken = None
        self.treeView  = False
        self.contextStack = [] # Stack of program istances that store the vars, and subprograms of the current program. I have used the list as a stack

        self.nextToken()
        self.nextToken()

    # Return true if the current token matches
    def checkToken(self, kind):
        return kind == self.curToken[0]

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken[0]

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind + ", got " + self.curToken[1] + " token readed as" + self.curToken[0])
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # print("Token actual: " + str(self.curToken)) # descomentar
        # print("Contexto actual: " + str(self.contextStack))
        # print("Variables definidas en el contexto actual: " + str(self.contextStack[-1].vars))

        # for i in self.contextStack:
        #     print("Subprogramas de " + str(i) + ":\n\t" + str(i.programs))

    def abort(self, message):
        sys.exit("Error. " + message)


    # Context management functions


    def addVariable(self, ident):
        self.contextStack[-1].addVariable(ident)

    def addSubprogram(self, prog):
        self.contextStack[-1].addSubprogram(prog)
    
    def checkVarDefined(self, var_id):
        for i in reversed(self.contextStack):
            if i.checkVarDefined(var_id):
                return True
        return False

    def checkCallPosible(self, func_id, params_type):
        for i in reversed(self.contextStack):
            if i.checkCallPosible(func_id, params_type):
                return True
        return False
            
    # Tree view functions
    
    def activateTreeView(self):
        self.treeView = True
        
    def deactivateTreeView(self):
        self.treeView = False

    # Syntax related functions

    # program syntax
    # program ID
    #   block
    # .
    def program(self):
        if self.treeView:
            print(index_space + "PROGRAM")
        increaseIndexSpace()
        if self.checkToken("PROG"):
            self.nextToken()

            if self.checkToken("ID"):
                main = Program(self.curToken[1],[])
                self.contextStack.append(main)
                self.nextToken()

            self.block()
            self.match("EOP")
        else:
            self.abort("Program does not start as expected.")
        decreaseIndexSpace()

    # block syntax
    # {
    #   declarations
    #   subprograms
    #   blockstatements
    # }
    def block(self):
        if self.treeView:
            print(index_space + "BLOCK")
        increaseIndexSpace()
        if self.checkToken("OCB"):
            self.nextToken()

            self.declarations()
            self.subprograms()
            self.blockstatements()

            self.match("CCB")
        else:
            self.abort("System expected to read a block.")
        decreaseIndexSpace()

    # declarations syntax
    # ( declare varlist ; )*
    def declarations(self):
        if self.treeView:
            print(index_space + "DECLARATIONS")
        increaseIndexSpace()
        while self.checkToken("DECL"):
            self.nextToken()

            self.varlist()
            self.match("SMCOL")
        decreaseIndexSpace()

    # varlist syntax
    # ID (, ID)* | E
    def varlist(self):
        if self.treeView:
            print(index_space + "VARLIST")
        increaseIndexSpace()
        if self.checkToken("ID"):
            self.addVariable(self.curToken[1])
            self.nextToken()

            while self.checkToken("COM"):
                self.nextToken()
                self.addVariable(self.curToken[1])
                self.match("ID")
        decreaseIndexSpace()

    # subprograms syntax
    # (subprogram)*
    def subprograms(self):
        if self.treeView:
            print(index_space + "SUBPROGRAMS")
        increaseIndexSpace()
        while self.checkToken("FUNC") or self.checkToken("PROC"):
            self.subprogram()
        decreaseIndexSpace()

    # subprogram syntax
    # function ID ( formalparlist )
    #   block
    # | or |
    # procedure ID ( formalparlist )
    #   block
    def subprogram(self):
        if self.treeView:
            print(index_space + "SUBPROGRAM")
        increaseIndexSpace()
        if self.checkToken("FUNC") or self.checkToken("PROC"):
            self.nextToken()

            sub_id = self.curToken[1]

            self.match("ID")
            self.match("OPAR")
            params = self.formalparlist()
            self.match("CPAR")
            sub = Program(sub_id, params)
            self.addSubprogram(sub)
            self.contextStack.append(sub)
            # print("hago un push en la pila")
            self.block()
            self.contextStack.pop()
            # print("hago un pop en la pila")
        else:
            self.abort("System expected a subprogram here.")
        decreaseIndexSpace()


    # formalparlist syntax
    #   formalparitem (, formalparitem)* | E
    def formalparlist(self):
        if self.treeView:
            print(index_space + "FORMALPARLIST")
        increaseIndexSpace()
        params = []
        if self.checkToken("IN") or self.checkToken("INOUT"):
            new_par = self.formalparitem()
            params.append(new_par)
            self.addVariable(new_par.id)

            while self.checkToken("COM"):
                self.nextToken()
                new_par = self.formalparitem()
                params.append(new_par)
                self.addVariable(new_par.id)

        decreaseIndexSpace()
        return params

    # formalparitem syntax
    # in ID | inout ID
    def formalparitem(self):
        if self.treeView:
            print(index_space + "FORMALPARITEM")
        increaseIndexSpace()
        var_id = None

        if self.checkToken("IN"):
            self.nextToken()
            var_id = self.curToken[1]
            var_tp = True
            self.match("ID")
        elif self.checkToken("INOUT"):
            self.nextToken()
            var_id = self.curToken[1]
            var_tp = False
            self.match("ID")
        else:
            self.abort("System expected a formal parameter.")

        decreaseIndexSpace()
        return Parameter(var_id, var_tp)

    # statements syntax
    # statement ;
    # | or |
    # {
    #   statement (; statement)*
    # }
    def statements(self):
        if self.treeView:
            print(index_space + "STATEMENTS")
        increaseIndexSpace()
        if self.checkToken("OCB"):
            self.nextToken()

            self.statement()

            while self.checkToken("SMCOL"):
                self.nextToken()
                self.statement()

            self.match("CCB")
        else:
            self.statement()
            self.match("SMCOL")
        decreaseIndexSpace()

    # blockstatements syntax
    # statement ( ; statement )*
    def blockstatements(self):
        if self.treeView:
            print(index_space + "BLOCKSTATEMENTS")
        increaseIndexSpace()
        self.statement()

        while self.checkToken("SMCOL"):
            self.nextToken()

            self.statement()

        decreaseIndexSpace()

    # statement syntax
    # assignStat
    # | or |
    # ifStat
    # | or |
    # whileStat
    # | or |
    # switchcaseStat
    # | or |
    # forcaseStat
    # | or |
    # incaseStat
    # | or |
    # callStat
    # | or |
    # returnStat
    # | or |
    # inputStat
    # | or |
    # printStat
    # | or |
    # E (empty)
    def statement(self):
        if self.treeView:
            print(index_space + "STATEMENT")
        increaseIndexSpace()
        if self.checkToken("ID"):
            self.assignStat()
        elif self.checkToken("IF"):
            self.ifStat()
        elif self.checkToken("WHILE"):
            self.whileStat()
        elif self.checkToken("SWITCH"):
            self.switchcaseStat()
        elif self.checkToken("FOR"):
            self.forcaseStat()
        elif self.checkToken("INCS"):
            self.incaseStat()
        elif self.checkToken("CALL"):
            self.callStat()
        elif self.checkToken("RET"):
            self.returnStat()
        elif self.checkToken("INPUT"):
            self.inputStat()
        elif self.checkToken("PRINT"):
            self.printStat()
        decreaseIndexSpace()

    # assignStat syntax
    # ID := expresion
    def assignStat(self):
        if self.treeView:
            print(index_space + "ASSIGSTAT")
        increaseIndexSpace()
        if self.checkPeek("ASIG"):
            if self.checkVarDefined(self.curToken[1]):
                self.nextToken()
                self.nextToken()
                self.expression()
            else:
                self.abort("Variable " + self.curToken[1] + " has not been defined yet.")
        else:
            self.abort("System expected to read ':=' operator.")
        decreaseIndexSpace()

    # ifStat syntax
    # if ( condition )
    #   statements
    # elsepart
    def ifStat(self):
        if self.treeView:
            print(index_space + "IFSTAT")
        increaseIndexSpace()
        if self.checkToken("IF"):
            self.nextToken()
            self.match("OPAR")
            self.condition()
            self.match("CPAR")
            self.statements()
            self.elsepart()
        decreaseIndexSpace()

    # elsepart syntax
    # else
    #   statements
    # | or |
    # E
    def elsepart(self):
        if self.treeView:
            print(index_space + "ELSEPART")
        increaseIndexSpace()
        if self.checkToken("ELSE"):
            self.nextToken()
            self.statements()
        decreaseIndexSpace()

    # whileStat syntax
    # while ( condition )
    #   statements
    def whileStat(self):
        if self.treeView:
            print(index_space + "WHILESTAT")
        increaseIndexSpace()
        if self.checkToken("WHILE"):
            self.nextToken()
            self.match("OPAR")
            self.condition()
            self.match("CPAR")
            self.statements()
        decreaseIndexSpace()

    # switchcaseStat syntax
    # switchcase ( case ( condition ) statements )*
    #   default statements
    def switchcaseStat(self):
        if self.treeView:
            print(index_space + "SWITCHCASESTAT")
        increaseIndexSpace()
        if self.checkToken("SWITCH"):
            self.nextToken()

            while self.checkToken("CASE"):
                self.nextToken()
                self.match("OPAR")
                self.condition()
                self.match("CPAR")
                self.statements()

            self.match("DFLT")
            self.statements()

        decreaseIndexSpace()


    # forcaseStat syntax
    # forcase ( case ( condition ) statements)*
    #   default statements
    def forcaseStat(self):
        if self.treeView:
            print(index_space + "FORCASESTAT")
        increaseIndexSpace()
        if self.checkToken("FOR"):
            self.nextToken()

            while self.checkToken("CASE"):
                self.nextToken()
                self.match("OPAR")
                self.condition()
                self.match("CPAR")
                self.statements()

            self.match("DFLT")
            self.statements()
        decreaseIndexSpace()

    # incaseStat syntax
    # incase ( case ( condition ) statements)*
    def incaseStat(self):
        if self.treeView:
            print(index_space + "INCASE")
        increaseIndexSpace()
        if self.checkToken("INCS"):
            self.nextToken()

            while self.checkToken("CASE"):
                self.nextToken()
                self.match("OPAR")
                self.condition()
                self.match("CPAR")
                self.statements()
        decreaseIndexSpace()

    # returnStat syntax
    #   return ( expression )
    def returnStat(self):
        if self.treeView:
            print(index_space + "RETURNSTAT")
        increaseIndexSpace()
        if self.checkToken("RET"):
            self.nextToken()
            self.match("OPAR")
            self.expression()
            self.match("CPAR")
        decreaseIndexSpace()

    # callStat syntax
    # call ID( actualparlist )
    def callStat(self):
        if self.treeView:
            print(index_space + "CALLSTAT")
        increaseIndexSpace()
        if self.checkToken("CALL"):
            self.nextToken()
            func_id = self.currentToken[1]
            self.match("ID")
            self.match("OPAR")
            par_list = self.actualparlist()
            self.match("CPAR")

            if not self.checkCallPosible(func_id, par_list):
                self.abort("Problem calling the function " + func_id + ". Check if the function has been defined and if the number of arguments is correct and check the type of each parameter.")
        decreaseIndexSpace()

    # printStat syntax
    #   print( expression )
    def printStat(self):
        if self.treeView:
            print(index_space + "PRINTSTAT")
        increaseIndexSpace()
        if self.checkToken("PRINT"):
            self.nextToken()
            self.match("OPAR")
            self.expression()
            self.match("CPAR")
        decreaseIndexSpace()

    # inputStat syntax
    #   input ( ID )
    def inputStat(self):
        if self.treeView:
            print(index_space + "INPUTSTAT")
        increaseIndexSpace()
        if self.checkToken("INPUT"):
            self.nextToken()
            self.match("OPAR")
            if self.checkVarDefined(self.curToken[1]):
                self.match("ID")
            else:
                self.abort("Variable " + self.curToken[1] + " has not been defined.")
            self.match("CPAR")
        decreaseIndexSpace()

    # actualparlist syntax
    #   actualparitem ( , actualparitem )*
    # | or |
    # E
    def actualparlist(self):
        if self.treeView:
            print(index_space + "ACTUALPARLIST")
        increaseIndexSpace()
        par_list = []
        if self.checkToken("IN") or self.checkToken("INOUT"):
            par_list.append(self.actualparitem())

            while self.checkToken("COM"):
                self.nextToken()
                par_list.append(self.actualparitem())

        decreaseIndexSpace()
        return par_list

    # acutalparitem syntax
    #   in expression | inout ID
    def actualparitem(self):
        if self.treeView:
            print(index_space + "ACTUALPARITEM")
        increaseIndexSpace()
        if self.checkToken("IN"):
            self.nextToken()
            self.expression()
            return True
        elif self.checkToken("INOUT"):
            self.nextToken()
            if self.checkVarDefined(self.curToken[1]):
                self.match("ID")
                return False
            else:
                self.abort("Variable " + self.curToken[1] + " has not been defined.")
        else:
            self.abort("System expected a in or inout token.")
        decreaseIndexSpace()


    # condition syntax
    #   boolterm ( or boolterm )*
    def condition(self):
        if self.treeView:
            print(index_space + "CONDITION")
        increaseIndexSpace()
        self.boolterm()

        while self.checkToken("OR"):
            self.boolterm()
        decreaseIndexSpace()

    # boolterm syntax
    #   boolfactor ( and boolfactor )*
    def boolterm(self):
        if self.treeView:
            print(index_space + "BOOLTERM")
        increaseIndexSpace()
        self.boolfactor()

        while self.checkToken("AND"):
            self.boolfactor()

        decreaseIndexSpace()

    # boolfactor syntax
    #   not [ condition ]
    # | or |
    #   [ condition ]
    # | or |
    #   expression REL_OP expression
    def boolfactor(self):
        if self.treeView:
            print(index_space + "BOOLFACTOR")
        increaseIndexSpace()
        if self.checkToken("NOT"):
            self.nextToken()
            self.match("OBRA")
            self.condition()
            self.match("CBRA")
        elif self.checkToken("OBRA"):
            self.nextToken()
            self.condition()
            self.match("CBRA")
        else:
            self.expression()
            self.rel_op()
            self.expression()
        decreaseIndexSpace()

    # expression syntax
    # optionalSign term (ADD_OP term)*
    def expression(self):
        if self.treeView:
            print(index_space + "EXPRESSION")
        increaseIndexSpace()
        # print("entro expresion")
        self.optionalSign()
        self.term()

        while(self.checkToken("PLUS") or self.checkToken("MINUS")):
            # print("Symbol + or -")
            self.nextToken()
            self.term()

        decreaseIndexSpace()
        # print("salgo expresion")


    # term syntax
    #   factor (MULT_OP factor)*
    def term(self):
        if self.treeView:
            print(index_space + "TERM")
        increaseIndexSpace()
        self.factor()

        while(self.checkToken("MULT") or self.checkToken("DIV")):
            self.nextToken()
            self.factor()

        decreaseIndexSpace()

    # factor syntax
    #   INTEGER
    #   | or |
    #   ( expression )
    #   | or |
    #   ID idtail
    def factor(self):
        if self.treeView:
            print(index_space + "FACTOR")
        increaseIndexSpace()
        if self.checkToken("NUMB"):
            self.nextToken()
        elif self.checkToken("OPAR"):
            self.nextToken()
            self.expression()
            self.match("CPAR")
        elif self.checkToken("ID"):
            # print(self.contextStack[-1].programs)
            ident = self.curToken[1]
            self.nextToken()
            params = self.idtail()
            # print("llamada a id: " + ident + ", numero de param: " + str(num_params))
            # print(str(self.checkCallPosible(ident, num_params)))
            # print("function id: " + str(self.contextStack[-1].programs[-1].id) + ", numero de param: " + str(len(self.contextStack[-1].programs[-1].params)))
            # print(params)
            if not self.checkVarDefined(ident) and not self.checkCallPosible(ident, params):
                self.abort("System expected a function or variable, but " + ident + " has not been defined.")
            # print("--> realizada la llamada")
        else:
            self.abort("Syntax expected a factor, starting by a ID or NUMBER token or '(' symbol. ")

        decreaseIndexSpace()

    # idtail syntax
    # ( actualparlist ) | E
    def idtail(self):
        if self.treeView:
            print(index_space + "IDTAIL")
        increaseIndexSpace()
        par_type = None
        if self.checkToken("OPAR"): # then is a function call
            # print("entro idtail")
            self.nextToken()
            par_type = self.actualparlist()
            self.match("CPAR")
            # print("salgo idtail")

        decreaseIndexSpace()
        return par_type

    # optionalSign syntax
    #   ADD_OP | E
    def optionalSign(self):
        if self.checkToken("PLUS") or self.checkToken("MINUS"):
            self.nextToken()

    # rel_op syntax
    #   = | <= | >= | > | < | <>
    def rel_op(self):
        if self.checkToken("EQ"):
            self.nextToken()
        if self.checkToken("LTEQ"):
            self.nextToken()
        if self.checkToken("GTEQ"):
            self.nextToken()
        if self.checkToken("LT"):
            self.nextToken()
        if self.checkToken("GT"):
            self.nextToken()
        if self.checkToken("NOTEQ"):
            self.nextToken()

    # add_op syntax
    #   + | -
    def add_op(self):
        if self.checkToken("PLUS"):
            self.nextToken()
        if self.checkToken("MINUS"):
            self.nextToken()

    # mul_op syntax
    #   * | /
    def mul_op(self):
        if self.checkToken("MULT"):
            self.nextToken()
        if self.checkToken("DIV"):
            self.nextToken()
