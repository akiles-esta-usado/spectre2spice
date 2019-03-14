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
#-- Title      : Netlist manager
#-- Project    : Spectre2Spice 
#-------------------------------------------------------------------------------
#-- File       : netlist_manager.py
#-- Author     : Thomas E. Benz  
#-- Created    : 2018-11
#-------------------------------------------------------------------------------
#-- Description: This is the netlist manager, it gets the arguments, creates folders
#                and translates netlists one by one.
#-------------------------------------------------------------------------------

from spectre2spice.include_resolver import *
from spectre2spice.parser_logging   import *
from spectre2spice.preprocessor     import preprocessor
from spectre2spice.parser_core      import *
import spectre2spice.shared_variables as shv
import os

# This is the netlist manager, it scans the whole input directory and resolves
# includes, it then translates the netlists, while creating the output directories
# and files.


# the main function to call
def netlist_manager(args):

    # start with parsing all the cmd arguments
    # ----------------------------------------

    # enable all console output
    thr = 999 if args['silent'] else -1

    # should debug output be activated?
    debug = 1 if args['debug'] else 0

    # should logging be enabled? if so parse the logging folder
    logging = not (args['log_path'] == None)
    if(logging):
        log_path = args['log_path'][0]

    # parse the output directory
    output_path = args['output_path'][0]

    # parse the tech directory
    tech_path = args['tech_path'][0]

    # greeting message
    console_text('Welcome to Spectre2Spice', 0, thr)

    # call the include resolver on the top netlist, to get all the netlists
    # to be translated
    [top_filename, top_ext] = args['top_file'][0].split('.')
    filenames = get_filenames(args['parent_path'][0], top_filename, top_ext)

    # Print the results of the hierarchy
    console_text('Analyzing includes', 0, thr)
    console_text('Hierarchy:\n\n' + pprint_filenames(filenames, '        '), 1, thr)

    # set the global variables according to the user input
    shv.tech_path      = tech_path
    shv.debug          = debug
    shv.suppress_log   = not logging
    shv.thr            = thr


    # start with translating the netlists
    # ----------------------------------------

    # go through every netlist in the filename list and translate it
    for current_netlist in filenames:

        # extract the data needed to call the parser
        path         = current_netlist[0]
        sub_path     = path[len(args['parent_path'][0]):] # the rest of the path string
        netlist_name = current_netlist[1]
        netlist_ext  = current_netlist[2]

        # get a relative path inside the top folder

        # print a simple header
        console_text('Translating file: ' + colors.NAME_COL + 
            string_len_format(netlist_name + '.' + netlist_ext, 15) + colors.NORM_COL +
            ' located at: ' + path, 0, thr)

        # create output directories if neccesary
            # create subfolder if needed
        if not os.path.exists(output_path + sub_path):
            os.makedirs(output_path + sub_path)
    
        # if logging is requested: create logging folder structure
        if(logging):
            if not os.path.exists(log_path + sub_path):
                os.makedirs(log_path + sub_path)
            # the path to the log file will be handed to the logging methode
            log_file = log_path + sub_path + netlist_name + '.log'

            # clear log file
            lf = open(log_file, 'w')
            lf.close()

            # set global varibale
            shv.log_file       = log_file
    
        else:
            log_file = ''


        # now read the input netlist file and create an output file
        input_file  = open(path + netlist_name + '.' + netlist_ext)
        output_file = open(output_path + sub_path + netlist_name + '.sp', 'w')

        # start with the translation here
        # -------------------------------


        # first call the preprocessor
        preprocessed = preprocessor(input_file.read())

        # if logging is activated -> write preprocessed circuit to files
        if(logging):
            pp_file = open(log_path + sub_path + netlist_name + '.txt', 'w')
            pp_file.write(preprocessed)
            pp_file.close()

        # parse the netlist now
        # function defined in parser_core.py
        try:
            parsed_cards = parse_main(preprocessed)

        except UnknownCardException as e:
            console_text('Unsupported Card: ' + str(e), 3, -1)


        # cards are now parsed, write them out as a netlist
        # this next part directly calls the backend
        # -------------------------------------------------
        num_cards = 0
        for card in parsed_cards:
            for sub_card in card:
                num_cards += 1

                # here the spice backend is called
                output_file.write(sub_card.spice_print() + '\n')

        # inform about the result
        console_text('Translated ' + string_len_format(str(len(parsed_cards)), 5)
         + 'to ' + str(num_cards) + ' model cards', 1, thr)


        # close all files
        input_file.close()
        output_file.close()
