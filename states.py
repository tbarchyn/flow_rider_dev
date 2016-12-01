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

import sys
import os
from math import *
import numpy as np
import pandas as pd
import datetime

class states:
    '''
    this class manages flow rider states
    '''
    def __init__(self):
        '''
        constructor initializes the state dataframe
        '''
        self.frame = 0                     # a running id for state adds
        self.columns = ('id', 'x', 'y', 'z', 'time', 'track', 'velocity', 'heading', 'min_flowspeed',
                        'max_flowspeed', 'done')
        self.df = pd.DataFrame (columns = self.columns)
        
        self.start_time = datetime.datetime.now ()
        return
    
    def add_state (self, x, y, z, time, track, velocity, heading, min_flowspeed, max_flowspeed):
        '''
        add a state to the state dataframe
        
        x = x position (m)
        y = y position (m)
        z = z position (m)
        time = time (if None, the time since init will be used)
        track = the azimuth the vehicle is going over the ground (degrees)
        velocity = the velocity the vehicle is going over the ground (m/s)
        heading = the azimuth the vehicle is pointing (degrees)
        min_flowspeed = the minimum flow speed that is realistic (m/s)
        max_flowspeed = the maximum flow speed that is realistic (m/s)
        
        Note: 'done' is a column to log if it has been intersected, this is set to 0.0 (not done),
              or to 1.0 (done). Pandas dataframes are not capable enough to reliably handle a boolean
              column.
        '''
        frame = self.frame
        self.frame = self.frame + 1
        
        # record time difference if unsupplied
        if time is None:
            time_diff = datetime.datetime.now () - self.start_time
            time = time_diff.seconds + (1e-6 * time_diff.microseconds)

        add = pd.Series ((frame, x, y, z, time, track, velocity, heading, min_flowspeed,
                          max_flowspeed, 0.0), index = self.columns)
        self.df = self.df.append (add, ignore_index = True)
        return
    
    def done_all_callback (self):
        '''
        callback method to set all the done flags to 'done', this is called by intersection code
        '''
        self.df['done'] = 1.0
        return
    
    def read_states (self, states_filename):
        '''
        method to read states from disk for analysis
        states_filename = filename of the states file
        '''
        try:
            self.df = pd.read_csv (states_filename)
            try:
                # see if there is a min flowspeed specified . . if not just pend in default
                test = self.df['min_flowspeed'][0]
            except:
                print ('adding min and max flowspeed for compatibility with old states dataframes')
                self.df['min_flowspeed'] = self.params.min_flowspeed_default
                self.df['max_flowspeed'] = self.params.max_flowspeed_default
        
        except:
            print ('ERROR: cannot read the states filename ' + states_filename)

        return
    
    def write_states (self, states_filename):
        '''
        method to write the states to disk for post analysis
        '''
        self.df.to_csv (states_filename, index = False)
        return
