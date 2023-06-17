'''
Do not edit main function.
Do not use anything other than coordinate class from lib
'''

import random as rnd
import math
import numpy as np
import time
import cv2
import typing

import lib
from lib import coordinate as coordinate
from lib import SignalsNotReady as SignalsNotReady

DELAY = time.time() - lib.calliberate()

def distance(point1, point2): #returns the distance 
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def RMS(particle_errors): #returns the RMS value of the passed list of errors of each particle
    mean_of_squares=0
    for i in range(len(particle_errors)):
        mean_of_squares += (particle_errors[i])**2
    mean_of_squares /= len(particle_errors)
    return math.pow((mean_of_squares),(1/2))

def predict(station_pos : typing.List[coordinate], station_dis : typing.List[float]) -> coordinate :
    '''
    Implement this function. Return a coordinate.
    station_pos : List of coordinates of stations.
    station_dis : List of distances of bot from stations.
    Raise error when not implemented or when None in distances. Wait till all distances have a value.
    Do not use any other variables than what is provided in function arguments.
    Implement your filter and predict coordinate of bot
    '''

    if None in station_dis : 
        raise SignalsNotReady("Signals haven't reached yet. Wait for it")
    else : 
        #initializing random particles
        particles = [] #list of coordinates of all assigned particles
        N = 10000 # Number of assigned particles
        for i in range(N):
            particles.append((rnd.uniform(0,1000),rnd.uniform(0,500))) # appending random particles 
        # x,y=0,0
        # for i in range(100): #if this portion of code is uncommented, then put N=33000
        #                      #this function creates equally spaced particles thorughout the screen instead of random particles
        #     x=0 
        #     for j in range(333):
        #         x+=3
        #         particles.append((x,y))
        #     y+=5
        errors = [[0 for i in range(len(station_pos))] for j in range(N)] # A 2D list storing only zeros
        #this list stores the list of errors for each particle from each station
        for i in range(N):
            for j in range(len(station_pos)):
                errors[i][j]= math.fabs(distance(particles[i],station_pos[j]) - station_dis[j])
        sum_errors = [] # this list stores the RMS value of errors from all stations
        for i in range(N):
            sum_errors.append(RMS(errors[i])) # appends the RMS values
        min_error = min(sum_errors) # finds the min error, the one with min error will be the max probability
        min_index = sum_errors.index(min_error) # finds the index of the one with the mean error
        required = particles[min_index] #finds the required particle
        return required          
        #Your code goes here
        raise NotImplementedError

def main() : 
    global DELAY

    grid = coordinate([1000, 500])

    num_stations = 6
    for i in range(num_stations) : 
        lib.Station(coordinate([rnd.random() * grid[0], rnd.random() * grid[1]]), 600)

    center = grid / 2.0
    omega = 2 * math.pi / 6
    R = 175
    
    bot = lib.Bot(coordinate(center + coordinate([0, R])), 20)
    bot._predict = predict

    for station in lib.Station.stations : 
        station.initialize()

    canvas = lib.Canvas(grid, lib.Station.stations, [bot], 10)

    key = 0

    _iter = 0
    while (key & 0xff) not in [27, 81, 113]: 
        
        _iter += 1
        _iter = _iter % 5
        if _iter == 0: 
            DELAY = time.time() - lib.calliberate()

        for station in lib.Station.stations : 
            station.send()

        lib.transmit(bot)

        pos = bot.pos
        t = time.time() - DELAY
        del_t_1 = t - bot.last_update
        # del_t_2 = 1 / bot.frequency
        theta = omega * del_t_1 / 2
        v = 2 * R * math.sin(theta) / del_t_1
        r = pos - center
        r_cap = r / r.mag()
        r_per = coordinate([r_cap[1], -r_cap[0]])
        r_per = r_per / r_per.mag()
        v_cap = r_cap * math.sin(-theta) + r_per * math.cos(theta)
        v_cap = v_cap / v_cap.mag()
        velocity = v_cap * v

        bot.move(velocity)

        bot.gps()

        canvas.update()

        key = cv2.waitKey(1)

if __name__ == '__main__' : 
    main()
