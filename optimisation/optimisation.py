import time
import random
import math
from tabulate import tabulate


people = [('Seymour', 'BOS'),
          ('Franny', 'DAL'),
          ('Zooey', 'CAK'),
          ('Walt', 'MIA'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]
# destination NY
destination = 'LGA'

flight = {}

for line in file('schedule.txt'):
    origin, dest, time_depart, time_arrival, price = line.strip().split(
        ',')
    flight.setdefault((origin, dest), [])
    flight[(origin, dest)].append((time_depart, time_arrival, price))


def getminute(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]


def flightschedule(r):
    schedule = []
    for d in range(len(r) / 2):
        name = people[d][0]
        origin = people[d][1]
        outbound = flight[(origin, destination)][r[d * 2]]
        inbound = flight[(origin, destination)][r[d * 2 + 1]]
        schedule.append([name, origin, destination, outbound, inbound])
    return schedule


s = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
schedule_flight = flightschedule(s)
print tabulate(schedule_flight)
