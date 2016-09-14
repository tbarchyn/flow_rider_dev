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

class params:
    def __init__ (self):
        '''
        constructor initializes parameters for the flow rider
        '''
        # default filenames for flow rider states
        states_file = 'flow_rider_states.csv'
        intersections_file = 'flow_rider_intersections.csv'
        
        
        # vehicle limits
        self.min_fluid_vel = 0.0                # minimum acceptable velocity through fluid
        self.max_fluid_vel = 100.0              # maxumum acceptable velocity through fluid
        
        
        return
        


