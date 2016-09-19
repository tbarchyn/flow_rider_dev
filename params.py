# flow rider
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

# params = default parameter set for flowrider

import numpy as np
import pandas as pd

class params:
    def __init__ (self):
        '''
        constructor initializes parameters for the flow rider
        '''
        # default filenames for saving the state
        self.states_filename = 'flow_rider_states.csv'
        self.intersections_filename = 'flow_rider_intersections.csv'

        self.set_assimilation_bounds_dynamically = True         # set the assimilation bounds every
                                                                # assimilate call with the dimensions
                                                                # of the states . . if no prototype
                                                                # is provided
        self.default_assimilations_spacepad = 1.0               # default pad in space outside of states
        self.default_grid_size = 10                             # default grid size
        self.k_nearest = 100                                    # get k nearest points for assimilations
        self.distance_exponent = 1.0                            # distance weighting = 1/dist^x, this is x
        
        # default names for writing assimilation rasters
        self.assimilation_flow_x_mean_name = 'flow_x_mean.tif'
        self.assimilation_flow_y_mean_name = 'flow_y_mean.tif'
        self.assimilation_flow_x_sd_name = 'flow_x_sd.tif'
        self.assimilation_flow_y_sd_name = 'flow_y_sd.tif'
        self.assimilation_flow_x_med_name = 'flow_x_med.tif'
        self.assimilation_flow_y_med_name = 'flow_y_med.tif'
        self.assimilation_flow_vel_name = 'flow_vel.tif'
        self.assimilation_flow_az = 'flow_az.tif'

        return
        
    def pre_validate (self, sdiff, tdiff, hdiff):
        '''
        function to define pre-validation checks - this must be relatively discriminatory
        to limit the number of intersections that are calculated.
        
        sdiff = space difference for intersection pair (m) (numpy array)
        tdiff = time difference for intersection pair (numpy array)
        hdiff = heading difference for intersection pair (degrees) (numpy array)
        
        this returns a boolean mask which can be applied over the test intersections
        '''
        max_dist = 100.0
        max_timediff = 100.0
        min_heading_diff = 40.0
        
        smask = sdiff < max_dist
        tmask = tdiff < max_timediff
        hmask = hdiff > min_heading_diff
        mask = smask & tmask & hmask
        return (mask)
    
    def post_validate (self, df):
        '''
        function to define post-validation checks - this removes unrealistic estimates from
        the intersections dataframe
        
        df = the full intersections dataframe
        
        this returns a mask which is True where we should keep the intersections
        '''
        
        # check the vehicle velocities to see if they are reasonable
        min_velocity = 0.0                          # minimum vehicle velocity through the flow
        max_velocity = 100.0                        # maximum vehicle velocity through the flow
        h1_vel = np.array (df['h1_vel'])            # coerce to np arrays because pandas is not up to this task(!)
        h2_vel = np.array (df['h2_vel'])
        h1_mask = (h1_vel > min_velocity) & (h1_vel < max_velocity)
        h2_mask = (h2_vel > min_velocity) & (h2_vel < max_velocity)
        mask = h1_mask & h2_mask
        
        return (mask)
    
    def calc_weights (self, df):
        '''
        method to calculate the static weights for each intersection
        returns a numpy array to slot into the dataframe weights column
        '''
        pass
        weights = np.array (df['weight'])
        weights[:] = 1.0
        #space_zero_weight = 100.0
        #space
        
        #sdiff_weight = 
        #tdiff_weight =
        #hdiff_weight = 
        #weights = sdiff_weight * tdiff_weight * hdiff_weight
        return (weights)

        
