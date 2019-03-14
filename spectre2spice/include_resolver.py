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
#-- Title      : Include resolver
#-- Project    : Spectre2Spice 
#-------------------------------------------------------------------------------
#-- File       : include_resolver.py
#-- Author     : Thomas E. Benz  
#-- Created    : 2018-11
#-------------------------------------------------------------------------------
#-- Description: A set of function to recursively resolve includes
#-------------------------------------------------------------------------------

# importing modules neccesary to define parser
from pyparsing                    import Word, nums, alphas, Optional, Combine, Forward, printables, Suppress
from spectre2spice.parser_core    import *
from spectre2spice.parser_logging import *
from spectre2spice.parser_classes import *
from spectre2spice.spectre_bnf    import *

# This functions are used by the netlsit manager to find the include statements in the netlists
# and resolve them.


# go through the filetree and resolve all includes
def get_filenames_rec(parent_path, sub_path, filename, ext, level, hierarchy):

    # open the parent file
    file = open(parent_path + sub_path + filename + '.' + ext, 'r')

    # append it to the hierarchy
    hierarchy.append([str(parent_path+sub_path), str(filename), str(ext), level])

    # search every line of the netlist if there is an include statement
    for line in file:
        if line.startswith('include'):
            parsed      = include_def.parseString(line)
            include_ele = parsed[0].get_include()
            # call the same function, but now 'a level deeper'
            get_filenames_rec(parent_path + sub_path, include_ele[0], include_ele[1], include_ele[2], level+1, hierarchy)

    # return the subhierarchy to the parent function
    file.close()
    return hierarchy


# nice wrapper for the hierarchical function
def get_filenames(parent_path, filename, input_ext):
    return get_filenames_rec(parent_path, '', filename, input_ext, 0, [])


# small prettyprint for all the filenames
def pprint_filenames(filename_list, prefix):

    res = ''
    for name in filename_list:
        name_line = prefix
        # indent the line depending on the hierarchy level
        for tab in range(0,name[3]):
            name_line += '  '

        # create arrows to make the dependeny clearer
        if(name[3] !=0):
            name_line += '└-> ' + name[1] + '.' + name[2]
        else:
            name_line += name[1] + '.' + name[2]

        res += name_line + '\n'

    return res