# flow_rider_dev

Problem statement: vehicle is riding in a flow (wind, water, etc.); we know the real velocity and track over the ground from a GNSS; we know the real heading from an IMU. We don't, however, know how fast the vehicle is moving through the flow, making this more than a simple vector calculation. This is a very common problem because GNSS and IMUs are cheap, prevalent, and good - flow velocity instruments are neither cheap, nor prevalent, nor good.

What this does: takes heading, track, velocity estimates and performs vector intersections to make estimates of flow vector. Each intersection is qualified and a weighting model is used to interpolate spatially (and possibly temporally). This harnesses the basic idea that flow is often spatially and temporally autocorrelated . . .
