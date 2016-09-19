# gdal ref raster utility class
# Copyright 2014-2016 Thomas E. Barchyn
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

import gdal
import osr
import numpy as np
import sys
import copy

class ref_raster:
    """
    Referenced raster class. This simply includes lookups for the cell centers to enable
    straightforward lookups of the real space location.
    """
    def __init__ (self, filename = None, originX = None, originY = None, cell_Width = None,
                  cell_Height = None, ncols = None, nrows = None):
        """
        Constructor requires either a prototype filename, or the specifications to create
        a blank raster full of np.nans. Note that presently a prototype raster is still
        required to get projectio
        
        filename = the filename to read raster values from
        originX = the X origin location (m)
        originY = the Y origin location (m)
        cell_Width = the width of cells (m)
        cell_Height = the height of cells (m)
        ncols = the number of columns
        nrows = the number of rows
        """
        if filename is None:
            self.originX = originX
            self.originY = originY
            self.cell_Width = cell_Width
            self.cell_Height = cell_Height
            self.ncols = ncols
            self.nrows = nrows
            read_existing_raster = False
        else:    
            self.prototype_filename = filename
            read_existing_raster = True
        
        if read_existing_raster:
            try:
                self.ras = self.read_GDAL_raster (self.prototype_filename)      # read the raster
                raster = gdal.Open (self.prototype_filename)
                geotransform = raster.GetGeoTransform()
                self.originX = geotransform[0]
                self.originY = geotransform[3]
                self.cell_Width = geotransform[1]
                self.cell_Height = geotransform[5]
                self.ncols = self.ras.shape[1]             # set nrows and cols as local variables for convenience
                self.nrows = self.ras.shape[0]
            except:
                print ('ERROR: raster read error')
        else:
            try:
                self.ras = np.zeros ((self.nrows, self.ncols)) * np.nan
            except:
                print ('ERROR: raster creation error')
        
        # calculate the indices
        self.x_index = np.zeros (self.ncols)
        for i in range(0, self.ncols):
            self.x_index[i] = (i * cell_Width) + originX + (cell_Width / 2.0)

        self.y_index = np.zeros (self.nrows)
        for j in range(0, self.nrows):
            self.y_index[j] = (j * cell_Height) + originY + (cell_Height / 2.0)

        return
    
    def blank_copy (self):
        """
        Return a blank copy of the raster with NAs everywhere
        """
        try:
            d = copy.deepcopy (self)
        except:
            print ('ERROR: raster copy error')
        
        d.ras[:,:] = np.nan
        return d
    
    def read_GDAL_raster (self, filename):
        """
        method to read a gdal raster and return band 1 as a np array
        
        filename = the filename of the raster to read
        """
        raster = gdal.Open (filename)
        band = raster.GetRasterBand(1)
        x = band.ReadAsArray ()  
        nodata_val = band.GetNoDataValue ()      # get the missing data flag
        x [x == nodata_val] = np.nan             # set missing data properly
        return (x)
    
    def write_tiff (self, filename, prototype_filename = None,
                               nan_val = None, proj_string = None):
        """
        Write a tiff to disk, if a proj_string and nan value is supplied, use those
        instead of a prototype filename. It is easier to use a prototype raster.

        filename = the filename to write
        prototype_filename = the prototype filename (correctly projected)
        nan_val = optional value for nan cells
        proj_string = projection string, if none, there is no projection assigned
        """
        if prototype_filename is None:
            if self.prototype_filename is None:
                use_prototype = False
            else:
                prototype_filename = self.prototype_filename        # use the pre-defined one 
                use_prototype = True
        
        if use_prototype:
            raster = gdal.Open (prototype_filename)
            geotransform = raster.GetGeoTransform()
            originX = geotransform[0]
            originY = geotransform[3]
            cell_Width = geotransform[1]
            cell_Height = geotransform[5]
            ncols = self.ras.shape[1]
            nrows = self.ras.shape[0]
        else:
            originX = self.originX
            originY = self.originY
            cell_Width = self.cell_Width
            cell_Height = self.cell_Height
            ncols = self.ncols
            nrows = self.nrows
            
        # create driver
        driver = gdal.GetDriverByName('GTiff')
        outRaster = driver.Create (filename, ncols, nrows, 1, gdal.GDT_Float32)
        outRaster.SetGeoTransform((originX, cell_Width, 0, originY, 0, cell_Height))
        outband = outRaster.GetRasterBand(1)
        
        # make a copy to write out
        x = self.ras.copy()
        
        # set the nodata flag properly
        if use_prototype:
            nodata_flag = raster.GetRasterBand(1).GetNoDataValue()  # get the original value
        else:
            nodata_flag = nan_val
        x [np.isnan(x)] = nodata_flag                           # assign it to the array
        outband.SetNoDataValue (nodata_flag)                    # set it in the output band
        
        # write array and set projection (if projection supplied)
        outband.WriteArray (x)
        outRasterSRS = osr.SpatialReference ()
        if use_prototype:
            outRasterSRS.ImportFromWkt (raster.GetProjectionRef())
            outRaster.SetProjection (outRasterSRS.ExportToWkt())
        else:
            if not proj_string is None:
                outRasterSRS.ImportFromWkt (proj_string)
                outRaster.SetProjection (outRasterSRS.ExportToWkt())
        
        outband.FlushCache ()
        return
    
    

