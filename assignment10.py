import pandas as pd

routes = pd.read_csv('routes.dat.txt', names=['airline', 
                                              'airline_id',
                                              'source_airport',
                                              'source_airport_id',
                                              'destination_airport',
                                              'destination_airport_id',
                                              'codeshare', 'stops',
                                              'equipment'])

print(routes)


planes = pd.read_csv('planes.dat.txt',)
print(planes)
