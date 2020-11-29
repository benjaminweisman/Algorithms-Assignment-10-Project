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



###############################################################################

#                               READ IN DATA FILES

###############################################################################

routes = pd.read_csv('routes.dat.txt', names=['airline', 
                                              'airline_id',
                                              'source_airport',
                                              'source_airport_id',
                                              'destination_airport',
                                              'destination_airport_id',
                                              'codeshare', 
                                              'stops',
                                              'equipment'])

# Subset routes with 0 or 1 stop
routes = routes[routes["stops"] == 0]


planes = pd.read_csv('planes.dat.txt', names = ['aircraft_name',
                                                'IATA_code',
                                                'ICAO_code'])

# Plane Capacities
caps = pd.read_csv('planes_cap.csv', names=['Name', 
                                              'Code3',
                                              'Code4',
                                              'Model',
                                              'Capacity',])




###############################################################################

#                           INITIALIZE NETWORKX GRAPH

###############################################################################


G = nx.MultiDiGraph()




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

routeCheck('JFK', 'SFO')


def equipCheck(source, destination):
    '''
    Parameters
    ----------
    source : string
        source airport code (eg. JFK, LGA)
    
    destination: string
        destination airport code (eg. SFO, OAK, SJC)

    Returns
    -------
    list of equipment for each route between source and destination
    
    '''
    routes_list = (routes["source_airport"] == f"{source}") & (routes["destination_airport"] == f"{destination}")
    routes_list = routes[routes_list]
    return list(routes_list["equipment"])



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



###############################################################################

#                            IDENTIFYING EDGES

###############################################################################


# Direct Edges from NY to SF
for ny in ny_airports:
    for sf in sf_airports:
        if routeCheck(ny, sf) != 0:
            for c in airlineCheck(ny,sf):               # add an edge for each airline with a route from ny to sf
                G.add_edge(ny,sf,weight='CAPACITY', carrier=c) # CHANGE THIS WEIGHT VALUE ONCE WE HAVE CAPACITY SORTED OUT
            

# Finding routes ny -> midpoint -> sf where the carrier is the same on both legs
for ny in ny_airports:
    for mid in midpoints:
        if routeCheck(ny,mid) != 0:                                                                                 # if there is a route from ny -> mid, find all sf airports with route from mid
            for sf in sf_airports:
                if (routeCheck(mid, sf) != 0) and list(set(airlineCheck(ny,mid)) & set(airlineCheck(mid,sf))) != []: # if the same airline has routes ny -> mid and mid -> sf, then
                    carriers = list(set(airlineCheck(ny,mid)) & set(airlineCheck(mid,sf)))                           # creates list of airlines with routes ny -> mid and mid -> sf
                    for c in carriers:                                                                              # for each carrier with routes ny -> mid and mid -> sf
                        G.add_edge(ny,mid, weight='CAPACITY', carrier=c)                                            # add an edge for each carrier with a route from ny -> mid
                        G.add_edge(mid, sf, weight='CAPACITY', carrier=c)                                           # add an edge for the same carrier with a route from mid -> sf

                    

print(carriers)
G.edges()
for sf in sf_airports:
    print(G.get_edge_data('SAT', sf))







