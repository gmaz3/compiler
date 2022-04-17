# -*- coding: utf-8 -*-

import sys
from lex import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.curToken  = None
        self.peekToken = None
        
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
            self.abort("Expected " + kind + ", got " + self.curToken[0])
        self.nextToken()
    
    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # print("Token actual: " + str(self.curToken)) # descomentar
    
    def abort(self, message):
        sys.exit("Error. " + message)
        
    # program syntax
    # program ID
    #   block
    # .
    def program(self):
        if self.checkToken("PROG"):
            self.nextToken()
            
            self.match("ID")
            self.block()
            self.match("EOP")
        else:
            self.abort("Program does not start as expected.")

    # block syntax
    # {
    #   declarations
    #   subprograms
    #   blockstatements
    # }
    def block(self):
        if self.checkToken("OCB"):
            self.nextToken()
            
            self.declarations()
            self.subprograms()
            self.blockstatements()
            
            self.match("CCB")
        else:
            self.abort("System expected to read a block.")
    
    # declarations syntax
    # ( declare varlist ; )*
    def declarations(self):
        while self.checkToken("DECL"):
            self.nextToken()
            
            self.varlist()
            self.match("SMCOL")
            
    # varlist syntax
    # ID (, ID)* | E
    def varlist(self):
        if self.checkToken("ID"):
            self.nextToken()
            
            while self.checkToken("COM"):
                self.nextToken()
                self.match("ID")

    # subprograms syntax
    # (subprogram)*
    def subprograms(self):
        while self.checkToken("FUNC") or self.checkToken("PROC"):
            self.subprogram()
            
    # subprogram syntax
    # function ID ( formalparlist )
    #   block
    # | or |
    # procedure ID ( formalparlist )
    #   block
    def subprogram(self):
        if self.checkToken("FUNC") or self.checkToken("PROC"):
            self.nextToken()
            
            self.match("ID")
            self.match("OPAR")
            self.formalparlist()
            self.match("CPAR")
            self.block()
        else:
            self.abort("System expected a subprogram here.")
        
            
    # formalparlist syntax
    #   formalparitem (, formalparitem)* | E
    def formalparlist(self):
        self.formalparitem()
        
        while self.checkToken("COM"):
            self.nextToken()
            self.formalparitem()
        
    # formalparitem syntax
    # in ID | inout ID
    def formalparitem(self):
        if self.checkToken("IN") or self.checkToken("INOUT"):
            self.nextToken()
            self.match("ID")
        else:
            self.abort("System expected a formal parameter.")
            
    # statements syntax
    # statement ;
    # | or |
    # {
    #   statement (; statement)*
    # }
    def statements(self):
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
            
    # blockstatements syntax
    # statement ( ; statement )*
    def blockstatements(self):
        self.statement()
        
        while self.checkToken("SMCOL"):
            self.nextToken()
            self.statement()
    
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
            
    # assignStat syntax            
    # ID := expresion
    def assignStat(self):
        if self.checkPeek("ASIG"):
            self.nextToken()
            self.nextToken()
            self.expression()
        else:
            self.abort("System expected a id.")
            
    # ifStat syntax
    # if ( condition )
    #   statements
    # elsepart
    def ifStat(self):
        if self.checkToken("IF"):
            self.nextToken()
            self.match("OPAR")
            self.condition()
            self.match("CPAR")
            self.statements()
            self.elsepart()
            
    # elsepart syntax
    # else
    #   statements
    # | or |
    # E
    def elsepart(self):        
        if self.checkToken("ELSE"):
            self.nextToken()
            self.statements()
            
    # whileStat syntax
    # while ( condition )
    #   statements
    def whileStat(self):
        if self.checkToken("WHILE"):
            self.nextToken()
            self.match("OPAR")
            self.condition()
            self.match("CPAR")
            self.statements()
            
    # switchcaseStat syntax
    # switchcase ( case ( condition ) statements )*
    #   default statements
    def switchcaseStat(self):
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
            
            
    # forcaseStat syntax
    # forcase ( case ( condition ) statements)*
    #   default statements
    def forcaseStat(self):
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
            
    # incaseStat syntax
    # incase ( case ( condition ) statements)*
    def incaseStat(self):
        if self.checkToken("INCS"):
            self.nextToken()
            
            while self.checkToken("CASE"):
                self.nextToken()
                self.match("OPAR")
                self.condition()
                self.match("CPAR")
                self.statements()
                
    # returnStat syntax
    #   return ( expression )
    def returnStat(self):
        if self.checkToken("RET"):
            self.nextToken()
            self.match("OPAR")
            self.expression()
            self.match("CPAR")
            
    # callStat syntax
    # call ID( actualparlist )
    def callStat(self):
        if self.checkToken("CALL"):
            self.nextToken()
            self.match("ID")
            self.match("OPAR")
            self.actualparlist()
            self.match("CPAR")
            
    # printStat syntax
    #   print( expression )
    def printStat(self):
        if self.checkToken("PRINT"):
            self.nextToken()
            self.match("OPAR")
            self.expression()
            self.match("CPAR")
            
    # inputStat syntax
    #   input ( ID )
    def inputStat(self):
        if self.checkToken("INPUT"):
            self.nextToken()
            self.match("OPAR")
            self.match("ID")
            self.match("CPAR")
            
    # actualparlist syntax
    #   actualparitem ( , actualparitem )*
    # | or |
    # E
    def actualparlist(self):
        if self.checkToken("IN") or self.checkToken("INOUT"):
            self.actualparitem()
            
            while self.checkToken("COM"):
                self.nextToken()
                self.actualparitem()
        
    # acutalparitem syntax
    #   in expression | inout ID
    def actualparitem(self):
        if self.checkToken("IN"):
            self.nextToken()
            self.expression()
        elif self.checkToken("INOUT"):
            self.nextToken()
            self.match("ID")
        else:
            self.abort("System expected a in or inout token.")
            
            
    # condition syntax
    #   boolterm ( or boolterm )*
    def condition(self):
        self.boolterm()
        
        while self.checkToken("OR"):
            self.boolterm()
            
    # boolterm syntax
    #   boolfactor ( and boolfactor )*
    def boolterm(self):
        self.boolfactor()
        
        while self.checkToken("AND"):
            self.boolfactor()
            
    # boolfactor syntax
    #   not [ condition ]
    # | or |
    #   [ condition ]
    # | or |
    #   expression REL_OP expression
    def boolfactor(self):
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
            
    # expression syntax
    # optionalSign term (ADD_OP term)*
    def expression(self):
        self.optionalSign()
        self.term()
        
        while(self.checkToken("PLUS") or self.checkToken("MINUS")):
            self.nextToken()
            self.term()
            
            
    # term syntax
    #   factor (MULT_OP factor)*
    def term(self):
        self.factor()
        
        while(self.checkToken("MULT") or self.checkToken("DIV")):
            self.nextToken()
            self.factor()
            
    # factor syntax
    #   INTEGER
    #   | or |
    #   ( expression )
    #   | or |
    #   ID idtail
    def factor(self):
        if self.checkToken("NUMB"):
            self.nextToken()
        elif self.checkToken("OPAR"):
            self.nextToken()
            self.expression()
            self.match("CPAR")
        elif self.checkToken("ID"):
            self.nextToken()
            self.idtail()
        else:
            self.abort("Syntax expected a factor, starting by a ID or NUMBER token or '(' symbol. ")
            
    # idtail syntax
    # ( actualparlist ) | E
    def idtail(self):
        if self.checkToken("OPAR"):
            self.nextToken()
            self.actualparlist()
            self.match("CPAR")
            
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
            
    