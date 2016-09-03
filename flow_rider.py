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

# purpose: this contains the main flow rider class, used in flow vector
#          estimation where true speed of vehicle is unknown. This uses
#          spatial and temporal weighting to weight vector intersections.

# conventions / terminology:
# all dimensions and coordinates are euclidean!
# all angles use compass azimuth convention in degrees (0 is grid north, clockwise to 360)
# heading is the direction the vehicle is pointed
# track is the direction the vehicle is going over the ground
# velocity is the speed the vehicle is going over the ground (towards track direction)



from math import *
import numpy as np
import pandas as pd

from rider import *

class flow:
    '''
    The flow class contains assimilations of the flow from the individual flow
    rider state estimates.
    '''
    def __init__ (self, params_filename = 'params.py'):
        '''
        constructor
        params_filename = the filename for the parameter filename, defaults
                          to params.py (local)
        '''
        try:
            execfile (params_filename)
        except:
            print ('ERROR: cannot open parameter file')
            
        self.params = params ()               # this should read in as an object
        
        
        return
        
    def add_state (self, track, heading, velocity):
        '''
        add a state to the state list
        
        track = the azimuth the vehicle is going over the 
        '''
        return
    
    def add_intersections (self):
        '''
        method to add the intersections from the new state to the list
        '''
        return
        
    def save_flow (self, filename):
        '''
        method to write out the flow vector as a raster
        filename = the filename to use
        '''
        return
        
    def save_intersections (self, filename):
        '''
        method to save the instersections to a csv file
        filename = the filename of intersections
        '''
        return
        
        
        










