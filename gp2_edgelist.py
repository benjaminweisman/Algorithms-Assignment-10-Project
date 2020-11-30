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
print("Maximum Flow:", maxFlow)



# totalFlow = 0
# for ny in ny_airports:
#     maxFlow = 0
#     for sf in sf_airports:
#         totalFlow += nx.maximum_flow(G, ny,sf)[0]


                        



# totalFlow = 0
# for ny in ny_airports:
#     maxFlow = 0
#     for sf in sf_airports:
#         flow = nx.maximum_flow(G, ny,sf)[0]
#         if flow > maxFlow:
#             source = ny
#             dest = sf
#             maxFlow = flow
#         totalFlow += maxFlow
#     # print("Maximum Flow:", maxFlow, "from", source, "to", dest)           
            



# print(carriers)
# G.edges()
# for sf in sf_airports:
#     print(G.get_edge_data('SAT', sf))

# nx.draw_networkx(G)
# mp.show()




# for ny in ny_airports:
#     for sf in sf_airports:
#         if nx.has_path(G,ny,sf):
#             print(nx.shortest_path(G,ny,sf))
            
# for mid in midpoints:
#     test = (routes["source_airport"] == "TTN") & (routes['destination_airport'] == mid)
#     test = routes[test]
#     if 
#     print(test)