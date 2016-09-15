# flow_rider
# Copyright 2016 Thomas E. Barchyn
# Contact: Thomas E. Barchyn [tbarchyn@gmail.com]

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Please familiarize yourself with the license of this tool, available
# in the distribution with the filename: /docs/license.txt
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# purpose: when you are riding the flow and you gotta know . . .

# NOTES: conventions / terminology:
# all dimensions and coordinates are euclidean!
# all angles use compass azimuth convention in degrees (0 is grid north, clockwise to 360)
# heading is the direction the vehicle is pointed
# track is the direction the vehicle is going over the ground
# velocity is the speed the vehicle is going over the ground (towards track direction)

import sys
from math import *
import numpy as np
import pandas as pd

from intersections import *
from states import *
from params import *

class flow:
    '''
    The flow class contains the flow assimilations
    '''
    def __init__ (self, params_filename = None, quiet = False):
        '''
        constructor
        params_filename = the filename for the parameter filename, defaults
                          to params.py (local). For every flow
        quiet = boolean to supress some output
        '''
        self.welcome (quiet)
        
        if params_filename is None:
            print ('WARNING: using default parameters file params.py - you should')
            print ('         customize this for your flow!')
            params_filename = 'params.py'
        
        # load the parameters, override default params import
        try:
            execfile (params_filename)
        except:
            print ('ERROR: cannot open flow parameter file - flow rider will not work!')
            sys.exit ()
            
        self.params = params ()                                             # this should read in as an object
        self.states = states ()                                             # states     
        self.intersections = intersections (self.params)                    # intersections
        return
        
    def welcome (self, quiet):
        '''
        print a welcome message
        quiet = boolean to control whether printing of welcome message occurs
        '''
        if not quiet:
            print ('------------------------------------------------------------')
            print ('flow_rider_dev: when you are riding the flow and you gotta know . .')
            print ('Copyright 2016 Tom Barchyn')
            print ('This software has no warranty whatsoever! please see licence!')
            print ('------------------------------------------------------------')
        
        return







