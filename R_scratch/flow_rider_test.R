# flow rider vector scratch
# tom barchyn
# 13 Sept 2016
# this has no warranty whatsoever!

#################################################
# test parameters
t1_angle <- 310.0             # track 1 angle (over ground)
t1_vel <- 1.2                 # track 1 velocity (over ground)
h1_angle <- 250               # heading 1

t2_angle <- 320               # track 2 angle (over ground)
t2_vel <- 1.5                 # track 2 velocity (over groung)
h2_angle <- 265               # heading 2

#################################################
# functions
calc_intersection <- function (t1_angle, t1_vel, h1_angle, t2_angle, t2_vel, h2_angle) {
    # function to calculate a given intersection
    # arguments:
    # t1_angle = track 1 angle (over ground)
    # t1_vel = track 1 velocity (over ground)
    # h1_angle = heading 1
    # t2_angle = track 2 angle (over ground)
    # t2_vel = track 2 velocity (over ground)
    # h2_angle = heading 2
    
    # variable names here:
    # x1 (h1_vel) = the multiplier on heading vector 1 (the 'in flow' velocity)
    # x2 (h2_vel) = the multiplier on heading vector 2 (the 'in flow' velocity)
    # flow = vector of flow (x, y)
    
    # set up an output list
    i <- list ()
    i$h1_vel <- NA
    i$h2_vel <- NA
    i$flow <- c(NA, NA)
    
    # check to make sure the headings are not parallel (will never intersect)
    if (h1_angle != h2_angle) {
        # convert to vectors (x, y)
        t1 <- c(t1_vel * sin (t1_angle * pi/180.0), t1_vel * cos (t1_angle * pi/180.0))
        t2 <- c(t2_vel * sin (t2_angle * pi/180.0), t2_vel * cos (t2_angle * pi/180.0))
        h1 <- c(sin (h1_angle * pi/180.0), cos (h1_angle * pi/180.0))
        h2 <- c(sin (h2_angle * pi/180.0), cos (h2_angle * pi/180.0))
    
        # calculate flow through intersection
        x2 <- ( (t1[1] - t2[1] + ((h1[1] / h1[2]) * (t2[2] - t1[2]))) /
                ((h2[2] * h1[1] / h1[2]) - h2[1]) )
        x1 <- -1.0 * (t2[2] - t1[2] - (x2 * h2[2])) / h1[2]
        flow <- t1 - (x1 * h1)
    
        # assign list
        i$h1_vel <- x1
        i$h2_vel <- x2
        i$flow <- flow
    }
    return (i)
}

calc_intersections <- function (df) {
    # function to calculate intersections for a dataframe
    # t1_angle = track 1 angle (over ground)
    # t1_vel = track 1 velocity (over ground)
    # h1_angle = heading 1
    # t2_angle = track 2 angle (over ground)
    # t2_vel = track 2 velocity (over ground)
    # h2_angle = heading 2
    
    # this adds the following columns:
    # h1_vel = velocity through flow for 1
    # h2_vel = velocity through flow for 1
    # flow_x = x component of flow
    # flow_y = y component of flow
    # int_angle <- angle of intersection in degrees
    
    df$h1_vel <- NA
    df$h2_vel <- NA
    df$flow_x <- NA
    df$flow_y <- NA
    df$int_angle <- NA
    
    for (i in 1:nrow(df)) {
        df$int_angle[i] <- min (c((df$h1_angle[i] - df$h2_angle[i]) %% 360.0, 
                                  (df$h2_angle[i] - df$h1_angle[i]) %% 360.0))
        
        # calculate the intersection and record
        ret <- calc_intersection (df$t1_angle[i], df$t1_vel[i], df$h1_angle[i], df$t2_angle[i],
                                  df$t2_vel[i], df$h2_angle[i])
        
        df$h1_vel[i] <- ret$h1_vel
        df$h2_vel[i] <- ret$h2_vel
        df$flow_x[i] <- ret$flow[1]
        df$flow_y[i] <- ret$flow[2]
    }
    
    return (df)
}

make_intersections <- function (dt) {
    # function to make a dataframe of intersections
    # pass
}



#################################################
# do a test calculation with some random numbers
df <- data.frame (
    id = 1:10,
    heading = c (rnorm (5, mean = 315, sd = 10.0), rnorm (5, mean = 45, sd = 10)),
    track = c (rnorm (5, mean = 270, sd = 10.0), rnorm (5, mean = 90, sd = 10)),
    velocity = rnorm (10, mean = 1.0, sd = 1)
)

# validate the random numbers in the dataframe
df$heading <- df$heading %% 360.0
df$track <- df$track %% 360.0
df$velocity[df$velocity < 0.0] <- 0.0

















# plot the visualization
plot (-1.0 * t1[1], -1.0 * t1[2], col = 'red', xlim = c(-2, 2), ylim = c(-2, 2))
points (-1.0 * t2[1], -1.0 * t2[2], col = 'blue')
points (flow[1], flow[2], col = 'forestgreen')
abline (h = 0, col = 'grey')
abline (v = 0, col = 'grey')





