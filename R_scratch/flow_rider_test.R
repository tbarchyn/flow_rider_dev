# flow rider vector scratch
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
    
        # check to make sure the velocities are positive
        if (x1 > 0.0 & x2 > 0.0) {
            # assign list
            i$h1_vel <- x1
            i$h2_vel <- x2
            i$flow <- flow
        }
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
    # remove the intersections that didn't work out
    df <- df[!is.na (df$h1_vel), ]
    return (df)
}

pre_eval_intersection <- function (int) {
    # function to evaluate one intersection prior to inclusion
    # the idea here is to stop the number of intersections getting out of hand
    # returns boolean TRUE if good
    
    is_good <- FALSE
    if (int$hdiff[1] > 40.0) {
        is_good <- TRUE
    }
    return (is_good)
}

make_intersections <- function (ids, times, headings, tracks, velocities) {
    # function to make a dataframe of intersections
    # ids = ids of the state estimates
    # times = times of the state estimates
    # headings = headings of the state estimates
    # tracks = tracks of the state estimates
    # velocities = velocities of the state estimates
    
    # make a prototype dataframe
    proto_df <- data.frame (
        t1_angle = NA,
        t1_vel = NA,
        h1_angle = NA,
        t2_angle = NA,
        t2_vel = NA,
        h2_angle = NA,
        id1 = NA,
        id2 = NA,
        timediff = NA,
        hdiff = NA
    )

    res_df <- proto_df
    for (i in 1:length(ids)) {
        for (j in i:length(ids)) {
            if (i != j) {
                new_int <- proto_df                 # get a fresh copy
                new_int$t1_angle[1] <- tracks[i]
                new_int$t1_vel[1] <- velocities[i]
                new_int$h1_angle[1] <- headings[i]
                new_int$t2_angle[1] <- tracks[j]
                new_int$t2_vel[1] <- velocities[j]
                new_int$h2_angle[1] <- headings[j]
                new_int$id1[1] <- ids[i]
                new_int$id2[1] <- ids[j]
                new_int$timediff[1] <- abs(times[i] - times[j])
                new_int$hdiff[1] <- min (c((headings[i] - headings[j]) %% 360.0, 
                                           (headings[j] - headings[i]) %% 360.0))
                
                # pre_evaluate this intersection before appending
                if (pre_eval_intersection (new_int)) {
                    res_df <- rbind (res_df, new_int)
                }
            }
        }
    }
    res_df <- res_df[2:nrow(res_df), ]        # remove the first row of NAs
    return (res_df)
}



#################################################
# do a test calculation with some random numbers
n <- 50        # keep this even
df <- data.frame (
    id = 1:n,
    time = 1:n,
    heading = c (rnorm (n/2, mean = 315, sd = 10.0), rnorm (n/2, mean = 45, sd = 10)),
    track = c (rnorm (n/2, mean = 270, sd = 10.0), rnorm (n/2, mean = 90, sd = 10)),
    velocity = rnorm (n, mean = 1.0, sd = 0.1)
)

# validate the random numbers in the dataframe
df$heading <- df$heading %% 360.0
df$track <- df$track %% 360.0
df$velocity[df$velocity < 0.0] <- 0.0

# make intersections
ints <- make_intersections (df$id, df$time, df$heading, df$track, df$velocity)
ints <- calc_intersections (ints)


# plot the intersections
plot (ints$flow_x, ints$flow_y, pch = 19, col = 'red')
abline (v = 0, col = 'grey')
abline (h = 0, col = 'grey')

# calculate the mean flow vector
flow_x_mean <- mean (ints$flow_x)
flow_y_mean <- mean (ints$flow_y)
flow_x_mean
flow_y_mean

# calculate the mean flow direction and velocity
flow_az <- (atan2 (flow_x_mean, flow_y_mean) * 180.0 / pi) %% 360.0
flow_vel <- sqrt (flow_x_mean^2.0 + flow_y_mean^2.0)
flow_az
flow_vel









