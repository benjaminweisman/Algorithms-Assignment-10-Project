#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 22:01:07 2020

@author: julianpalazzo
"""

import pandas as pd
import networkx as nx

routes = pd.read_csv('routes.dat.txt', names=['airline', 
                                              'airline_id',
                                              'source_airport',
                                              'source_airport_id',
                                              'destination_airport',
                                              'destination_airport_id',
                                              'codeshare', 
                                              'stops',
                                              'equipment'])




planes = pd.read_csv('planes.dat.txt', names = ['aircraft_name',
                                                'IATA_code',
                                                'ICAO_code'])


# Initialize NetworkX directed graph
G = nx.DiGraph()




# To filter only NY airports

# Subset Routes for all NY source_airports
ny_airports = ['LGA', 'JFK', 'ISP', 'SWF', 'TTN', 'HPN', 'EWR']
routes_from_ny = routes.loc[routes["source_airport"].isin(ny_airports)]


# Subset Routes to San Francisco Airports
sf_airports = ['SFO', 'SJC', 'OAK']
routes_to_sf = routes.loc[routes["destination_airport"].isin(sf_airports)]
                        
# list of airports that fly directly to all sf_airports
midpoints = list(routes_to_sf["source_airport"])
midpoints = list(dict.fromkeys(midpoints)) # removes duplicates

# Subset Routes from NY to layover airport between NY and SF
ny_to_midpoint = routes_from_ny.loc[routes_from_ny["destination_airport"].isin(midpoints)]

                         

# List of all airports with flights to sf airports (not sure if all ny airports should be included in this list)
source_airports = ny_airports
for x in midpoints:
    if x not in source_airports:
        source_airports.append(x)

                  


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
    return list(routes_list["equipment"])
    # return len(routes_list)
    # print(len(routes_list), "direct routes")

routeCheck('JFK', 'SFO')

# Uses routeCheck to list number of direct flights between all ny_airports and sf_airports
for ny in ny_airports:
    for sf in sf_airports:
        if routeCheck(ny, sf) != 0:
            print(routeCheck(ny, sf), "routes from", ny, "to", sf)






# Uses routeCheck to find # of routes between ny and midpoint + # of routes from midpoint to sf
for ny in ny_airports:
    for mid in midpoints:
        if routeCheck(ny, mid) != 0:
            for sf in sf_airports:
                if routeCheck(mid, sf) != 0:
                    print(routeCheck(ny, mid), "+", routeCheck(mid, sf), "routes")

for ny in ny_airports:
    for mid in midpoints:
        if routeCheck(ny, mid) != 0:
            G.add_edge(ny, mid, weight=routeCheck(ny,mid))
            
            # for sf in sf_airports:
            #     if routeCheck(mid, sf) != 0:
            #         G.add_edge()

nx.edges(G)






