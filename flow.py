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

import os
from math import *
import numpy as np
import pandas as pd

from intersections import *
from states import *
from params import *
from assimilations import *

class flow:
    '''
    This is the lead import for flow_rider
    '''
    def __init__ (self, params_filename = None, quiet = False):
        '''
        constructor
        params_filename = the filename for the parameter filename, defaults
                          to params.py (local). Wind and water are going to
                          have different parameter files as there are very different
                          autocorrelation scales. Likely some vehicle customization will
                          be required also.
        quiet = boolean to suppress some output
        '''
        self.welcome (quiet)
        
        if params_filename is None and not quiet:
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
        self.states = states ()  
        self.intersections = intersections (self.params, self.states.done_all_callback)
        self.assimilations = assimilations (self.params)
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
            print ('University of Calgary')
            print ('This software has no warranty whatsoever! please see licence!')
            print ('This software is in early early beta and may contain bugs!')
            print ('------------------------------------------------------------')
        
        return

    def calc_global_mean_flow (self):
        '''
        method to return the mean flow from the intersections dataframe
        returns: flow_x_mean, flow_y_mean, flow_az, flow_vel
        '''
        flow_x_mean = np.mean (self.intersections.df['flow_x'])
        flow_y_mean = np.mean (self.intersections.df['flow_y'])
        flow_az = (atan2 (flow_x_mean, flow_y_mean) * 180.0 / pi) % 360.0
        flow_vel = sqrt (flow_x_mean**2.0 + flow_y_mean**2.0)
        return (flow_x_mean, flow_y_mean, flow_az, flow_vel)

    def add_state (self, x, y, z, time, track, velocity, heading, min_flowspeed, max_flowspeed):
        '''
        add a state to the state dataframe (this echoes states.add_state), but adds
        a call to update the intersections.
        
        x = x position (m)
        y = y position (m)
        z = z position (m)
        time = time
        track = the azimuth the vehicle is going over the ground (degrees)
        velocity = the velocity the vehicle is going over the ground (m/s)
        heading = the azimuth the vehicle is pointing (degrees)
        min_flowspeed = the minimum flow speed that is realistic (m/s)
        max_flowspeed = the maximum flow speed that is realistic (m/s)
        '''
        
        # add a state to the states dataframe
        self.states.add_state(x, y, z, time, track, velocity, heading, min_flowspeed, max_flowspeed)
        
        # intersect that state
        self.intersections.update (self.states.df)
        return

    def assimilate (self, prototype_filename = None):
        '''
        method to run assimilations
        prototype_filename = this is a raster to copy that is projected and has pre-defined extent
        '''
        # check to see if we have assimilation grids set up
        if prototype_filename is None:
            # ok, no prototype supplied, estimate the bounds from the states dataframe
            originX = np.array (self.states.df['x']).min() - self.params.default_assimilations_spacepad
            originY = np.array (self.states.df['y']).min() - self.params.default_assimilations_spacepad
            cell_Width = ((np.array (self.states.df['x']).max() + self.params.default_assimilations_spacepad) -
                            originX) / self.params.default_grid_size
            cell_Height = ((np.array (self.states.df['y']).max() + self.params.default_assimilations_spacepad) -
                            originY) / self.params.default_grid_size
            ncols = self.params.default_grid_size
            nrows = self.params.default_grid_size
            
            # check to see if we are setting bounds every assimilate call
            if self.params.set_assimilation_bounds_dynamically:
                # re-initialize with new dimensions from states
                self.assimilations.initialize (originX = originX, originY = originY, cell_Width = cell_Width,
                                                cell_Height = cell_Height, ncols = ncols, nrows = nrows)
            else:
                if not self.assimilations.assimilation_bounds_set:
                    # do the one-time initialization
                    self.assimilations.initialize (originX = originX, originY = originY, cell_Width = cell_Width,
                                                cell_Height = cell_Height, ncols = ncols, nrows = nrows)
        else:
            if not self.assimilations.assimilation_bounds_set:
                # initialize if we haven't yet
                self.assimilations.initialize (prototype_filename = prototype_filename)
        
        # and . . run the assimilations
        self.assimilations.assimilate (self.intersections.df)
        return
    
    def write (self):
        '''
        method to save everything to default filenames as supplied in the params file
        '''
        self.states.write_states (self.params.states_filename)
        self.intersections.write_intersections (self.params.intersections_file)
        return
    
    def read (self):
        '''
        method to read everything from the default filenames as supplied in the params file
        '''
        self.states.read_states (self.params.states_filename)
        self.intersections.read_intersections (self.params.intersections_file)
        return

    def write_assimilations (self, folder = None):
        '''
        method to write assimilations to disk in a folder
        folder = assigned folder to dump tiffs (optional)
        '''
        original_dir = os.getcwd ()
        if not folder is None:
            os.chdir (folder)
        self.assimilations.flow_x_mean.write_tiff (self.params.assimilation_flow_x_mean_name)
        self.assimilations.flow_y_mean.write_tiff (self.params.assimilation_flow_y_mean_name)
        self.assimilations.flow_x_sd.write_tiff (self.params.assimilation_flow_x_sd_name)
        self.assimilations.flow_y_sd.write_tiff (self.params.assimilation_flow_y_sd_name)
        self.assimilations.flow_x_med.write_tiff (self.params.assimilation_flow_x_med_name)
        self.assimilations.flow_y_med.write_tiff (self.params.assimilation_flow_y_med_name)
        self.assimilations.flow_vel.write_tiff (self.params.assimilation_flow_vel_name)
        self.assimilations.flow_az.write_tiff (self.params.assimilation_flow_az)
        
        # back to original directory
        os.chdir (original_dir)
        return



