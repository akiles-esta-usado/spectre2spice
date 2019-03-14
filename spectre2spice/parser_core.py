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
#-- Title      : Parser Core 
#-- Project    : Spectre2Spice 
#-------------------------------------------------------------------------------
#-- File       : parser_core.py
#-- Author     : Thomas E. Benz  
#-- Created    : 2018-11
#-------------------------------------------------------------------------------
#-- Description: The core of the parser, it combines front and backend
#-------------------------------------------------------------------------------

# importing modules neccesary to define parser
from pyparsing                      import Word, nums, alphas, Optional, Combine, Forward, printables, Suppress
from spectre2spice.model_reader     import *
from spectre2spice.component_reader import *
from spectre2spice.parser_logging   import *
from spectre2spice.spectre_bnf      import *
from spectre2spice.parser_classes   import *
import spectre2spice.shared_variables as shv

# This is the main parsing function, it is called from the netlist manager for a given
# netlist. It goes through this netlist card by card and preselects the card depending 
# on the type. It chooses then the correct entry point of the BNF, e.g parameter searches for
# eqations, while functions will be parsed with the function_definition BNF part.

# Its argument is the netlist as a string (file_string)
def parse_main(file_string):


    # cards are seperated by a nwline -> write them in a list
    model_cards = file_string.split('\n')

    # output list
    parsed_cards = []
    
    # see how the model card starts and parse it
    for model_card in model_cards:
        
        if(  model_card.startswith('parameters')):
            # parse parametrs -> top will be an equation
            parsed_list = []
            for result, start, stop in equation.scanString(model_card):
                parsed_list.append(result[0])
            parsed_cards.append(parsed_list)


        elif(model_card.startswith('real')):
            # parse functions -> top will be a func_def
            for result, start, stop in func_definition.scanString(model_card):
                parsed_cards.append([result[0]])


        elif(model_card.startswith('simulator')):
            # parse lang specification -> not really used
            parsed_lang = lang_def.parseString(model_card)
            parsed_cards.append(parsed_lang)


        elif(model_card.startswith('include') or model_card.startswith('ahdl_include')):
            # parse lang specification -> not really used
            parsed_include = include_def.parseString(model_card)
            parsed_cards.append(parsed_include)


        elif(model_card.startswith('inline') or model_card.startswith('subckt')):
            # parse subcircuit definition
            parsed_subckt = subcircuit.parseString(model_card)
            parsed_cards.append(parsed_subckt)


        elif(model_card.startswith('ends')):
            # parse subcircuit end
            parsed_ends = ends.parseString(model_card)
            parsed_cards.append(parsed_ends)


        elif(model_card.startswith('model')):
            # parse a model definition card
            parsed_model = model.parseString(model_card)
            parsed_cards.append(parsed_model)


        elif(model_card.startswith('if')):
            # parse a conditional card
            parsed_cond= conditional.parseString(model_card)
            parsed_cards.append(parsed_cond)


        # some cards are nor supported and the are only needed for e.g monte carlo simulations
        # so they can be safely ignored for now.
        elif(model_card.startswith('statistics') or model_card.startswith('process') or model_card.startswith('vary') or model_card.startswith('mismatch')):
            console_text('Unsupported card: ' + str(model_card), 2, shv.thr)


        # even thoght the preprocessor is pretty good at cleaning up the netlists, it can happen
        # that empty cards slip through, they will be ignored at this place
        elif(model_card == '' or model_card == ' *  * '):
            # skip empty cards
            continue
        
        # if we cannot extract a hint from the card, if starts with a user defined name
        # this is probably an instance of a circuit, subcrcuit or a circuit element
        # like a capacitor, resistor, .... Try to parse it, if this fails it is
        # an unsupported card -> stop the translation      
        else:
            # could be an instance of a cirquit -> try to parse it
            try:
                parsed = instance.parseString(model_card)
                parsed_cards.append(parsed)

            # Unknown card
            except:
                raise UnknownCardException(model_card)
            
    # return a list of parsed cards.
    return parsed_cards

