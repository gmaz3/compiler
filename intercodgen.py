# -*- coding: utf-8 -*-

import re

class IntermediateCode:
    def __init__(self):
        self.quads = [] # list of all quads
        self.numqs = 0  # number of quads
        self.tempv = 0  # next temporal variable
        self.label = 0  # next label
        self.p = re.compile('t_[0-9]+')


    def addQuad(self,op,arg1,arg2,res): # add a quadruple to the intermediate code
        new_quad = [op]
        new_quad.append(arg1)
        new_quad.append(arg2)
        new_quad.append(res)

        self.quads.append(new_quad)
        self.numqs += 1

    def newTmpVar(self): # return the next temporal var
        tmp = "t_" + str(self.tempv)
        self.tempv += 1
        return tmp

    def freeTmpVar(self, var): # recycling temporal variables
        if self.p.match(var):
            self.tempv -= 1

    def nextLabel(self): # return the next label unused
        lab = self.label
        self.label += 1
        return lab