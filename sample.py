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

# sample flow_rider test

from flow import *

if __name__ == '__main__':
    fl = flow ()
    
    # read states, run intersections, and calc global mean
    #fl.states.read_states ('../df.csv')
    fl.states.read_states ('../test/raw_pts_fakedata.csv')
    fl.intersections.update (fl.states.df)
    fl.intersections.write_intersections ('../oput.csv')
    flow_x_mean, flow_y_mean, flow_az, flow_vel = fl.calc_global_mean_flow ()
    print ('flow mean x ' + str(flow_x_mean))
    print ('flow mean y ' + str(flow_y_mean))
    print ('flow az ' + str(flow_az))
    print ('flow vel ' + str(flow_vel))

    # assimilate to a grid
    print ('performing assimilations')
    fl.assimilate (prototype_filename = '../test/gap_proto_sm.tif')
    fl.write_assimilations (folder = '../test/')
    print ('complete')



