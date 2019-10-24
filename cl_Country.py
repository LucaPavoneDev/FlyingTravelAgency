# Country Object Classes
from cl_Data import database as db

class Country(object):
    def __init__(self,
                 cname    = "UNNAMED COUNTRY",
                 codeNum  = "000",
                 codeWord = "N/A"):
        # Create Country ID Number
        self.id = db.appendToList(db.countryList,self)
        # Create Country Attributes
        self.countryName    = cname    # Country Name
        self.countryCapital = None     # Location Object of Capital City (Filled in below)
        self.codeWord       = codeWord # ISO 3166-1 Alpha-3 Code (3 chars)
        self.codeNumber     = codeNum  # ISO 3166-1 Numeric Code (3 chars)
        self.locations      = []       # One country may have many locations of interest
                                       # Including its capital city.

    def __repr__(self):
        return self.countryName

    # Add location to country locations list.
    def addLocation(self,newLoc):
        if(isinstance(newLoc,Location)):
            if(newLoc not in self.locations):
                self.locations.append(newLoc)
                print("Location \'"+newLoc.name+"\' added to "+self.countryName+"'s location list.")
            else:
                pass
                print("Location is already in the list.")
        else:
            pass
            print("Given object must be a location. Terminating.")

    # Remove location from country locations list.
    def remLocation(self,oldLoc):
        if(isinstance(oldLoc,Location)):
            if(oldLoc in self.locations):
                self.locations.remove(oldLoc)
                print("Location \'"+oldLoc.name+"\' removed from "+self.countryName+"'s location list.")
            else:
                pass
                print("Location doesn't exist in the list.")
        else:
            pass
            print("Given object must be a location. Terminating.")

    # Assign a location as a capital city.
    def assignCapital(self,newCap):
        if(isinstance(newCap,Location)):
            self.countryCapital = newCap
            print("The capital of "+self.countryName+" is "+self.countryCapital.name+".")
        else:
            pass
            #print("Given object must be a location. Terminating.")

class Location(object):
    def __init__(self,
                 name = "UNNAMED LOCATION",
                 code = "N/A",
                 cap  = False):
        # Create Location ID Number
        self.id = db.appendToList(db.locationList,self)
        # Create Attributes
        self.name   = name
        self.code   = code
        self.cap    = cap

    # Some debuggery to help with showing off
    def __repr__(self):
        if(self.cap == "True"):
            return self.name+"*"
        else:
            return self.name

# Start the fun - import csv, os, and set up directory vars.
import csv, os, sqlite3

csvDir  = os.getcwd()+"\\csv\\"
locCSV  = csvDir+"locations.csv"
ctryCSV = csvDir+"countries.csv"

dbCon = sqlite3.connect("./travelAgency.db")
dbCur = dbCon.cursor()

def assignLocationsAndCapitals():
    # Assign locations and their capitals to countries, using code.
    for l in db.locationList:
        # Locations is the longer list, so it iterates through countries per location.
        for c in db.countryList:
            # Only 'do the thing' when country codes for each line up.
            if(l.code == c.codeWord):
                # Assign a capital city if there's none, and if the location is designated a capital
                if(c.countryCapital == None and l.cap == "True"):
                    c.assignCapital(l)
                # In either case, add location to country's location list.
                # Huzzah.
                c.addLocation(l)
    for c in db.countryList:
        print(c)
        print(c.locations)

def populateCountriesLocations_CSV():
    # Populate country table.
    with open(ctryCSV,newline="") as countryFile:
        ctryReader = csv.DictReader(countryFile)
        for rowC in ctryReader:
            newCountry = Country(cname    = rowC["name"],
                                 codeWord = rowC["codeword"],
                                 codeNum  = rowC["codenum"])

    # Populate Location table.
    with open(locCSV,newline="") as locationFile:
        locReader = csv.DictReader(locationFile)
        for rowL in locReader:
            newLocation = Location(name = rowL["name"],
                                   code = rowL["code"],
                                   cap  = rowL["capital"])

    # Assign Locations to Countries
    assignLocationsAndCapitals()

def populateCountriesLocations_SQL(locations,countries):
    # Add Countries
    for ctry in countries:
        name       = ctry[0]
        codeword   = ctry[1]
        codenumber = ctry[2]

        newCtry = Country(name,codeword,codenumber)
    # Add Locations
    for loc in locations:
        name = loc[0]
        code = loc[1]
        cap  = loc[2]

        newLoc = Location(name,code,cap)

    # Assign Locations to Countries
    assignLocationsAndCapitals()

dbCur.execute("SELECT name, code, capital FROM locations ORDER BY id")
locs   = dbCur.fetchall()
dbCur.execute("SELECT name, codeword, codenum FROM countries ORDER BY id")
counts = dbCur.fetchall()

# To be depricated.
populateCountriesLocations_CSV()

dbCon.close()
