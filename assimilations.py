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

import numpy as np
import pandas as pd
from gdal_raster_utils import *
from scipy.spatial import cKDTree as KDTree

class assimilations:
    '''
    generic assimilations class
    '''
    def __init__ (self, params):
        '''
        initialize assimilation arrays
        params = a parameter object
        '''
        self.params = params
        self.assimilation_bounds_set = False            # flag if assimilation bounds fixed
        return
    
    def initialize (self, prototype_filename = None, originX = None, originY = None, cell_Width = None,
                  cell_Height = None, ncols = None, nrows = None):
        '''
        method to initialize rasters with either a prototype file, or pre-defined bounds
        prototype_filename = properly projected prototype raster to assimilate onto
                             if this is not supplied, assimilations are just created
        originX = the X origin location (m)
        originY = the Y origin location (m)
        cell_Width = the width of cells (m)
        cell_Height = the height of cells (m)
        ncols = the number of columns
        nrows = the number of rows
        '''
        self.flow_x_mean = ref_raster (prototype_filename = prototype_filename, originX = originX, originY = originY,
                                       cell_Width = cell_Width, cell_Height = cell_Height, ncols = ncols, nrows = nrows)
        self.flow_y_mean = ref_raster (prototype_filename = prototype_filename, originX = originX, originY = originY,
                                       cell_Width = cell_Width, cell_Height = cell_Height, ncols = ncols, nrows = nrows)
        self.flow_x_sd = ref_raster (prototype_filename = prototype_filename, originX = originX, originY = originY,
                                       cell_Width = cell_Width, cell_Height = cell_Height, ncols = ncols, nrows = nrows)
        self.flow_y_sd = ref_raster (prototype_filename = prototype_filename, originX = originX, originY = originY,
                                       cell_Width = cell_Width, cell_Height = cell_Height, ncols = ncols, nrows = nrows)
        self.flow_x_med = ref_raster (prototype_filename = prototype_filename, originX = originX, originY = originY,
                                       cell_Width = cell_Width, cell_Height = cell_Height, ncols = ncols, nrows = nrows)
        self.flow_y_med = ref_raster (prototype_filename = prototype_filename, originX = originX, originY = originY,
                                       cell_Width = cell_Width, cell_Height = cell_Height, ncols = ncols, nrows = nrows)
        self.flow_vel = ref_raster (prototype_filename = prototype_filename, originX = originX, originY = originY,
                                       cell_Width = cell_Width, cell_Height = cell_Height, ncols = ncols, nrows = nrows)
        self.flow_az = ref_raster (prototype_filename = prototype_filename, originX = originX, originY = originY,
                                       cell_Width = cell_Width, cell_Height = cell_Height, ncols = ncols, nrows = nrows)
        self.assimilation_bounds_set = True
        return
    
    def assimilate (self, intersections):
        '''
        method to interpolate to the raster grids, note presently this only does 2d intersections
        intersections = supplied intersections dataframe
        '''
        # get relevant variables as np arrays
        flow_x = np.array (intersections['flow_x'])
        flow_y = np.array (intersections['flow_y'])
        weight = np.array (intersections['weight'])
                
        # create KDTree for subsetting to neighbors
        locs = np.array (zip (intersections['x'], intersections['y']))
        tree = KDTree (locs, leafsize = 10)
        
        for i in range (0, self.flow_x_mean.nrows):
            for j in range (0, self.flow_x_mean.ncols):
                
                # query the tree to get nearest points
                loc = np.array ([self.flow_x_mean.y_index[i], self.flow_x_mean.x_index[j]])
                dists, indices = tree.query (loc, k = self.params.k_nearest, eps = 0.0)
                dists = dists [~np.isinf (dists)]              # tree returns inf if more k neighbors requested
                indices = indices [~np.isinf (dists)]          # than exist, this cuts the number down
                
                # calculate weighted averages
                flow_x_average = np.average (a = flow_x, weights = weight)
                flow_y_average = np.average (a = flow_y, weights = weight)
                self.flow_x_mean.ras[i, j] = flow_x_average
                self.flow_y_mean.ras[i, j] = flow_y_average
                self.flow_x_sd.ras[i, j] = np.sqrt (np.average ((flow_x - flow_x_average)**2.0, weights = weight))
                self.flow_y_sd.ras[i, j] = np.sqrt (np.average ((flow_y - flow_y_average)**2.0, weights = weight))
                self.flow_x_med.ras[i, j] = np.percentile (a = flow_x, q = 50.0)
                self.flow_y_med.ras[i, j] = np.percentile (a = flow_y, q = 50.0)
                
        # compute convenience vectors
        self.flow_vel.ras = np.sqrt (self.flow_x_mean.ras**2.0 + self.flow_y_mean.ras**2.0)
        self.flow_az.ras = np.arctan2 (self.flow_x_mean.ras, self.flow_y_mean.ras)
        self.flow_az.ras = self.flow_az.ras % 360.0
        return
    