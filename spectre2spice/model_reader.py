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

#-------------------------------------------------------------------------------
#-- Title      : Model Table Reader 
#-- Project    : Spectre2Spice 
#-------------------------------------------------------------------------------
#-- File       : model_reader.py
#-- Author     : Thomas E. Benz  
#-- Created    : 2018-11
#-------------------------------------------------------------------------------
#-- Description: Reads in the model table, where is specified how the arguments
#                of the spectre models translate to the spice models
#-------------------------------------------------------------------------------

# This file reads in the model table in the toml format. Toml is a very minimal
# language to create .ini like configuartion files. https://github.com/toml-lang/toml

# At the moment, each model must have these keys:
#  ignored = "Yes" (or = "No") - specify if the model should be ignored
#  added     - specify a list of all the parameters that should be added
#  removed   - specify a list of all the parameters that should not be translated and simply be ignored
#  tranlated - list of lists: ["Specter param name", "Spice param name"]
#
# It is important, that you either tranlate or remove all the parameters of the spetre model
# Otherwise an error message will be generated

import sys
from toml                           import loads as tl
from spectre2spice.parser_logging   import *
import spectre2spice.shared_variables as shv


# Main function of this file. It gets the path to the model table, the name of the model
# and the arguments from the spectre model. It then translates them to the arguments of
# the spice model. It returns a list with the arguments and a 0 if the model should not be ignored
def translate_model(model_table, model_name, args):

    # read the model translation table and parse it
    model_table   = open(model_table, 'r').read()
    parsed_dict   = tl(model_table)

    # get the corresponding table
    try:
        current_model = parsed_dict[model_name]
    except:
        # if the model is not found in the table; 
        # print an error message to the console and return Null to stop the
        # translation
        # Warning
        console_text('Model not found in the model table\n' + str(model_name), 2, shv.thr)
        return None

    if(current_model['ignored'] == "Yes"):
        return [[], 1]

    # create an empty argument list, first add the new arguments, then go through the given argumnet list and
    # check if the argument should be translated or removed
    new_args = current_model['added']

    # do the translation
    to_translate = current_model['translated']

    for [from_ele, to_ele] in to_translate:
        for arg_eq in args:

            arg = arg_eq.split('=')
            if(arg[0] == from_ele and len(arg) == 1):
                # an argument without an =
                new_args.append(to_ele)
                args.pop(args.index(arg_eq))

            elif(arg[0] == from_ele):
                # an argument with an =
                new_args.append(to_ele + '=' + arg[1])
                args.pop(args.index(arg_eq))

    # remove unneeded elements
    to_remove = current_model['removed']

    for remove_ele in to_remove:
        for arg_eq in args:

            arg = arg_eq.split('=')
            if(arg[0] == remove_ele):
                # unconditionally remove 
                args.pop(args.index(arg_eq))

    # sanity check: see if all arguments have either be translated or removed. If not return None
    # this stopps the programm. 
    if(len(args) != 0):
        console_text('Some model parameters are missing in the model table: ' + str(args), 3, shv.thr)
        return None

    return [new_args, 0]


