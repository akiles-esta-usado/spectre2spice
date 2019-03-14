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
#-- Title      : Logging Functions
#-- Project    : Spectre2Spice 
#-------------------------------------------------------------------------------
#-- File       : parser_logging.py
#-- Author     : Thomas E. Benz  
#-- Created    : 2018-11
#-------------------------------------------------------------------------------
#-- Description: A few functions used to generate pretty console output
#-------------------------------------------------------------------------------

from spectre2spice.parser_core        import *
import spectre2spice.shared_variables as shv

# Terminal color bytes
class colors:
    ERR_COL  = '\033[1;31m'
    SUCC_COL = '\033[0;32m'
    WARN_COL = '\033[0;33m'
    NAME_COL = '\033[0;36m'
    NORM_COL = '\033[0;0m'

# standard functions to generate log
def debug_output(printable):

    # fetch the current global variables
    log_file       = shv.log_file
    suppress_debug = shv.suppress_log
    debug          = shv.debug

    if(not suppress_debug):
        lf = open(log_file, 'a')
        lf.write(str(printable) + '\n')
        lf.close()

    if(debug):
        print(str(printable))

    return 0

def debug_find_ele(string, start, tocs, ele_type):
    output = str(ele_type) + ' in: ' + string_len_format(string[start:start+22],22) + ' --- tocs: '
    for toc in tocs:
        output += str(toc)
        if(len(tocs) > 1):
            output += '\n                                                '

    debug_output(output)
    return 0

def string_len_format(string, length):
    if(len(string) < length):
        pat = ''
        for i in range(0, length-len(string)):
            pat += ' '
        return string + pat
    return string

# This function directly prints to standard out.
def console_text(printable, level, thr):

    if(level==0 and level > thr):
        print(colors.NORM_COL + 'Info:   ' + str(printable) + colors.NORM_COL)

    if(level==1 and level > thr):
        print(colors.SUCC_COL + 'Done:   ' + str(printable) + colors.NORM_COL)

    if(level==2 and level > thr):
        print(colors.WARN_COL + 'Warn:   ' + str(printable) + colors.NORM_COL)

    if(level==3 and level > thr):
        print(colors.ERR_COL + 'Error:  ' + str(printable) + colors.NORM_COL)

    return None

# definition of the custom error thrown if an unsupport card is 
# encountered. 
class UnknownCardException(Exception):
    def __init__(self, card):
        self.card = card

    def __str__(self):
        return str(self.card)