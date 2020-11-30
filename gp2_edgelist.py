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


# # Plane Capacities
# caps = pd.read_csv('planes_cap.csv', names=['Name', 'Code3', 'Code4', 'Model', 'Capacity',])

# Plane Capacities
capacity = pd.read_csv('capacity.csv')


routes_clean = pd.read_csv('routes_clean2.csv', names = ['airline',
                                                          'airline_id',
                                                          'source_airport',
                                                          'source_airport_id',
                                                          'destination_airport',
                                                          'destination_airport_id',
                                                          'codeshare', 
                                                          'stops',
                                                          'equipment1',
                                                          'equipment2',
                                                            'equipment3',
                                                            'equipment4',
                                                              'equipment5',
                                                              'equipment6',
                                                                'equipment7',
                                                                'equipment8',
                                                                  'equipment9'])

# routes_clean = pd.read_csv('routes_clean2.csv', dtype = {"col1": "string", "col2": "string","col3": "string","col4": "string","col5": "string","col6":"string","col7": "string","col8": "string","col9": "string" })

###############################################################################

#                    REPLACE EQUIPMENT VALUES WITH CAPACITY

###############################################################################

routes.reset_index()

# # split multi-value equipment fields
# routes = pd.DataFrame(routes.equipment.str.split(" ").tolist(), index=routes.index).stack()

# Create dictionary of equipment : capacity values
cap_dict = pd.Series(capacity.Capacity.values, index = capacity.Code3).to_dict()

# Replace equipment keys with their associated capacity values
routes = routes.replace(to_replace=cap_dict, value=None)


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
    cap = 0
    routes_list = (routes["source_airport"] == f"{source}") & (routes["destination_airport"] == f"{destination}") & (routes["airline"] == f"{carrier}")
    routes_list = routes[routes_list]
    for e in routes_list["equipment"]:
        cap += int(e)
    return cap
    

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
                # G.add_edge(ny,sf,weight='CAPACITY', carrier=c) # CHANGE THIS WEIGHT VALUE ONCE WE HAVE CAPACITY SORTED OUT
                
                try:
                    G.add_edge(ny,sf,weight=capacityCheck(ny, sf,c), carrier=c)
                except: continue

# Finding routes ny -> midpoint -> sf where the carrier is the same on both legs
for ny in ny_airports:
    for mid in midpoints:
        if routeCheck(ny,mid) != 0:                                                                                 # if there is a route from ny -> mid, find all sf airports with route from mid
            for sf in sf_airports:
                if (routeCheck(mid, sf) != 0) and list(set(airlineCheck(ny,mid)) & set(airlineCheck(mid,sf))) != []: # if the same airline has routes ny -> mid and mid -> sf, then
                    carriers = list(set(airlineCheck(ny,mid)) & set(airlineCheck(mid,sf)))                           # creates list of airlines with routes ny -> mid and mid -> sf
                    for c in carriers:                                                                              # for each carrier with routes ny -> mid and mid -> sf
                        # G.add_edge(ny,mid, weight='CAPACITY', carrier=c)                                            # add an edge for each carrier with a route from ny -> mid
                        # G.add_edge(mid, sf, weight='CAPACITY', carrier=c)                                           # add an edge for the same carrier with a route from mid -> sf
                        try:
                            G.add_edge(ny,mid,weight=capacityCheck(ny, mid,c), carrier=c)
                            G.add_edge(mid,sf,weight=capacityCheck(mid, sf,c), carrier=c)
                        except: continue

# print(carriers)
# G.edges()
# for sf in sf_airports:
#     print(G.get_edge_data('SAT', sf))







