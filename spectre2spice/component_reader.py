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
#-- Title      : Component Table Reader 
#-- Project    : Spectre2Spice 
#-------------------------------------------------------------------------------
#-- File       : component_reader.py
#-- Author     : Thomas E. Benz  
#-- Created    : 2018-11
#-------------------------------------------------------------------------------
#-- Description: Reads in the component table, where is specified how the arguments
#                of the spectre components translate to the spice components
#-------------------------------------------------------------------------------

# This file reads in the component table in the toml format. Toml is a very minimal
# language to create .ini like configuartion files. https://github.com/toml-lang/toml

# At the moment, each component must have these keys:
#  * spectre component name
#  * spice component prefix
#  * deleted arguments
#  * translated arguments
#  * keep type - this fuction will print the component type between the ports and the arguments \
#    this is normally needed in the case of mosfets or subcircuits
#
# If there is no component found in the table, it is assumed to be an subcircuit
# it gets the prefix X_ and keeps all arguments.

import sys
from toml                           import loads as tl
from spectre2spice.parser_logging   import *
import spectre2spice.shared_variables as shv


# Main function of this file. It gets the path to the component table, the name of the type 
# and the arguments from the spectre component. It then translates them into the arguments of
# the spice component and adds the prefix to the designator.
def translate_component(component_table, designator, comp_type, args):

    # read the component translation table and parse it
    component_table   = open(component_table, 'r').read()
    parsed_dict       = tl(component_table)

    # get the component
    try:
        current_component = parsed_dict[comp_type]
        in_table = True
    except:
        # if it is not found in the table, assume it to be a subcircuit.
        # print an info message to the terminal
        console_text('Component not in table; assume it to be a subcircuit: ' + str(designator), 0, shv.thr)
        in_table = False


    # start with the case, the component was found
    if(in_table):

        # the new arguments, add the type if specified in the table
        if(current_component['keep_type'] == 'No'):
            new_args = []
        else:
            new_args = []
            new_args.append(comp_type)

        # create the new designator
        new_designator = current_component['spice_prefix'][0] + '_' + designator

        # do the translation of the parameters
        to_translate = current_component['translated']
    
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
        to_remove = current_component['removed']
    
        for remove_ele in to_remove:
            for arg_eq in args:
    
                arg = arg_eq.split('=')
                if(arg[0] == remove_ele):
                    # unconditionally remove 
                    args.pop(args.index(arg_eq))
    
        # sanity check: see if all arguments have either be translated or removed. If not return None
        # this stopps the programm. 
        if(len(args) != 0):
            console_text('Some model parameters are missing in the component table: ' + str(args), 3, shv.thr)
            return None


    # assume a subcircuit
    else:

        # just pass this through 1:1
        new_designator = 'X_' + designator
        new_args = []
        new_args.append(comp_type)
        for arg in args:
            new_args.append(arg)


    return [new_designator, new_args]


