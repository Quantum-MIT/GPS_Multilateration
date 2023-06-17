        # particles = [] #list of coordinates of all assigned particles
        # N = 10000 # Number of assigned particles
        # for i in range(N):
        #     particles.append((rnd.uniform(0,1000),rnd.uniform(0,500))) # appending random particles 
        # # x,y=0,0
        # # for i in range(100): #if this portion of code is uncommented, then put N=33000
        # #                      #this function creates equally spaced particles thorughout the screen instead of random particles
        # #     x=0 
        # #     for j in range(333):
        # #         x+=3
        # #         particles.append((x,y))
        # #     y+=5
        # errors = [[0 for i in range(len(station_pos))] for j in range(N)] # A 2D list storing only zeros
        # #this list stores the list of errors for each particle from each station
        # for i in range(N):
        #     for j in range(len(station_pos)):
        #         errors[i][j]= math.fabs(distance(particles[i],station_pos[j]) - station_dis[j])
        # sum_errors = [] # this list stores the RMS value of errors from all stations
        # for i in range(N):
        #     sum_errors.append(RMS(errors[i])) # appends the RMS values
        # min_error = min(sum_errors) # finds the min error, the one with min error will be the max probability
        # min_index = sum_errors.index(min_error) # finds the index of the one with the mean error
        # required = particles[min_index] #finds the required particle
        # return required    