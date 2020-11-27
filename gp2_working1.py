#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:51:47 2020

@author: julianpalazzo
"""

import pandas as pd

proj = '/Users/julianpalazzo/New College of Florida/Fall Semester 2020/CAP5328 Algorithms for Data Science/Group_Project_2'
data = '/data/'




routes = pd.read_csv('routes.dat.txt', names=['airline', 
                                              'airline_id',
                                              'source_airport',
                                              'source_airport_id',
                                              'destination_airport',
                                              'destination_airport_id',
                                              'codeshare', 
                                              'stops',
                                              'equipment'])


# routes = routes[routes["stops" == 1]]


planes = pd.read_csv('planes.dat.txt', names = ['aircraft_name',
                                                'IATA_code',
                                                'ICAO_code'])
planes






# To filter only NY airports

# Subset Routes for all NY source_airports
ny_airports = ['LGA', 'JFK', 'ISP', 'SWF', 'TTN', 'HPN', 'EWR']
routes_from_ny = routes.loc[routes["source_airport"].isin(ny_airports)]


# Subset Routes to San Francisco Airports
sf_airports = ['SFO', 'SJC', 'OAK']
routes_to_sf = routes.loc[routes["destination_airport"].isin(sf_airports)]
                        

midpoints = list(routes_to_sf["source_airport"])

# Subset Routes from NY to layover airport between NY and SF
ny_to_midpoint = routes_from_ny.loc[routes_from_ny["destination_airport"].isin(midpoints)]
# need to merge this df with the routes_to_sf dataframe?
                         

# List of all airports with flights to sf airports (not sure if all ny airports should be included in this list)
source_airports = ny_airports
for x in midpoints:
    if x not in source_airports:
        source_airports.append(x)

len(source_airports)                  
           
            
           
            
           
sfo = routes["destination_airport"] == "SFO"
sfo = routes[sfo]
len(sfo)


# list of airports with flights to SFO
source_to_sfo = list(sfo["source_airport"])
len(source_to_sfo)

# Subset ny_routes for 
ny_to_sfo = ny_routes.loc[ny_routes["destination_airport"].isin(source_to_sfo)]



lga = routes["source_airport"] == "LGA"
lga = routes[lga]
len(lga)

jfk = routes["source_airport"] == "JFK"
jfk = routes[jfk]
len(jfk)


# There are 7 nonstop flights from JFK to SFO
jfk_to_sfo = (routes["source_airport"] == "JFK") & (routes["destination_airport"] == "SFO")
jfk_to_sfo = routes[jfk_to_sfo]
len(jfk_to_sfo)


ny_airports = ['LGA', 'JFK', 'ISP', 'SWF', 'TTN', 'HPN', 'EWR']
routes.loc[routes["source_airport"].isin(ny_airports)]






            
# Select airports that are midpoint for flights from LGA to SFO        
lga.loc[lga["destination_airport"].isin(source_to_sfo)]          



lga[lga["destination_airport"] in source_to_sfo]
