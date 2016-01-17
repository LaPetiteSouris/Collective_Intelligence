import time
import random
import math
from tabulate import tabulate

# Flight schedule

s = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
people = [('Seymour', 'BOS'),
          ('Franny', 'DAL'),
          ('Zooey', 'CAK'),
          ('Walt', 'MIA'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]
# destination NY
destination = 'LGA'

flights = {}

for line in file('optimisation/schedule.txt'):
    origin, dest, time_depart, time_arrival, price = line.strip().split(
        ',')
    flights.setdefault((origin, dest), [])
    flights[(origin, dest)].append((time_depart, time_arrival, int(price)))


def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]


def flightschedule(r):
    schedule = []
    for d in range(len(r) / 2):
        name = people[d][0]
        origin = people[d][1]
        outbound = flights[(origin, destination)][r[d * 2]]
        inbound = flights[(origin, destination)][r[d * 2 + 1]]
        schedule.append([name, origin, destination, outbound, inbound])
    return schedule


def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24 * 60

    for d in range(len(sol) / 2):
        # Get the inbound and outbound flights
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d * 2])]
        returnf = flights[(destination, origin)][int(sol[d * 2 + 1])]
        # Total price is the price of all outbound and return flights
        totalprice += outbound[2]
        totalprice += returnf[2]

        # Track the latest arrival and earliest departure
        if latestarrival < getminutes(outbound[1]):
            latestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]):
            earliestdep = getminutes(returnf[0])

    # Every person must wait at the airport until the latest person arrives.
    # They also must arrive at the same time and wait for their flights.
    totalwait = 0
    for d in range(len(sol) / 2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d * 2])]
        returnf = flights[(destination, origin)][int(sol[d * 2 + 1])]
        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep

    # Does this solution require an extra day of car rental? That'll be $50!
    if latestarrival > earliestdep:
        totalprice += 50

    return totalprice + totalwait


def randomhillclimbing(domain):

    solution = [random.randint(domain[i][0], domain[i][1])
                for i in range(len(domain))]
    while 1:
        # For each random solution from beginning
        # take one neigbhor on left and one on right
        neigbhor = []
        for j in range(len(solution)):
            up_neighbor = solution[j] + 1
            down_neighbor = solution[j] - 1
            # Stop moving if out of bound
            if up_neighbor > domain[j][1]:
                up_neighbor = domain[j][1]
            if down_neighbor < domain[j][0]:
                down_neighbor = domain[j][0]
            neigbhor.append(
                solution[1:j] + [up_neighbor] + solution[j + 1:])
            neigbhor.append(
                solution[1:j] + [down_neighbor] + solution[j + 1:])
        current_cost = schedulecost(solution)
        best_cost = current_cost
        for i in range(len(neigbhor)):
            cost = schedulecost(neigbhor[i])
            if cost < best_cost:
                best_cost = cost
                solution = neigbhor[i]

        # if there is no change whatso ever , then we have reached the bottom
        if best_cost == current_cost:
            break
    return solution


domain = [(0, 8)] * (len(people) * 2)
s = randomhillclimbing(domain)
cost = schedulecost(s)
schedule_flight = flightschedule(s)
print tabulate(schedule_flight)
print 'Final cost is %d' % cost
