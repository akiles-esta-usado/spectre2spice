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
#-- Title      : Preprocessor 
#-- Project    : Spectre2Spice 
#-------------------------------------------------------------------------------
#-- File       : preprocessor.py
#-- Author     : Thomas E. Benz  
#-- Created    : 2018-11
#-------------------------------------------------------------------------------
#-- Description: Takes a specter netlist (as a string) and preprocesses this
#                string to be easier parsed.
#-------------------------------------------------------------------------------

# The preprocessor was tailered to work with a given set of netlist files.
# It can happen, that other netlists may have a formatting, that require
# you to modify this module to produce clean model cards.

# The following parser works only, if exatly one model card is placed on one line
# Comments should be removed.
# This file is a bit messy, as it was created in an iterative fashion
# It has to account for various formatting techniques (or the lack of) in the source files.

import re

def preprocessor(circuit):
    

    # start with the line breaks
    circuit = re.sub('\\\\\n', ' ', circuit)        # remove \ newlines 
    circuit = re.sub('\n ', '\n',   circuit)        # remove leading space after a new line
    circuit = re.sub('\n+', '\n',   circuit)        # remove multiple newline
    circuit = re.sub(' +', ' ',     circuit)        # remove multiple spaces

    # removing all comments - pass 1
    circuit = re.sub(' *\* *\n','\n',   circuit)    # remove single *
    circuit = re.sub('\/\/.*\n','\n',   circuit)    # remove // comments
    circuit = re.sub('\*\*\*+.*\n', '', circuit)    # remove *** comments

    # cleaning up whitespaces and removing empty lines
    circuit = re.sub(' +', ' ',   circuit)          # remove multiple spaces
    circuit = re.sub('\n+', '\n', circuit)          # remove multiple newline
    circuit = re.sub('\n ', '\n', circuit)          # remove empty_lines

    # removing all comments - pass 2
    circuit = re.sub('\n\*(.*)?','\n\n', circuit)   # remove single *

    # cleaning up whitspaces - pass 2
    circuit = re.sub('\n +\+', '\n+', circuit)      # remove leading space after a new line
    circuit = re.sub(' +', ' ',       circuit)      # remove multiple spaces
    circuit = re.sub('\n ', '\n',     circuit)      # remove empty_lines
    circuit = re.sub('\n+', '\n',     circuit)      # remove multiple newline

    # removing the + line cont. and bringing one card to a single line
    circuit = re.sub('\n *\+ ', ' ', circuit)       # remove line contination (+)

    # clean up function declarations and format them
    circuit = re.sub('\{\n', '{', circuit)
    circuit = re.sub('\n\}', '}', circuit)

    # remove the now emty lines once more
    circuit = re.sub('\n\n', '\n', circuit)
    circuit = re.sub('\n ', '\n',  circuit) 

    # this is a small hack, seems like the previous steps missed a whitespace in front of a { 
    circuit = re.sub('\n{', '{', circuit)

    # replace e0 with eps0 - as spice has a problem with e0 being a variable name
    circuit = re.sub('e0', 'eps0', circuit)

    # this two replacements helps the parser to detect literals with an unit postfix
    # eg, there could be a disambiguity in the bnf: var = 17f nex_var = 18
    # the parser needs to check for a space between the statements (in the all the other cases, spaces can be ignored)
    circuit = re.sub('\*', ' * ', circuit)
    circuit = re.sub('\)', ' ) ', circuit)

    # remove ' *  * ' card - some code comment formatting schemes, result in a emty card - remove this
    circuit = re.sub(' \*  \* \n', '', circuit)
 
    return circuit