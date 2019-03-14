#!/usr/bin/env python3
##
## Copyright (c) 2019 Thomas Benz.
## 
## This file is part of librecell-layout 
## (see https://codeberg.org/thommythomaso/spectre2spice/master/)
## 
## This program is free software: you can redistribute it and/or modify
## it under the terms of the CERN Open Hardware License (CERN OHL-S) as it will be published
## by the CERN, either version 2.0 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## CERN Open Hardware License for more details.
## 
## You should have received a copy of the CERN Open Hardware License
## along with this program. If not, see <http://ohwr.org/licenses/>.
## 
## 
##

# coding=utf8
#-------------------------------------------------------------------------------
#-- Title      : Parsed Objects 
#-- Project    : Spectre2Spice 
#-------------------------------------------------------------------------------
#-- File       : parser_classes.py
#-- Author     : Thomas E. Benz  
#-- Created    : 2018-11
#-------------------------------------------------------------------------------
#-- Description: Contains a class for every object, that can be parsed           
#-------------------------------------------------------------------------------

from spectre2spice.parser_logging     import *
from spectre2spice.model_reader       import *
from spectre2spice.component_reader   import *


# In this document, for every object, that can be parsed by Specter2Spice,
# a class is defined. Every class has a wrapper, that is called once an
# object is found by pyparsing. Pyparsing hands the parsed information 
# to this wrapper, which in turn creates a new object with the parsed information.
# This creates a tree like data structure for every card.
# Every class needs to have a prettyprint methode, e.g spice_print. This methode
# is recursively called as soon as the backend want to write out the netlist
# in the target format.

# Every class represents an object type, e.g an equation will be stored into an
# object of the Equation class. An eqaution has two arguments, a left and a right side
# argument. Those can be in turn other objects, e.g an Equation can have an expression
# as a right side argument and a variable(name) as an left side argument.

# To change the output netlist format, add a new pretty print function to every methode.
# In this file, every methode has a spice_print() methode to generate spice code.
# For debugging purposes, other methodes exist in some classes, but they are commented
# out and not needed. But the can be an example what other target languages can be used.


class Equation:
    def __init__ (self, ls, rs):

        self.left_side = ls
        self.right_side = rs

    # def pprint(self):
    #     return str(self.left_side.pprint()) + ' = ' + str(self.right_side.pprint())

    # def py_print(self):
    #     return str(self.left_side.py_print()) + ' = ' + str(self.right_side.py_print())

    def spice_print(self):
        return '.param ' + str(self.left_side.spice_print()) + '=\'' + str(self.right_side.spice_print()) + '\''

    # def spectre_print(self):
    #     return 'parameters ' + str(self.left_side.spectre_print()) + '=' + str(self.right_side.spectre_print())


def eq_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'equation  ')
    return Equation(tocs[0], tocs[1])

# ----------------------------------------------------------

class Number:
    def __init__(self, parsed):

        value = ''.join(parsed)
        self.value = str(value)

    # def pprint(self):
    #     return self.value

    # def py_print(self):
    #     return self.value

    def spice_print(self):
        return self.value

    # def spectre_print(self):
    #     return self.value


def num_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'number    ')
    return Number(tocs)

# ----------------------------------------------------------

class Variable:
    def __init__(self, name):

        self.name = name

        # if(name[0] == 'as'):  # remove python keywords
        #     self.py_name = ['py_as']
        # else:
        #     self.py_name = name

    # def pprint(self):
    #     return str(self.name[0])

    # def py_print(self):
    #     return str(self.py_name[0])

    def spice_print(self):
        return str(self.name[0])

    # def spectre_print(self):
    #     return str(self.name[0])

def var_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'variable  ')
    return Variable(tocs)

# ----------------------------------------------------------

class Duoary_OP:
    def __init__(self, operator):

        self.op    = operator
        
        # if(operator[0] == '||'):   # translate to python operators
        #     self.py_op = [' or ']
        # elif(operator[0] == '&&'):
        #     self.py_op = [' and ']
        # else: self.py_op = operator

    # def pprint(self):
    #     return str(self.op[0])

    # def py_print(self):
    #     return str(self.py_op[0])

    def spice_print(self):
        return str(self.op[0])

    # def spectre_print(self):
    #     return str(self.op[0])

def op_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'operator  ')
    return Duoary_OP(tocs)

# ----------------------------------------------------------

class Unary_OP:
    def __init__(self, operator, expression_fragment):

        self.op    = operator 
        self.frag  = expression_fragment

    # def pprint(self):
    #     return str(self.op[0]) + str(self.frag[0].pprint())

    # def py_print(self):
    #     return str(self.op[0]) + str(self.frag[0].py_print())

    def spice_print(self):
        return str(self.op[0]) + str(self.frag[0].spice_print())

    # def spectre_print(self):
    #     return str(self.op[0]) + str(self.frag[0].spectre_print())

def unop_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'un_op     ')
    return Unary_OP(tocs[0], tocs[1:])

# ----------------------------------------------------------

class Expression:
    def __init__(self, param_list):

        self.expression_list = param_list

    # # def pprint(self):
    # #     res =  ''
    # #     for ele in self.expression_list:
    # #         res += str(ele.pprint()) #+ ' '
    # #     return res #+ ')'

    # # def py_print(self):
    # #     res = ''
    # #     for ele in self.expression_list:
    # #         res += str(ele.py_print())
    # #     return res 

    def spice_print(self):
        res = ''
        for ele in self.expression_list:
            res += str(ele.spice_print())
        return res 

    # # def spectre_print(self):
    # #     res = ''
    # #     for ele in self.expression_list:
    # #         res += str(ele.spectre_print())
    # #     return res 


def expr_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'expression')
    return Expression(tocs)

# ----------------------------------------------------------

class Function:
    def __init__(self, name, arguments):

        self.name = name
        self.args = arguments

    # def pprint(self):
    #     res = str(self.name.pprint()) + '('
    #     for ele in self.args:
    #         res += str(ele.pprint()) + ', '
    #     return res + ')'

    # def py_print(self):
    #     res = str(self.name.py_print()) + '('
    #     for ele in self.args:
    #         res += str(ele.py_print()) + ', '
    #     res = res[:-2]
    #     return res + ')'

    def spice_print(self):

        res = str(self.name.spice_print()) + '('
        for ele in self.args:
            res += str(ele.spice_print()) + ','
        res = res[:-1]  + ')'

        # hacky: spice does not support to change parameter (.param) during runtime.
        # therefore I set all the v(.,.) functions to 0. 
        if(self.name.spice_print() == 'v' or self.name.spice_print() == 'V'):
            console_text('Set voltage in .param to 0: - ' + res, 2, -1) # log to the terminal
            res = '0'
        return res

    # def spectre_print(self):
    #     res = str(self.name.spectre_print()) + '('
    #     for ele in self.args:
    #         res += str(ele.spectre_print()) + ','
    #     res = res[:-1]
    #     return res + ')'


def func_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'function  ')
    return Function(tocs[0], tocs[1:])

# ----------------------------------------------------------

class Case:
    def __init__(self, cond, if_ele, else_ele):

        self.cond      = cond
        self.if_ele    = if_ele
        self.else_ele  = else_ele

    # def pprint(self):
    #     return 'if(' + self.cond.pprint() + ') then(' + self.if_ele.pprint() + ') else(' + self.else_ele.pprint() + ')'

    # def py_print(self):
    #     res = ''
    #     res += self.if_ele.py_print()
    #     res += ' if (' + self.cond.py_print()
    #     res += ') else (' + self.else_ele.py_print() + ")"
    #     return res

    def spice_print(self):
        return self.cond.spice_print() + '?' + self.if_ele.spice_print() + ':' + self.else_ele.spice_print()

    # def spectre_print(self):
    #     return self.cond.spectre_print() + '?' + self.if_ele.spectre_print() + ':' + self.else_ele.spectre_print()

def case_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'case      ')
    return Case(tocs[0], tocs[1], tocs[2])

# ---------------------------------------------------------

class FunctionDef:
    def __init__(self, name, arguments, body):

        self.name = name
        self.arguments = arguments
        self.body = body

    # def pprint(self):
    #     res = 'real '
    #     res += self.name.pprint() + '('
    #     for arg in self.arguments:
    #         res += arg.pprint() + ','
    #     res += ') {' + str(self.body.pprint()) + '}'
    #     return res

    # def py_print(self):
    #     res = 'def '
    #     res += self.name.py_print() + '('
    #     for arg in self.arguments:
    #         res += arg.py_print() + ','
    #     res = res[:-1]
    #     res += '):\n    return ' + str(self.body.py_print()) + '\n'
    #     return res

    def spice_print(self):
        res = '.func '
        res += self.name.spice_print() + '('
        for arg in self.arguments:
            res += arg.spice_print() + ','
        res = res[:-1]
        res += ') {' + str(self.body.spice_print()) + '}'

        return res

    # def spectre_print(self):
    #     res = 'real '
    #     res += self.name.spectre_print() + '('
    #     for arg in self.arguments:
    #         res += 'real ' + arg.spectre_print() + ','
    #     res = res[:-1]
    #     res += ') {return ' + str(self.body.spectre_print()) + ';}'
    #     return res


def func_def_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'func_def  ')
    return FunctionDef(tocs[0], tocs[1:-1], tocs[-1])

# ---------------------------------------------------------

class LangDef:
    def __init__(self, lang):

        self.lang = lang[0]

    # def pprint(self):
    #     return 'simulator lang = ' + str(self.lang)

    # def py_print(self):
    #     return '# simulator lang = ' + str(self.lang)

    def spice_print(self):
        return '*simulator lang=' + str(self.lang)

    # def spectre_print(self):
    #     return 'simulator lang=' + str(self.lang)


def lang_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'lang_def  ')
    return LangDef(tocs)

# ----------------------------------------------------------

class IncludeDef:
    def __init__(self, include_type, path, file, extension):

        self.type = include_type
        self.path = path
        self.file = file
        self.ext  = extension

    # def pprint(self):
    #     return string_len_format(str(self.type),12) + ' "' + str(self.path) + str(self.file) + '.' + str(self.ext) + '"'

    # def py_print(self):
    #     return '# ' + string_len_format(str(self.type),12) + ' ' + str(self.path) + str(self.file) + '.' + str(self.ext)

    def spice_print(self):
        if(self.type == 'include ' or self.type == 'include'):
            return '.include ' + str(self.path) + str(self.file) + '.sp'
        else:
            # these are analog includes (AHDL or A-Verilog) Spice cannot use them
            return '*.' + str(self.type) + ' ' + str(self.path) + str(self.file) + '.' + str(self.ext)

    # def spectre_print(self):
    #     if(self.type == 'include ' or self.type == 'include'):
    #         return 'include "' + str(self.path) + str(self.file) + '.scs"'
    #     else:
    #         return str(self.type) + ' ' + str(self.path) + str(self.file) + '.' + str(self.ext)


    def get_include(self):
        return [str(self.path), str(self.file), str(self.ext)]

def include_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'include   ')
    return IncludeDef(tocs[0], tocs[1], tocs[2], tocs[3])

# ----------------------------------------------------------

class Subcircuit:
    def __init__(self, args):

        # differenciate between inline subcks and normal ones
        if(args[0] == 'inline' or args[0] == 'inline '):

            # inline
            self.inline = True
            self.name   = args[1]
            self.conns  = args[2:]

        else:
            # normal case
            self.inline = False
            self.name   = args[0]
            self.conns  = args[1:]

    # def pprint(self):
    #     res = ''
    #     if(inline):
    #         res += 'inline '
    #     res += str(self.name.pprint()) + '('
    #     for ele in self.connections:
    #         res += str(ele.pprint()) + ', '
    #     return res + ')'
 
    # def py_print(self):
    #     res = '# '
    #     if(self.inline):
    #         res += 'inline '
    #     res += str(self.name.py_print()) + '('
    #     for ele in self.connections:
    #         res += str(ele.py_print()) + ', '
    #     res = res[:-2]
    #     return res + ')'

    def spice_print(self):
        res = '.subckt '
        res += str(self.name.spice_print()) + ' ('
        for ele in self.conns:
            res += str(ele.spice_print()) + ' '
        return res[:-1] + ')'

    # def spectre_print(self):
    #     res = ''
    #     if(inline):
    #         res += 'inline '
    #     res += 'subckt'
    #     res += str(self.name.spice_print()) + ' ('
    #     for ele in self.conns:
    #         res += str(ele.spice_print()) + ' '
    #     return res[:-1] + ')'

def subcirquit_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'subcirquit')
    return Subcircuit(tocs)

# ----------------------------------------------------------

class Instance:
    def __init__(self, name, arguments):

        self.name = name

        # Doing a bit of postprocessing. Due to the fact, that spice does not need the () to group the port
        # list in the instance card, parsing with the bnf will be hard.
        it = 0

        # check all the parsed arguments, some will be variables (ports) and some will be
        # parameter equations. The parameter eqations start with .param, therefore
        # its easy to count the number of ports.
        # e.g res gnd vdd resistor r=5
        # the name can easily be extracted by the BNF. The rest is hard; It will count 4 variables
        # gnd, vdd and resistor. The loop counts the number of variables, the first n-1 are ports and the
        # last is the type.
        while not (arguments[it].spice_print().startswith('.param')):
            #listing the ports and the type of the instance
            it+=1
        it = it - 1 # We dont need to count the type for the number of arguments

        self.ports = arguments[0:it]
        self.type  = arguments[it]
        self.args  = arguments[it+1:]

    def spice_print(self):

        # translate the arguments so far
        plain_args = []
        for arg in self.args:
            plain_args.append(arg.spice_print()[7:])

        # call the component translation function
        [new_designator, new_args] = translate_component(shv.tech_path + 'component_table.toml', self.name.spice_print(),
         self.type.spice_print(), plain_args)

        # build the new component card
        res = new_designator + ' '
        for port in self.ports:
            res += str(port.spice_print()) + ' '

        for arg in new_args:
            res += arg + ' '

        return res

def instance_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'instance  ')
    return Instance(tocs[0], tocs[1:])

# ----------------------------------------------------------

class Ends:  # this is the end subcircuit card
    def __init__(self, name):

        self.name = name

    # def pprint(self):
    #     return 'ends ' + str(self.name[0].pprint())

    # def py_print(self):
    #     return '# ends ' + str(self.name[0].py_print())

    def spice_print(self):
        return '.ends ' + str(self.name[0].spice_print())

    # def spectre_print(self):
    #     return 'ends ' + str(self.name[0].specer_print())        

def ends_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'ends      ')
    return Ends(tocs)

# ----------------------------------------------------------

class SubExpr:
    def __init__(self, expression):

        self.expr = expression

    # def pprint(self):
    #     return '(' + str(self.expr[0].pprint()) + ')'

    # def py_print(self):
    #     return '(' + str(self.expr[0].py_print()) + ')'

    def spice_print(self):
        return '(' + str(self.expr[0].spice_print()) + ')'

    # def spectre_print(self):
    #     return '(' + str(self.expr[0].spectre_print()) + ')'

def sub_expr_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'sub_expr  ')
    return SubExpr(tocs)

# ----------------------------------------------------------

class SubCase:
    def __init__(self, case):

        self.case = case

    # def pprint(self):
    #     return '(' + str(self.case[0].pprint()) + ')'

    # def py_print(self):
    #     return '(' + str(self.case[0].py_print()) + ')'

    def spice_print(self):
        return '(' + str(self.case[0].spice_print()) + ')'

    # def spectre_print(self):
    #     return '(' + str(self.case[0].spectre_print()) + ')'

def sub_case_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'sub_case  ')
    return SubCase(tocs)

# ----------------------------------------------------------

class SubFunc:
    def __init__(self, function):

        self.function = function

    # def pprint(self):
    #     return '(' + str(self.function[0].pprint()) + ')'

    # def py_print(self):
    #     return '(' + str(self.function[0].py_print()) + ')'

    def spice_print(self):
        return '(' + str(self.function[0].spice_print()) + ')'

    # def spectre_print(self):
    #     return '(' + str(self.function[0].spectre_print()) + ')'

def sub_func_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'sub_func  ')
    return Subfunc(tocs)

# ----------------------------------------------------------

class StringType:
    def __init__(self, string):

        self.string = ''.join(string)

    # def pprint(self):
    #     return self.string

    # def py_print(self):
    #     return self.string

    def spice_print(self):
        return self.string

    # def spectre_print(self):
    #     return self.string

def string_type_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'string    ')
    return StringType(tocs)

# ----------------------------------------------------------

class Assertion:
    def __init__(self, name, arguments):

        self.name = name
        self.args = arguments

    # def pprint(self):
    #     res = self.name.pprint() + ' assert '
    #     for arg in self.args:
    #         res += arg.pprint()[7:] + ' '
    #     return res
    
    # def py_print(self):
    #     res = '#' + self.name.py_print() + ' assert '
    #     for arg in self.args:
    #         res += arg.py_print()[7:] + ' '
    #     return res
    
    def spice_print(self):
        res = '*' + self.name.spice_print() + ' assert '
        for arg in self.args:
            res += arg.spice_print()[7:] + ' '
        return res
    
    # def spectre_print(self):
    #     res = self.name.spectre_print() + ' assert '
    #     for arg in self.args:
    #         res += arg.spectre_print()[7:] + ' '
    #     return res

def assertion_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'assertion ')
    return Assertion(tocs[0], tocs[1:])

# ----------------------------------------------------------

class Model:
    def __init__(self, parameter):

        self.name = parameter[0]
        self.type = parameter[1]
        self.args = parameter[2:]

    # spice_print reads the model informations in by using the TOML language
    def spice_print(self):

        # translate the arguments so far
        plain_args = [self.type.spice_print()]
        for arg in self.args:
            plain_args.append(arg.spice_print()[7:])

        # do the translation, ignored is a binary flag if the model should be ignored
        # new_args is the response.
        [new_args, ignored] = translate_model(shv.tech_path + 'model_table.toml', self.name.spice_print(), plain_args)

        # print the model card if not ignored.
        if(not ignored):
            res = '.model ' + str(self.name.spice_print()) + ' '
            for arg in new_args:
                res += str(arg) + ' '
            return res

        # if ignored place a comment.
        else:
            return '*.model ' + self.name.spice_print() + ' ' + ' '.join(plain_args)

def model_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'model     ')
    return Model(tocs)

 # ----------------------------------------------------------
 
class Conditional: # for now only the if case is used.
    def __init__(self, parameter):

        self.cond   = parameter[0]
        self.ifcase = parameter[1]

    def spice_print(self):
        res =  '.if (' + str(self.cond.spice_print()) + ') {'
        res += str(self.ifcase.spice_print()) + '}'
        return res

    #def spectre_print(self):
    #    res =  '.if (' + str(self.cond.spectre_print()) + ') {'
    #    res += str(self.ifcase.spectre_print()) + '}'
    #    return res

def cond_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'cond      ')
    return Conditional(tocs)

 # ----------------------------------------------------------
 
class Tupel:
    def __init__(self, parameters):

        self.params = parameters

    def spice_print(self):
        res = '['
        for para in self.params:
            res += str(para.spice_print()) + ' '
        res = res[:-1] + ']'
        return res

    # def spectre_print(self):
    #     res = '['
    #     for para in self.params:
    #         res += str(para.spectre_print()) + ' '
    #     res = res[:-1] + ']'
    #     return res

def tupel_wrapper(string, start, tocs):
    debug_find_ele(string, start, tocs, 'tupel     ')
    return Tupel(tocs)


# this is the end of this document, if any new cards should be added, they can be added here.
# For every new card a new class and a new wrapper needs to be implemented.


