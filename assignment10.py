import pandas as pd

#Importing and Initializing our datasets
routes = pd.read_csv('routes.dat.txt', names=['airline', 
                                              'airline_id',
                                              'source_airport',
                                              'source_airport_id',
                                              'destination_airport',
                                              'destination_airport_id',
                                              'codeshare', 'stops',
                                              'equipment'])

planes = pd.read_csv('planes.dat.txt',)

#Showing our datasets
print(routes)
print(planes)



# To filter only NY airports
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






sfo = routes["destination_airport"] == "SFO"
sfo = routes[sfo]
len(sfo)

# list of airports with flights to SFO
source_to_sfo = list(sfo["source_airport"])
len(source_to_sfo)



# Select airports that are midpoint for flights from LGA to SFO
for a in source_to_sfo:
    for b in lga["destination_airport"]:
        if a == b:
            print("LGA", a, "SFO")
