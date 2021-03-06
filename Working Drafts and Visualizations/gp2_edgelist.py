#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 16:16:54 2020

@author: julianpalazzo
"""

###############################################################################

#                                   LIBRARIES

###############################################################################


import pandas as pd
import networkx as nx
import matplotlib.pyplot as mp


###############################################################################

#                               READ IN DATA FILES

###############################################################################

# routes = pd.read_csv('routes.dat.txt', names=['airline', 
#                                               'airline_id',
#                                               'source_airport',
#                                               'source_airport_id',
#                                               'destination_airport',
#                                               'destination_airport_id',
#                                               'codeshare', 
#                                               'stops',
#                                               'equipment'])


# routes = pd.read_csv('holy_grail.csv', names = ['airline',
#                                                 'airline_id',
#                                                 'source_airport',
#                                                 'source_airport_id',
#                                                 'destination_airport',
#                                                 'destination_airport_id',
#                                                 'codeshare', 
#                                                 'stops',
#                                                 'totalcap'])
                  

routes = pd.read_csv('holy_grail.csv')

                              

# Subset routes with 0 or 1 stop
routes = routes[routes["stops"] == 0]


# planes = pd.read_csv('planes.dat.txt', names = ['aircraft_name',
#                                                 'IATA_code',
#                                                 'ICAO_code'])


# # Plane Capacities
# caps = pd.read_csv('planes_cap.csv', names=['Name', 'Code3', 'Code4', 'Model', 'Capacity',])

# Plane Capacities
# capacity = pd.read_csv('capacity.csv')


# routes_clean = pd.read_csv('routes_clean2.csv', names = ['airline',
#                                                           'airline_id',
#                                                           'source_airport',
#                                                           'source_airport_id',
#                                                           'destination_airport',
#                                                           'destination_airport_id',
#                                                           'codeshare', 
#                                                           'stops',
#                                                           'equipment1',
#                                                           'equipment2',
#                                                             'equipment3',
#                                                             'equipment4',
#                                                               'equipment5',
#                                                               'equipment6',
#                                                                 'equipment7',
#                                                                 'equipment8',
#                                                                   'equipment9'])

# routes_clean = pd.read_csv('routes_clean2.csv', dtype = {"col1": "string", "col2": "string","col3": "string","col4": "string","col5": "string","col6":"string","col7": "string","col8": "string","col9": "string" })

###############################################################################

#                    REPLACE EQUIPMENT VALUES WITH CAPACITY

###############################################################################

# routes.reset_index()

# # split multi-value equipment fields
# routes = pd.DataFrame(routes.equipment.str.split(" ").tolist(), index=routes.index).stack()

# Create dictionary of equipment : capacity values
# cap_dict = pd.Series(capacity.Capacity.values, index = capacity.Code3).to_dict()

# Replace equipment keys with their associated capacity values
# routes = routes.replace(to_replace=cap_dict, value=None)




###############################################################################

#                               FUNCTIONS

###############################################################################

def routeCheck(source, destination):
    '''
    Parameters
    ----------
    source : string
        source airport code (eg. JFK, LGA)
    
    destination: string
        destination airport code (eg. SFO, OAK, SJC)

    Returns
    -------
    number of direct routes between source and destination
    
    '''
    routes_list = (routes["source_airport"] == f"{source}") & (routes["destination_airport"] == f"{destination}")
    routes_list = routes[routes_list]
    return len(routes_list)
    # print(len(routes_list), "direct routes")

# routeCheck('JFK', 'SFO')


# def equipCheck(source, destination):
#     '''
#     Parameters
#     ----------
#     source : string
#         source airport code (eg. JFK, LGA)
    
#     destination: string
#         destination airport code (eg. SFO, OAK, SJC)

#     Returns
#     -------
#     list of equipment for each route between source and destination
    
#     '''
#     routes_list = (routes["source_airport"] == f"{source}") & (routes["destination_airport"] == f"{destination}")
#     routes_list = routes[routes_list]
#     return list(routes_list["equipment"])



def airlineCheck(source, destination):
    '''
    Parameters
    ----------
    source : string
        source airport code (eg. JFK, LGA)
    
    destination: string
        destination airport code (eg. SFO, OAK, SJC)

    Returns
    -------
    list of airlines with route between source and destination
    
    '''
    routes_list = (routes["source_airport"] == f"{source}") & (routes["destination_airport"] == f"{destination}")
    routes_list = routes[routes_list]
    return list(routes_list["airline"])



# def capacityCheck(source, destination, carrier):
#     '''
#     Parameters
#     ----------
#     source : string
#         source airport code (eg. JFK, LGA)
    
#     destination: string
#         destination airport code (eg. SFO, OAK, SJC)
        
#     carrier: string
#         airline carrier for a given route

#     Returns
#     -------
#     capacity of route between source and destination for a given airline
    
#     '''
#     cap = 0
#     routes_list = (routes["source_airport"] == f"{source}") & (routes["destination_airport"] == f"{destination}") & (routes["airline"] == f"{carrier}")
#     routes_list = routes[routes_list]
#     for e in routes_list["equipment"]:
#         cap += int(e)
#     return cap
    

def capacityCheck(source, destination, carrier):
    '''
    Parameters
    ----------
    source : string
        source airport code (eg. JFK, LGA)
    
    destination: string
        destination airport code (eg. SFO, OAK, SJC)
        
    carrier: string
        airline carrier for a given route

    Returns
    -------
    capacity of route between source and destination for a given airline
    
    '''
    # cap = 0
    routes_list = (routes["source_airport"] == f"{source}") & (routes["destination_airport"] == f"{destination}") & (routes["airline"] == f"{carrier}")
    routes_list = routes[routes_list]
    # for e in routes_list["totalcap"]:
        # cap += int(e)
    # return cap
    return sum(routes_list["totalcap"])

###############################################################################

#                            FILTERING ROUTES

###############################################################################



# Subset Routes leaving from all NY airports
ny_airports = ['LGA', 'JFK', 'ISP', 'SWF', 'TTN', 'HPN', 'EWR']
routes_from_ny = routes.loc[routes["source_airport"].isin(ny_airports)]


# Subset Routes arriving at San Francisco Airports
sf_airports = ['SFO', 'SJC', 'OAK']
routes_to_sf = routes.loc[routes["destination_airport"].isin(sf_airports)]
                        
# list of airports that fly directly to all sf_airports
midpoints = list(routes_to_sf["source_airport"])
midpoints = list(dict.fromkeys(midpoints)) # removes duplicates

# Subset Routes from NY to layover airport between NY and SF
ny_to_midpoint = routes_from_ny.loc[routes_from_ny["destination_airport"].isin(midpoints)]


# Remove TTN - it is a small airport with only one budget airline 
ny_airports.remove('TTN')


###############################################################################

#                           INITIALIZE NETWORKX GRAPH

###############################################################################


G = nx.DiGraph()



###############################################################################

#                            ADDING EDGES TO GRAPH

###############################################################################


# Direct Edges from NY to SF
for ny in ny_airports:
    for sf in sf_airports:
        if routeCheck(ny, sf) != 0:
            for c in airlineCheck(ny,sf):               # add an edge for each airline with a route from ny to sf
             
                G.add_edge(ny,sf,capacity=capacityCheck(ny, sf,c), carrier=c)


# Finding routes ny -> midpoint -> sf where the carrier is the same on both legs
for ny in ny_airports:
    for mid in midpoints:
        if routeCheck(ny,mid) != 0:                                                                                 # if there is a route from ny -> mid, find all sf airports with route from mid
            for sf in sf_airports:
                if (routeCheck(mid, sf) != 0) and list(set(airlineCheck(ny,mid)) & set(airlineCheck(mid,sf))) != []: # if the same airline has routes ny -> mid and mid -> sf, then
                    carriers = list(set(airlineCheck(ny,mid)) & set(airlineCheck(mid,sf)))                           # creates list of airlines with routes ny -> mid and mid -> sf
                    for c in carriers:                                                                              # for each carrier with routes ny -> mid and mid -> sf
                        G.add_edge(ny,mid,capacity=capacityCheck(ny, mid,c), carrier=c)                                            # add an edge for each carrier with a route from ny -> mid
                        G.add_edge(mid,sf,capacity=capacityCheck(mid, sf,c), carrier=c)                                           # add an edge for the same carrier with a route from mid -> sf
                        




allFlows = []
for ny in ny_airports:
    for sf in sf_airports:
        print("Max Flow from", ny,"to", sf,"is",  nx.maximum_flow(G, ny,sf)[0])
        allFlows.append(nx.maximum_flow(G, ny,sf)[0])
maxFlow = sum(allFlows)

print("\n") 
print("PROBLEM 1 SOLUTION \n")
print("Maximum Flow:", maxFlow)



##############################################################################

#                               PROBLEM 2

###############################################################################


def routeCheckR(source, destination, df):
    '''
    Parameters
    ----------
    source : string
        source airport code (eg. JFK, LGA)
    
    destination: string
        destination airport code (eg. SFO, OAK, SJC)

    Returns
    -------
    number of direct routes between source and destination
    
    '''
    routes_list = (df["source_airport"] == f"{source}") & (df["destination_airport"] == f"{destination}")
    routes_list = df[routes_list]
    return len(routes_list)

def capacityCheckR(source, destination, carrier, df):
    '''
    Parameters
    ----------
    source : string
        source airport code (eg. JFK, LGA)
    
    destination: string
        destination airport code (eg. SFO, OAK, SJC)
        
    carrier: string
        airline carrier for a given route

    Returns
    -------
    capacity of route between source and destination for a given airline
    
    '''
    # cap = 0
    routes_list = (df["source_airport"] == f"{source}") & (df["destination_airport"] == f"{destination}") & (df["airline"] == f"{carrier}")
    routes_list = df[routes_list]
    return int(routes_list["totalcap"])


airline_list = [] # list of carriers for edges in G


# Carriers for Direct Edges from NY to SF
for ny in ny_airports:
    for sf in sf_airports:
        if routeCheck(ny, sf) != 0:
            for c in airlineCheck(ny,sf):               
                airline_list.append(c)


# Carriers with routes ny -> midpoint -> sf where the carrier is the same on both legs
for ny in ny_airports:
    for mid in midpoints:
        if routeCheck(ny,mid) != 0:                                                                                 # if there is a route from ny -> mid, find all sf airports with route from mid
            for sf in sf_airports:
                if (routeCheck(mid, sf) != 0) and list(set(airlineCheck(ny,mid)) & set(airlineCheck(mid,sf))) != []: # if the same airline has routes ny -> mid and mid -> sf, then
                    carriers = list(set(airlineCheck(ny,mid)) & set(airlineCheck(mid,sf)))                           # creates list of airlines with routes ny -> mid and mid -> sf
                    for c in carriers:                                                                              # for each carrier with routes ny -> mid and mid -> sf
                        airline_list.append(c)
    
airline_list = list(dict.fromkeys(airline_list)) # removes duplicates


maxMaxFlow = 0

for c in airline_list:
    r = routes[routes["airline"] == f"{c}"] # subset routes df for each airline

    M = nx.DiGraph()                        # initialize Directed Graph
    
    for ny in ny_airports:
        for sf in sf_airports:
            if routeCheckR(ny, sf, r) != 0:
                M.add_edge(ny,sf, capacity=capacityCheckR(ny,sf, c, r)) # add edges for direct routes ny -> sf
    
    for ny in ny_airports:
        for mid in midpoints:
            if routeCheckR(ny,mid,r) != 0:                                                                               
                for sf in sf_airports:
                    if (routeCheckR(mid, sf, r) != 0):
                        M.add_edge(ny,mid,capacity=capacityCheckR(ny, mid, c, r))
                        M.add_edge(mid, sf,capacity=capacityCheckR(mid, sf, c, r))
    maxFlow = 0
    for ny in ny_airports:
        for sf in sf_airports:
            if nx.has_path(M, ny, sf):
                flow = nx.maximum_flow(M, ny,sf)[0]
            if flow >= maxFlow:
                maxFlow = flow
    
    if maxFlow >= maxMaxFlow:
        maxMaxFlow = maxFlow
        maxFlowCarrier = c

print("\n \n")
print("PROBLEM 2 SOLUTION \n")
print("Max Flow Carrier:", maxFlowCarrier, "\nMax Flow Capacity:", maxMaxFlow, "passengers")

    
    
    
#                       SCRATCH WORK BELOW
    
# RUN THIS CHUNK TO SEE WHAT'S HAPPENING
for c in airline_list:
    r = routes[routes["airline"] == f"{c}"]
    M = nx.DiGraph()
    for ny in ny_airports:
        for mid in midpoints:
            for sf in sf_airports:
                if routeCheckR(ny,sf,r):
                    M.add_edge(ny,sf, capacity = capacityCheckR(ny,sf,c,r))
                if routeCheckR(ny,mid,r) and routeCheckR(mid,sf,r):
                    M.add_edge(ny,mid,capacity = capacityCheckR(ny,mid,c,r))
                    M.add_edge(mid,sf,capacity = capacityCheckR(mid,sf,c,r))                    
    print(c, M.edges())


# THIS IS THE SOLUTION
solution = 0
for c in airline_list:
    r = routes[routes["airline"] == f"{c}"]
    M = nx.DiGraph()
    for ny in ny_airports:
        for mid in midpoints:
            for sf in sf_airports:
                if routeCheckR(ny,sf,r):
                    M.add_edge(ny,sf, capacity = capacityCheckR(ny,sf,c,r))
                    
                    # print("LINE ONE",capacityCheckR(ny,sf,c,r))
                    
                if routeCheckR(ny,mid,r) and routeCheckR(mid,sf,r):
                    M.add_edge(ny,mid,capacity = capacityCheckR(ny,mid,c,r))
                    M.add_edge(mid,sf,capacity = capacityCheckR(mid,sf,c,r))
                    
                    # print("LINE TWO",capacityCheckR(ny,mid,c,r), capacityCheckR(mid,sf,c,r)) # the problem is with capacityCheckR?
    for u in M:
        for v in M:
            if u != v:
                flowC = nx.maximum_flow(M,u,v)[0]
                if flowC >= solution:
                    solution = flowC
                    
                    
                    
    # print(c, M.edges())

print("SOLUTION:", solution)





## Checking the function results before adding edges
# for c in airline_list:
#     r = routes[routes["airline"] == f"{c}"]

#     for ny in ny_airports:
#         for mid in midpoints:
#             if routeCheckR(ny,mid,r):
#                 for sf in sf_airports:
#                     if routeCheckR(mid,sf,r):
#                         print(ny,mid,routeCheckR(ny,mid,r), mid, sf, routeCheckR(mid, sf, r))
#                         print(capacityCheckR(ny,mid,c,r), capacityCheckR(mid,sf,c,r))



# #                   BROKEN SOLUTION


# maxMaxFlow = 0

# for c in airline_list:
#     r = routes[routes["airline"] == f"{c}"] # subset routes df for each airline
#     M = nx.DiGraph()                        # initialize Directed Graph
    
#     for ny in ny_airports:
#         for sf in sf_airports:
#             if routeCheckR(ny, sf, r) != 0:
#                 M.add_edge(ny,sf, capacity=capacityCheckR(ny,sf, c, r)) # add edges for direct routes ny -> sf
    
#     for ny in ny_airports:
#         for mid in midpoints:
#             if routeCheckR(ny,mid,r) != 0:                                                                               
#                 for sf in sf_airports:
#                     if (routeCheckR(mid, sf,r) != 0):
#                         M.add_edge(ny,mid,capacity=capacityCheckR(ny, mid, c, r))
#                         M.add_edge(mid, sf,capacity=capacityCheckR(mid, sf, c, r))
#     maxFlow = 0
#     for ny in ny_airports:
#         for sf in sf_airports:
#             if nx.has_path(M, ny, sf):
#                 flow = nx.maximum_flow(M, ny,sf)[0]
#             if flow >= maxFlow:
#                 maxFlow = flow
    
#     if maxFlow >= maxMaxFlow:
#         maxMaxFlow = maxFlow
#         maxFlowCarrier = c
        
# print("\n \n")
# print("PROBLEM 2 SOLUTION \n")
# print("Max Flow Carrier:", maxFlowCarrier, "\nMax Flow Capacity:", maxMaxFlow, "passengers")