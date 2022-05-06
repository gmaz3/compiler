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
    def __init__(self, identifier, parameters, prog_type):
        self.id = identifier        # subprogram id
        self.params = []    # subprogram parameters, is a list of Paramenter; there are two types: in(True), inout(False)
        self.vars = []              # variables declared inside the program context
        self.programs = []          # subprograms declared inside the program context
        self.type = prog_type       # whether the program is a function or is a procedure

        self.programs.append(self)

        for i in parameters:        # fill vars list up
            self.params.append(i)
            self.vars.append(i.id)

    # Check if var_id is already defined in the program context. true -> is defined; false -> is not defined
    def checkVarDefined(self, var_id):
        return self.vars.count(var_id) != 0

    # Check if is posible to call func_id, with parameters in the func_params list.
    def checkCallPosible(self, func_id, params_type, prog_type): # params_type is a list with the type of every parameter
        for subprog in self.programs:
            # print(str(subprog))
            if subprog.id == func_id and subprog.type == prog_type:
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
        if not self.checkCallPosible(subpr.id, subpr.params, subpr.type):
            self.programs.append(subpr)


class Parser:
    def __init__(self, lexer, intercod):
        self.lexer = lexer
        self.curToken  = None  # curToken[0] store token kind, curToken store the token symbol
        self.peekToken = None
        self.treeView  = False
        self.contextStack = [] # Stack of program istances that store the vars, and subprograms of the current program. I have used the list as a stack
        self.intercod = intercod

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

    def checkCallPosible(self, func_id, params_type, func_type):
        for i in reversed(self.contextStack):
            if i.checkCallPosible(func_id, params_type, func_type):
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
                main = Program(self.curToken[1],[],None)
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
            if self.checkToken("FUNC"):
                prog_type = 'f'
            else:
                prog_type = 'p'
                
            self.nextToken()

            sub_id = self.curToken[1]

            self.match("ID")
            self.match("OPAR")
            params = self.formalparlist()
            self.match("CPAR")
            sub = Program(sub_id, params, prog_type)
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
        # elif self.checkToken("INCS"):
        #     self.incaseStat()
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
            asig_var = self.curToken[1]
            if self.checkVarDefined(asig_var):
                self.nextToken()
                self.nextToken()
                e_place = self.expression()
                self.intercod.addQuad("ASIG",e_place,None,asig_var)
                self.intercod.freeTmpVar(e_place)
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
            cond = self.condition()
            self.match("CPAR")
            
            end_if = self.intercod.newLabel()
            self.intercod.freeTmpVar(cond)
            self.intercod.addQuad("IFN_GOTO",cond,None,end_if)
            
            self.statements()

            isThereElse = self.checkToken("ELSE")
            
            if isThereElse:
                end_else = self.intercod.newLabel()
                self.intercod.addQuad("GOTO",end_else,None,None)
                        
            self.intercod.addQuad("LAB",end_if,None,None)
            
            self.elsepart()
            
            if isThereElse:
                self.intercod.addQuad("LAB",end_else,None,None)
            
            
            
            # self.intercod.slideQuads(if_start,if_end)
            
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
            start_while = self.intercod.newLabel()
            end_while   = self.intercod.newLabel()
            self.intercod.addQuad("LAB",start_while,None,None)
            cond = self.condition()
            self.intercod.freeTmpVar(cond)
            self.intercod.addQuad("IFN_GOTO",cond,None,end_while)            
            self.match("CPAR")
            
            self.statements()
            
            self.intercod.addQuad("GOTO",start_while,None,None)
            self.intercod.addQuad("LAB",end_while,None,None)
        
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

            end_switch = self.intercod.newLabel()
            labels = []

            while self.checkToken("CASE"):
                labels.append(self.intercod.newLabel())
                self.nextToken()
                self.match("OPAR")
                cond = self.condition()
                self.match("CPAR")
                self.intercod.addQuad("IFN_GOTO",cond,labels[-1],None)
                self.statements()
                self.intercod.addQuad("GOTO",end_switch,None,None)
                self.intercod.addQuad("LAB",labels[-1],None,None)
                
            self.match("DFLT")
            self.statements()
            self.intercod.addQuad("LAB",end_switch,None,None)

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
            
            start_forcase = self.intercod.newLabel()
            labels = []
            
            self.intercod.addQuad("LAB",start_forcase,None,None)

            while self.checkToken("CASE"):
                labels.append(self.intercod.newLabel())
                self.nextToken()
                self.match("OPAR")
                cond = self.condition()
                self.match("CPAR")
                self.intercod.addQuad("IFN_GOTO",cond,labels[-1],None)
                self.statements()
                self.intercod.addQuad("GOTO",start_forcase,None,None)
                self.intercod.addQuad("LAB",labels[-1],None,None)

            self.match("DFLT")
            self.statements()
        
        decreaseIndexSpace()

    # incaseStat syntax
    # incase ( case ( condition ) statements)*
    # def incaseStat(self):
    #     if self.treeView:
    #         print(index_space + "INCASE")
    #     increaseIndexSpace()
    #     if self.checkToken("INCS"):
    #         self.nextToken()

    #         while self.checkToken("CASE"):
    #             self.nextToken()
    #             self.match("OPAR")
    #             self.condition()
    #             self.match("CPAR")
    #             self.statements()
    #     decreaseIndexSpace()

    # returnStat syntax
    #   return ( expression )
    def returnStat(self):
        if self.treeView:
            print(index_space + "RETURNSTAT")
            
        increaseIndexSpace()
        
        if self.checkToken("RET"):
            self.nextToken()
            self.match("OPAR")
            e_place = self.expression()
            self.match("CPAR")
            
            self.intercod.addQuad("RET",e_place,None,None)
        
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

            if not self.checkCallPosible(func_id, par_list, 'p'):
                self.abort("Problem calling the function " + func_id + ". Check if the function has been defined and if the number of arguments is correct and check the type of each parameter.")

            self.intercod.addQuad("CALL",func_id,None,None)
                
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
            e_place = self.expression()
            self.match("CPAR")
            self.intercod.addQuad("PRINT",e_place,None,None)
            
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
            var = self.curToken[1]
            
            if self.checkVarDefined(var):
                self.match("ID")
            else:
                self.abort("Variable " + var + " has not been defined.")
                
            self.match("CPAR")
            
            self.intercod.addQuad("INPUT",None,None,var)
            
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
            item = self.actualparitem()
            par_list.append(item[1])
            
            if item[1]:
                mode = "VAL"
            else:
                mode = "REF"
                
            self.intercod.addQuad("PAR",item[0],mode,None)

            while self.checkToken("COM"):
                self.nextToken()
                item = self.actualparitem()
                par_list.append(item[1])
                
                if item[1]:
                    mode = "VAL"
                else:
                    mode = "REF"
                    
                self.intercod.addQuad("PAR",item[0],mode,None)

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
            e_place = self.expression()
            return [e_place, True]
        elif self.checkToken("INOUT"):
            self.nextToken()
            var = self.curToken[1]
            if self.checkVarDefined(var):
                self.match("ID")
                return [var, False]
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
        e1_place = self.boolterm()

        while self.checkToken("OR"):
            e2_place = self.boolterm()
            self.intercod.freeTmpVar(e1_place)
            self.intercod.freeTmpVar(e2_place)
            w = self.intercod.newTmpVar()
            self.intercod.addQuad("OR",e1_place,e2_place,w)
            e1_place = w
            
        decreaseIndexSpace()
        return e1_place

    # boolterm syntax
    #   boolfactor ( and boolfactor )*
    def boolterm(self):
        if self.treeView:
            print(index_space + "BOOLTERM")
            
        increaseIndexSpace()
        e1_place = self.boolfactor()

        while self.checkToken("AND"):
            e2_place = self.boolfactor()            
            self.intercod.freeTmpVar(e1_place)
            self.intercod.freeTmpVar(e2_place)
            w = self.intercod.newTmpVar()
            self.intercod.addQuad("AND",e1_place,e2_place,w)
            e1_place = w

        decreaseIndexSpace()
        return e1_place

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
            e_place = self.intercod.newTmpVar()
            e1_place = self.condition()
            self.intercod.freeTmpVar(e1_place)
            self.intercod.addQuad("NOT",e1_place,None,e_place)
            self.match("CBRA")
            
        elif self.checkToken("OBRA"):
            self.nextToken()
            e_place = self.condition()
            self.match("CBRA")
            
        else:
            e_place = self.intercod.newTmpVar()
            
            e1_place = self.expression()
            relop = self.rel_op() # store the relop token 
            e2_place = self.expression()
            
            self.intercod.freeTmpVar(e1_place)
            self.intercod.freeTmpVar(e2_place)
            
            self.intercod.addQuad(relop[0],e1_place,e2_place,e_place)
            
        decreaseIndexSpace()
        return e_place

    # expression syntax
    # optionalSign term (ADD_OP term)*
    def expression(self):
        if self.treeView:
            print(index_space + "EXPRESSION")
        increaseIndexSpace()
        # print("entro expresion")
        
        minsign = self.optionalSign() # completar esta parte
        e1_place = self.term(minsign)

        while(self.checkToken("PLUS") or self.checkToken("MINUS")):
            token = self.curToken[0]
            self.nextToken()
            e2_place = self.term(False)
            self.intercod.freeTmpVar(e1_place)
            self.intercod.freeTmpVar(e2_place)
            w = self.intercod.newTmpVar()
            self.intercod.addQuad(token,e1_place,e2_place,w)
            e1_place = w
            

        decreaseIndexSpace()
        # self.intercod.freeTmpVar()
        # self.intercod.freeTmpVar()
        return e1_place # w usually
        # print("salgo expresion")


    # term syntax
    #   factor (MULT_OP factor)*
    def term(self,minsign):
        if self.treeView:
            print(index_space + "TERM")
            
        increaseIndexSpace()
        e1_place = self.factor(minsign)

        while(self.checkToken("MULT") or self.checkToken("DIV")):
            token = self.curToken[0]
            self.nextToken()
            e2_place = self.factor(False)
            self.intercod.freeTmpVar(e1_place)
            self.intercod.freeTmpVar(e2_place)
            w = self.intercod.newTmpVar()
            self.intercod.addQuad(token,e1_place,e2_place,w)
            e1_place = w

        decreaseIndexSpace()
        # self.intercod.freeTmpVar()
        # self.intercod.freeTmpVar()
        return e1_place # w usually

    # factor syntax
    #   INTEGER
    #   | or |
    #   ( expression )
    #   | or |
    #   ID idtail
    def factor(self,minsign):
        if self.treeView:
            print(index_space + "FACTOR")
            
        increaseIndexSpace()
            
        if self.checkToken("NUMB"):
            
            if minsign:
                e_place = self.intercod.newTmpVar()
                e1_place = self.curToken[1]
                self.intercod.addQuad("UMINUS",e1_place,None,e_place)
            else:
                e_place = self.curToken[1]
                
            self.nextToken()
            return e_place
        
        elif self.checkToken("OPAR"):
            
            if minsign:
                self.nextToken()
                e_place = self.intercod.newTmpVar()
                e1_place = self.expression()
                self.match("CPAR")
                self.intercod.addQuad("UMINUS",e1_place,None,e_place)
            else:
                self.nextToken()
                e_place = self.expression()
                self.match("CPAR")
            
            return e_place
        
        elif self.checkToken("ID"):
            # print(self.contextStack[-1].programs)
            ident = self.curToken[1]
            self.nextToken()
            params = self.idtail()

            if not self.checkVarDefined(ident) and not self.checkCallPosible(ident, params, 'f'): #Semantic analysis
                self.abort("System expected a function or variable, but " + ident + " has not been defined.")
                
            if params == None: # if is not a function call then
            
                if minsign:
                    e_place = self.intercod.newTmpVar()
                    e1_place = ident
                    self.intercod.addQuad("UMINUS",e1_place,None,e_place)
                else:
                    e_place = ident
                    
                return e_place
            else:
                w = self.intercod.newTmpVar()
                self.intercod.addQuad("PAR",w,"RET",None)
                self.intercod.addQuad("CALL",ident,None,None)
                return w
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
        minus_sign = self.checkToken("MINUS")
        plus_sign = self.checkToken("PLUS")
        
        if plus_sign or minus_sign:
            self.nextToken()
            
        return minus_sign

    # rel_op syntax
    #   = | <= | >= | > | < | <>
    def rel_op(self):
        tkn = self.curToken
        
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
            
        return tkn

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
