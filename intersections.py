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

# purpose: when you are riding the flow and you gotta know . . .

from math import *
import numpy as np
import pandas as pd

class intersections:
    '''
    this class manages intersection storage, calculation, and validation
    '''
    def __init__(self, params, states):
        '''
        constructor initializes the intersections dataframe
        params = a parameter object
        states = a states object
        '''
        self.params = params
        self.states = states              # states object
        
        #self.intersections = None
        return
    
    def update (self):
        '''
        method to update intersections from state dataframe
        '''
        df = self.subset ()
        df = self.pre_validate (df)
        df = self.calc (df)
        df = self.post_validate (df)
        # append fresh intersections to self.intersections dataframe
        return
        
    def subset (self):
        df = None
        return (df)
    
    def pre_validate (self, df):
        return (df)
    
    def post_validate (self, df):
        return (df)
    
    def calc_all (self, df):
        '''
        method to calculate intersections and add intersections data from a subset
        
        df = a subset dataframe of intersections
        returns the dataframe with appended columns
        '''
        df['h1_vel'] = np.nan
        df['h2_vel'] = np.nan
        df['flow_x'] = np.nan
        df['flow_y'] = np.nan
        
        for i in range (0, df.shape[0]):
            # calculate the intersection and record
            h1_vel, h2_vel, flow_x, flow_y = self.calc (df['t1_angle'][i], df['t1_vel'][i],
                                                        df['h1_angle'][i], df['t2_angle'][i],
                                                        df['t2_vel'][i], df['h2_angle'][i])
        
            df['h1_vel'][i] = h1_vel
            df['h2_vel'][i] = h2_vel
            df['flow_x'][i] = flow_x
            df['flow_y'][i] = flow_y

        return (df)

    def calc (self, t1_angle, t1_vel, h1_angle, t2_angle, t2_vel, h2_angle):
        '''
        method to calculate a given intersection
        
        t1_angle = track 1 angle (over ground)
        t1_vel = track 1 velocity (over ground)
        h1_angle = heading 1 (degrees)
        t2_angle = track 2 angle (over ground)
        t2_vel = track 2 velocity (over ground)
        h2_angle = heading 2 (degrees)
        
        variable names here:
        x1 (h1_vel) = the multiplier on heading vector 1 (the 'in flow' velocity)
        x2 (h2_vel) = the multiplier on heading vector 2 (the 'in flow' velocity)
        flow = vector of flow (x, y)
        '''
        # set up an output list
        h1_vel = np.nan
        h2_vel = np.nan
        flow_x = np.nan
        flow_y = np.nan
        
        # check to make sure the headings are not parallel (which will never intersect)
        if not h1_angle == h2_angle:
            # convert to vectors (x, y)
            t1 = np.array ([t1_vel * sin (t1_angle * pi/180.0), t1_vel * cos (t1_angle * pi/180.0)])
            t2 = np.array ([t2_vel * sin (t2_angle * pi/180.0), t2_vel * cos (t2_angle * pi/180.0)])
            h1 = np.array ([sin (h1_angle * pi/180.0), cos (h1_angle * pi/180.0)])
            h2 = np.array ([sin (h2_angle * pi/180.0), cos (h2_angle * pi/180.0)])
        
            # calculate flow through intersection
            x2 = ( (t1[0] - t2[0] + ((h1[0] / h1[1]) * (t2[1] - t1[1]))) /
                    ((h2[1] * h1[0] / h1[1]) - h2[0]) )
            x1 = -1.0 * (t2[1] - t1[1] - (x2 * h2[1])) / h1[1]
            flow = t1 - (x1 * h1)
        
            h1_vel = x1
            h2_vel = x2
            flow_x = flow[0]
            flow_y = flow[1]
                    
        return (h1_vel, h2_vel, flow_x, flow_y)
    
    def read_intersections (self, intersections_filename):
        '''
        method to read intersections from disk
        intersections_filename = filename of the intersections file
        '''
        try:
            self.df = pd.read_csv (intersections_filename)
        except:
            print ('ERROR: cannot read the intersections filename ' + intersections_filename)
            
        return
    
    def write_intersections (self, intersections_filename):
        '''
        method to write the intersections to disk for post analysis
        '''
        self.df.to_csv (intersections_filename, index = False)
        return        
        
        
        



    


