# flow_rider_dev

Problem statement: vehicle is riding in a flow (wind, water, etc.); we know the real velocity and track over the ground from a GNSS; we know the real heading from an IMU. We don't, however, know how fast the vehicle is moving through the flow, making this more than a simple vector calculation. This is a very common problem because GNSS and IMUs are cheap, prevalent, and good - flow velocity instruments are neither cheap, nor prevalent, nor good.

What this does: takes heading, track, velocity estimates and performs vector intersections to make estimates of flow vector. Each intersection is qualified and a weighting model is used to interpolate spatially (and possibly temporally). This harnesses the basic idea that flow is often spatially and temporally autocorrelated . . .

##### Usage
```
# import and set up your own flow (note this uses default parameters)
from flow import *
myflow = flow ()
```

You can now read in some states, or add them in real time. If your states dataframe is formatted correctly, you can just read the whole thing in. Or, if you are bringing states in one at a time or you are mining states from another logfile, use the add_state method.

```
# read in some states (if your dataframe is formatted correctly)
myflow.states.read_states (filename)

# bring the states in one at a time (replace the 0's with real numbers!)
myflow.add_state (x = 0, y = 0, z = 0, time = 0, track = 0,
                  velocity = 0, heading = 0)
```

As every state is brought in, the intersections are calculated and appended to the intersections dataframe.

```
# get the intersections as a pandas dataframe
myflow.itersections.df
```

Now we can run the assimilations. It is recommended that you have a prototype raster that is the exact size, shape, and position required. The flow rider will assimilate estimates for every cell in the raster.

```
# run assimilations
myflow.assimilate (prototype_raster = my_prototype_raster)

# write all the assimilations to a folder
myflow.write_assimilations (folder)

# or . . access the numpy arrays to do whatever
flow_x_mean_numpy_array = myflow.assimilations.flow_x_mean.ras
```
