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
#-- Title      : Spectre BNF
#-- Project    : Spectre2Spice 
#-------------------------------------------------------------------------------
#-- File       : spectre_bnf.py
#-- Author     : Thomas E. Benz  
#-- Created    : 2018-11
#-------------------------------------------------------------------------------
#-- Description: A description of the Spectre netlist BNF        
#-------------------------------------------------------------------------------

# importing modules neccesary to define parser
from pyparsing                    import Word, nums, alphas, Optional, Combine, Forward, printables, Suppress
from spectre2spice.parser_classes import *

# This file contains the BNF, it can be seen as the frontend of the parser, while
# the parser_classes.py is more of a backend. In the following definitions, every 
# parsable netlist part, like an integer, is defined.
# I have explained how a BNF works a bit more in the report.
# Pyparsing is a bit special, if definitios are recursive. expression = expression ^ ...
# This has to be defined with a forward definition. See the pyparsing manual for more
# information.
# If you want to port this translator to another source netlist language, this files
# needs to be replaced.

# Every main object, has a setParseAction() defined. This directly calls the wrapper
# function, that creates the abstract objects. 


#--------------------------- forward defs ---------------------------------
function   =   Forward()
sub_func   =   Forward()
case       =   Forward()
expression =   Forward()
unary_op   =   Forward()
tupel      =   Forward()
#--------------------------- forward defs ---------------------------------


#--------------------------- literals -------------------------------------
integer   = Combine(Optional("+") + Optional("-") + Word(nums))
real      = Combine(integer + "." + integer)
flot_num  = Combine(integer + ".")
scintific = (real ^ integer) + Word('eE', max=1) + integer
postfix   = (real ^ integer) + Word('tgxkmunpf', max=1) + Suppress(Word(' ').leaveWhitespace() | Word('\'') | Word('+*-/', max=1))
literal   = postfix ^ scintific ^ flot_num ^ real ^ integer

literal.setParseAction(num_wrapper)
#----------------------------literals--------------------------------------


#----------------------------variables-------------------------------------
variable  = Word(alphas + "_" + nums + '!', min=1)

variable.setParseAction(var_wrapper)
#----------------------------variables-------------------------------------


#----------------------------types-----------------------------------------
var_type  = 'real'
#----------------------------types-----------------------------------------


#----------------------------string----------------------------------------
string_type = '"' + Word(alphas + ' ' + '.,-_!?()').leaveWhitespace() + '"'

string_type.setParseAction(string_type_wrapper)
#----------------------------string----------------------------------------


#----------------------------duoary_op-------------------------------------
duoary_op = Word("!&|+-*/<>", max=2) ^ Word("!=", min=2)  ^ Word("==", min=2) ^ Word(">=", min=2)  ^ Word("<=", min=2) ^ Word("**", min=2)

duoary_op.setParseAction(op_wrapper)
#----------------------------duoary_op-------------------------------------


#----------------------------expression------------------------------------
sub_expr   =   Suppress("(") + expression + Suppress(")")
sub_case   =   Suppress("(") + case + Suppress(")")
sub_func   =   Suppress("(") + function + Suppress(")")
expr_part  =   sub_case ^ sub_expr ^ sub_func ^ function ^ literal ^ variable
expr_ele   =   (unary_op ^ expr_part)
expression <<  expr_ele + (duoary_op + expr_part)*(0,None) # this operator is needed to overwrite a forward

sub_expr.setParseAction(sub_expr_wrapper)
sub_case.setParseAction(sub_case_wrapper)
sub_func.setParseAction(sub_func_wrapper)

expression.setParseAction(expr_wrapper)
#----------------------------expression------------------------------------


#----------------------------unary_op--------------------------------------
unary_op   << Word('-') + expr_part

unary_op.setParseAction(unop_wrapper)
#----------------------------unary_op--------------------------------------


#----------------------------function--------------------------------------
function  <<   variable + Suppress("(") + expression + (Suppress(",") + expression)*(0,None) + Suppress(")")

function.setParseAction(func_wrapper)
#----------------------------function--------------------------------------


#----------------------------- case ---------------------------------------
case_part =    expression ^ sub_expr
case      <<   case_part + Suppress("?") + case_part + Suppress(":") + case_part

case.setParseAction(case_wrapper)
#----------------------------- case ---------------------------------------


#----------------------------equation--------------------------------------
equation  = Suppress(Optional('parameters')) + (expression) + Suppress('=') + (case ^ expression ^ tupel ^ string_type)

equation.setParseAction(eq_wrapper)
#----------------------------equation--------------------------------------


#----------------------------equation-def----------------------------------
func_name       = Suppress(var_type) + variable + Suppress('(')
func_para       = (Suppress(var_type) + expression + Suppress(Optional(',')))*(1,None) + Suppress(')') 
func_body       = Suppress('{' + 'return') + (case ^ expression) + Suppress(Optional(';') + '}')
func_definition = func_name + func_para + func_body

func_definition.setParseAction(func_def_wrapper)
#----------------------------equation-def----------------------------------


#-------------------------------lang-def-----------------------------------
lang_def       = Suppress('simulator' + Word(alphas) + '=') + Word(alphas)

lang_def.setParseAction(lang_wrapper)
#-------------------------------lang-def-----------------------------------


#-------------------------------include_def--------------------------------
path_def       = Optional(Word('..') ^ Word('.')) + Optional('/') + (Word(alphas + "_" + nums, min=1) + Word('/')) * (0, None)
path_def       = Combine(path_def)
include_def    = (Word('include ') ^ Word('ahdl_include')) + Suppress('\"') + path_def + Word(alphas + "_" + nums, min=1) + Suppress('.') + Word(alphas) + Suppress('\"')

include_def.setParseAction(include_wrapper)
#-------------------------------include_def-------------------------------


#-------------------------------subcircuit--------------------------------
subcircuit    = Optional('inline') + Suppress('subckt') + variable + Optional(Suppress('(')) + (variable)*(1,None) + Optional(Suppress(')'))

subcircuit.setParseAction(subcirquit_wrapper)
#-------------------------------subcircuit--------------------------------


#-------------------------------instance--------------------------------
instance     = variable + Suppress(Optional('(')) + (equation | variable)*(1,None) + Suppress(Optional(')')) + (equation | variable)*(0,None)

instance.setParseAction(instance_wrapper)
#-------------------------------instance--------------------------------


#-------------------------------end subcirquit---------------------------
ends         = Suppress('ends') + variable

ends.setParseAction(ends_wrapper)
#-------------------------------end subcirquit---------------------------


#-------------------------------model------------------------------------
model        = Suppress('model') + variable + variable + equation*(1,None)

model.setParseAction(model_wrapper)
#-------------------------------model------------------------------------


#-------------------------------assertion------------------------------------
assertion   = variable + Suppress("assert") + equation*(1,None)

assertion.setParseAction(assertion_wrapper)
#-------------------------------assertion------------------------------------


#-------------------------------cond-------------------------------------
conditional = Suppress('if') + Suppress('(') + expression + Suppress(')') + Suppress('{') + (assertion ^ instance)*(1,None) + Suppress('}')

conditional.setParseAction(cond_wrapper)
#-------------------------------cond-------------------------------------


#-------------------------------tupel------------------------------------
tupel       << Suppress('[') + variable*(2, None) + Suppress(']')

tupel.setParseAction(tupel_wrapper)
#-------------------------------tupel------------------------------------



# this is the end of this file, if you wish to add support for other cards, they can be placed
# here.


