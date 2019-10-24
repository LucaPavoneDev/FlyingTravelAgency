# Luca Pavone's Flying Travel Agency

# Import my classes in order, starting with data/database.
import cl_Data
# Importing product types before products leads to ... fun.
import cl_People, cl_Country, cl_Products
import cl_Hotels, cl_Insurance, cl_Transport, cl_Flights, cl_Activities
import cl_buildProds, cl_Orders

# Once all those ducks are in a row, call the interface and let that handle the doing.
print("We're alive! Fire off the Interface loop!")
import cl_Interface
print("Interface was shut down. Program ending...")
