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
        
        return self.numqs

    def newTmpVar(self): # return the next temporal var
        tmp = "t_" + str(self.tempv)
        self.tempv += 1
        return tmp

    def freeTmpVar(self, var): # recycling temporal variables
        if self.p.match(var):
            self.tempv -= 1

    def newLabel(self): # return the next label unused
        lab = self.label
        self.label += 1
        return "L" + str(lab)
    
    # def slideQuads(self,start,end): # slide quads from between star_pos and end_pos to the end of the quads list 
    #     l1 = self.quads[0:start]
    #     l2 = self.quads[start:end]
    #     l3 = self.quads[end:]
        
    #     self.quads = l1 + l3 + l2