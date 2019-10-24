# Reference and Features Classes
from cl_Data import database as db
from cl_Products import Vehicle

##################
# FOR TRANSPORTS #
##################

class Transport(object):
    def __init__(self,t=None,c=[],b=[],d=[],g=[]):
        # Create Transport ID
        self.id = db.appendToList(db.transpoList,self)
        # Create Transport Details
        self.transporter    = t # One transporter per product.
        self.vehicleCars    = c # One can have multiple cars.
        self.vehicleBikes   = b # One can have mutliple bikes.
        self.vehicleDrives  = d # One can offer mutliple drives.
        self.vehicleGears   = g # One can offer multiple gear types.

    def __repr__(self):
        return self.transporter.name+str("'s Depot")

class Transporter(object):
    def __init__(self,
                 newName="UNNAMED TRANSPORTER",
                 newDesc="UNDESCRIBED TRANSPORTER.",
                 newPrice=0.00):
        # Create Transporter ID Number
        self.id = db.appendToList(db.transporterList,self)
        # Add Transporter Attributes
        self.name = newName
        self.desc = newDesc
        self.baseRate = newPrice
        self.ctry = None
        self.locs = []

    def __repr__(self):
        return self.name

    def assignCountry(self,newCountry):
        from cl_Country import Country
        if(isinstance(newCountry,Country)):
            self.ctry = newCountry
            print(self.name+" is now based in "+newCountry.name)
        else:
            print("Specified object is not a Country.")

class Car(object):
    def __init__(self,
                 newName="UNNAMED CAR",
                 newDesc="UNDESCRIBED CAR.",
                 newRate=0.00):
        # Create Car ID Number
        self.id = db.appendToList(db.carsList,self)
        # Add Car Attributes
        self.name  = newName
        self.desc  = newDesc
        self.rate  = newRate

    def __repr__(self):
        return self.name

class Bike(object):
    def __init__(self,
                 newName="UNNAMED BIKE",
                 newDesc="UNDESCRIBED BIKE.",
                 newRate=0.00):
        # Create Bike ID Number
        self.id = db.appendToList(db.bikesList,self)
        # Add Bike Attributes
        self.name  = newName
        self.desc  = newDesc
        self.rate  = newRate

    def __repr__(self):
        return self.name

class Drive(object):
    def __init__(self,
                 newName="UNNAMED DRIVE",
                 newDesc="UNDESCRIBED DRIVE."):
        # Create Drive ID Number
        self.id = db.appendToList(db.driveList,self)
        # Add Drive Attributes
        self.name  = newName
        self.desc  = newDesc

    def __repr__(self):
        return self.name

class Gears(object):
    def __init__(self,
                 newName="UNNAMED GEARS",
                 newDesc="UNDESCRIBED GEARS."):
        # Create Gear ID Number
        self.id = db.appendToList(db.gearList,self)
        # Add Gear Attributes
        self.name  = newName
        self.desc  = newDesc

    def __repr__(self):
        return self.name

# Start the fun - import csv, os, and set up directory vars.
import csv, os, sqlite3
from ast import literal_eval as leval

csvDir  = os.getcwd()+"\\csv\\vehicles\\"
tranCSV = csvDir+"transporters.csv"
carCSV  = csvDir+"cars.csv"
bikeCSV = csvDir+"bikes.csv"
gearCSV = csvDir+"gears.csv"
driveCSV= csvDir+"drives.csv"
tporCSV = csvDir+"transports.csv"
vehiCSV = csvDir+"vehicles.csv"

dbCon = sqlite3.connect("./travelAgency.db")
dbCur = dbCon.cursor()

def populateTable_SQL(tuplist,obj,comment="Database"):
    for t in tuplist:
        if(len(t) == 2):
            # Tuple contains 2 objects
            n = str(t[0])
            d = str(t[1])

            nObj = obj(n,d)
            print(nObj.name+" added to "+comment+" at #"+str(nObj.id)+".")
        elif(len(t) == 3):
            # Tuple contains 3 objects.
            n = str(t[0])
            d = str(t[1])
            r = float(t[2])

            nObj = obj(n,d,r)
            print(nObj.name+" added to "+comment+" at #"+str(nObj.id)+".")
        else:
            print("Tuple must be 2 or 3 things long.")

def createTransportDepots_SQL(tuplist):
    for depot in tuplist:
        t = db.getObjFromList("transporterList",int(depot[0]))
        c = str(depot[1])
        b = str(depot[2])
        d = str(depot[3])
        g = str(depot[4])

        cl = c.split("|")
        bl = b.split("|")
        dl = d.split("|")
        gl = g.split("|")

        co = []
        bo = []
        do = []
        go = []

        for ci in cl:
            co.append(db.getObjFromList("carsList",int(ci)))
        for bi in bl:
            bo.append(db.getObjFromList("bikesList",int(bi)))
        for di in dl:
            do.append(db.getObjFromList("driveList",int(di)))
        for gi in gl:
            go.append(db.getObjFromList("gearList",int(gi)))

        nt = Transport(t,co,bo,do,go)

dbCur.execute("SELECT name, desc, rate FROM vehicle_transporters ORDER BY id")
transporters_list = dbCur.fetchall()
populateTable_SQL(transporters_list,Transporter,"Transporter List")

dbCur.execute("SELECT name, desc, rate FROM vehicle_cars ORDER BY id")
cars_list         = dbCur.fetchall()
populateTable_SQL(cars_list,Car,"Car List")

dbCur.execute("SELECT name, desc, rate FROM vehicle_bikes ORDER BY id")
bikes_list        = dbCur.fetchall()
populateTable_SQL(bikes_list,Bike,"Bike List")

dbCur.execute("SELECT name, desc FROM vehicle_gears ORDER BY id")
gears_list        = dbCur.fetchall()
populateTable_SQL(gears_list,Gears,"Gears List")

dbCur.execute("SELECT name, desc FROM vehicle_drives ORDER BY id")
drives_list       = dbCur.fetchall()
populateTable_SQL(drives_list,Drive,"Drives List")

dbCur.execute("""
SELECT transporter_id, cars, bikes, drives, gears
FROM vehicle_depots
ORDER BY transporter_id
""")
depot_list        = dbCur.fetchall()
createTransportDepots_SQL(depot_list)

dbCon.close()

'''
def createVehicles_SQL(tuplist):
    for tup in tuplist:
        name  = str(tup[0])
        desc  = str(tup[1])
        trans = db.getObjFromList("transporterList",int(tup[2]))
        vtype = str(tup[3])
        mod   = int(tup[4])
        drive = db.getObjFromList("driveList",int(tup[5]))
        gears = db.getObjFromList("gearList",int(tup[6]))

        if(vtype.lower() == "car"):
            model = db.getObjFromList("carsList",mod)
        elif(vtype.lower() == "bike"):
            model = db.getObjFromList("bikesList",mod)
        else:
            print("Either 'car' or 'bike' expected from vtype. Continuing.")
            continue

        nv = Vehicle(trans,model,drive,gears)
        nv.updateName(name)
        nv.updateDesc(desc)
        nv.calcVehiclePrice(True)

dbCur.execute("""
SELECT products.name,
       products.desc,
       prods_vehicles.transporter,
       prods_vehicles.vtype,
       prods_vehicles.model,
       prods_vehicles.drive,
       prods_vehicles.gears
FROM products INNER JOIN prods_vehicles
ON products.pid = prods_vehicles.pid
ORDER BY prods_vehicles.pid
""")
vehicle_list = dbCur.fetchall()

createVehicles_SQL(vehicle_list)
'''

'''
def createVehicles_CSV(file,p=False):
    with open(file,newline="") as tFile:
        vReader = csv.DictReader(tFile)
        for rowV in vReader:
            name  = str(rowV["name"])
            desc  = str(rowV["desc"])
            tran  = db.transporterList[int(rowV["transporter"])]
            vtype = str(rowV["vtype"])
            mod   = int(rowV["model"])
            drive = db.driveList[int(rowV["drive"])]
            gears = db.gearList[int(rowV["gears"])]

            if(vtype == "car"):
                model = db.carsList[mod]
            elif(vtype == "bike"):
                model = db.bikesList[mod]
            else:
                print("Either 'car' or 'bike' expected from vtype. Continuing.")
                continue

            nv = Vehicle(tran,model,drive,gears)
            nv.updateName(name)
            nv.updateDesc(desc)
            nv.calcVehiclePrice(True)
            if(p == True):
                print(nv)
                print(nv.desc)
                print(nv.drive)
                print(nv.gears)

createVehicles_CSV(vehiCSV,True)
'''

# Old CSV code here.

'''
def populateTable_CSV(file,obj,rates=True,comment="Database"):
    with open(file,newline="") as nFile:
        nReader = csv.DictReader(nFile)
        for rowN in nReader:
            n = rowN["name"]
            d = rowN["desc"]
            if(rates == True):
                r = leval(rowN["rate"])
                nObj = obj(n,d,r)
            else:
                nObj = obj(n,d)
            print(nObj.name+" added to "+comment+" at #"+str(nObj.id)+".")

# Populate Transporters Table
populateTable_CSV(tranCSV,Transporter,True,"Transporter List")

# Populate Cars Table
populateTable_CSV(carCSV,Car,True,"Car List")

# Populate Bikes Table
populateTable_CSV(bikeCSV,Bike,True,"Bike List")

# Populate Gears Table
populateTable_CSV(gearCSV,Gears,False,"Gear List")

# Populate Drives Table
populateTable_CSV(driveCSV,Drive,False,"Drive List")


# Create Transports (Not 'Transporter's!) from the Above using MAGIC!
with open(tporCSV,newline="") as tFile:
    tReader = csv.DictReader(tFile)
    for rowT in tReader:
        # Get initial variables and derive lists from products.
        t = db.transporterList[int(rowT["trans"])]
        c = rowT["cars"]
        b = rowT["bikes"]
        d = rowT["drives"]
        g = rowT["gears"]

        cl = c.split("|")
        bl = b.split("|")
        dl = d.split("|")
        gl = g.split("|")

        co = []
        bo = []
        do = []
        go = []

        # Iterate and Add to object lists to create Transporter object.
        for ci in cl:
            co.append(db.carsList[int(ci)])
        for bi in bl:
            bo.append(db.bikesList[int(bi)])
        for di in dl:
            do.append(db.driveList[int(di)])
        for gi in gl:
            go.append(db.gearList[int(gi)])

        nObj = Transport(t,co,bo,do,go)
        print(nObj.transporter)

# Create some ready-available Vehicles from Transporters and their Data.
# The idea is you should be able to create vehicles from transporters' choices.
# Later on down the line.
'''