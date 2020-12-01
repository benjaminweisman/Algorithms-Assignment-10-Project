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

# Subset routes with 0 or 1 stop
routes = routes[routes["stops"] <= 1]


planes = pd.read_csv('planes.dat.txt', names = ['aircraft_name',
                                                'IATA_code',
                                                'ICAO_code'])

# Plane Capacities
caps = pd.read_csv('planes_cap.csv', names=['Name', 
                                              'Code3',
                                              'Code4',
                                              'Model',
                                              'Capacity',])


# Initialize NetworkX directed graph
G = nx.MultiDiGraph()




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


# Subset direct routes from ny_airports to sf_airports
ny_to_sf = routes.loc[routes["destination_airport"].isin(sf_airports) & routes["source_airport"].isin(ny_airports)]
print("----------------------------")              
print(ny_to_sf)
print("----------------------------")
print(list(ny_to_sf['destination_airport']))
# # List of all airports with flights to sf airports (not sure if all ny airports should be included in this list)
# source_airports = ny_airports.copy()
# for x in midpoints:
#     if x not in source_airports:
#         source_airports.append(x)

                   


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


# If >= 1 route between ny and mid, check if there is >= 1 route from mid to sf. If so, add edge from ny to mid and add edge from mid to sf
for ny in ny_airports:
    for mid in midpoints:
        if routeCheck(ny, mid) != 0: # "if there is at least 1 direct route between ny and mid"
            for sf in sf_airports: # check if there is a direct route from mid to sf
                if routeCheck(mid, sf) != 0: # if there is >= 1 direct route between mid and sf
                    G.add_edge(ny, mid, weight=routeCheck(ny, mid))
                    G.add_edge(mid, sf, weight=routeCheck(mid, sf))
          
# Add edges for routes from ny_airports to sf_airports where # of routes >= 1
for ny in ny_airports:
    for sf in sf_airports:
        if routeCheck(ny,sf) != 0:
            G.add_edge(ny,sf, weight=routeCheck(ny,sf))



equipment_list = []

# List equipment for each route between ny and midpoint and midpoint to sf
for ny in ny_airports:
    for mid in midpoints:
        if equipCheck(ny, mid) != []:
            for sf in sf_airports:
                if equipCheck(mid, sf) != []:
                    equipment1 = equipCheck(ny,mid)
                    equipment2 = equipCheck(mid,sf)
                    for i in equipment1:
                        equipment_list.append(i)
                    for i in equipment2:
                        equipment_list.append(i)

equipment_list = list(dict.fromkeys(equipment_list)) # removes duplicates




# List airlines with routes from ny_airports to midpoints
for ny in ny_airports:
    for mid in midpoints:
        if airlineCheck(ny,mid) != []:
            print(airlineCheck(ny,mid))
        



# List paths from all ny_airports to all sf_airports
for ny in ny_airports:
    for sf in sf_airports:
        if nx.has_path(G, ny,sf):
            print(nx.shortest_path(G,ny,sf))







