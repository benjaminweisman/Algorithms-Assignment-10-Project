Blue Team - Read Me 

To replicate our data, make sure to have "plane.dat.txt" and "routes.dat.txt" 

Creating our master data file: 
Run "Data Processing File 1.Rmd", this file inputs "routes.dat.txt" and returns: "planes_cap.csv" and "capacity.csv"
Run "Data Processing File 2.py", this file takes  "routes.dat.txt","planes.dat.txt", and "capacity.csv" and returns: "replaced.csv"
Run "Data Processing File 3.Rmd", this file takes "replaced.dat.txt" and returns "holy_grail.csv"

Next Running the Algorithm