import pandas as pd

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

capacity = pd.read_csv('capacity.csv')

cap_dict = pd.Series(capacity.Capacity.values, index = capacity.Code3).to_dict()

# Replace equipment keys with their associated capacity values
routes_replace = routes.replace(to_replace=cap_dict, value=None)
#routes_replace
routes_replace.to_csv('replaced.csv')