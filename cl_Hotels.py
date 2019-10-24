# Reference and Features Classes
from cl_Data import database as db
from cl_Products import Hotel

##############
# FOR HOTELS #
##############
class Hotelier(object):
    def __init__(self,
                 newName="UNNAMED HOTELIER",
                 newRate=0.00):
        # Create Hotelier ID Number
        self.id = db.appendToList(db.hotelierList,self)
        # Other Hotelier Attributes
        self.name = newName         # Hotelier name.
        self.rate = newRate         # Hotelier baserate.

    def __repr__(self):
        return self.name

class HotelRoom(object):
    def __init__(self,
                 newName="UNNAMED ROOM",
                 newDesc="UNDESCRIBED ROOM.",
                 newCap=1,
                 newRate=0.00):
        # Create Hotel Room ID Number
        self.id = db.appendToList(db.hotelRoomList,self)
        # Create Hotel Room Attributes
        self.name = newName     # Room type name.
        self.desc = newDesc     # Room description.
        self.cap  = newCap      # Room capacity.
        self.rate = newRate     # Room Rate.

    def __repr__(self):
        return self.name

class HotelFeature(object):
    def __init__(self,
                 newName="UNNAMED FEATURE",
                 newDesc="UNDESCRIBED FEATURE.",
                 newRate=0.00):
        # Create Hotel Feature ID Number
        self.id = db.appendToList(db.hotelFeatureList,self)
        # Other Hotel Feature Attributes
        self.name = newName     # Feature name
        self.desc = newDesc     # Feature description
        self.rate = newRate     # Feature cost (if any)

    def __repr__(self):
        return self.name

# Start the fun - import csv, os, and set up directory vars.
import csv, os, sqlite3
from ast import literal_eval as leval

csvDir  = os.getcwd()+"\\csv\\hotels\\"
htlrCSV = csvDir+"hoteliers.csv"
featCSV = csvDir+"hotelFeatures.csv"
roomCSV = csvDir+"hotelRooms.csv"
prodCSV = csvDir+"hotelProducts.csv"

dbCon = sqlite3.connect("./travelAgency.db")
dbCur = dbCon.cursor()

def populateHotelData_CSV(files):
    # Populate Hoteliers
    with open(files[0],newline="") as hFile:
        hr = csv.DictReader(hFile)
        for rowH in hr:
            n = rowH["name"]
            r = rowH["rate"]
            newH = Hotelier(n,r)
            print(newH.name+" added to Hotelier List at #"+str(newH.id)+".")

    # Populate Hotel Features
    with open(files[1],newline="") as fFile:
        fr = csv.DictReader(fFile)
        for rowF in fr:
            n = rowF["name"]
            d = rowF["desc"]
            r = rowF["rate"]
            newF = HotelFeature(n,d,r)
            print(newF.name+" added to Hotel Feature List at #"+str(newF.id)+".")

    # Populate Hotel Room Types
    with open(files[2],newline="") as rFile:
        rr = csv.DictReader(rFile)
        for rowR in rr:
            n = rowR["name"]
            d = rowR["desc"]
            c = rowR["cap"]
            r = rowR["rate"]
            newR = HotelRoom(n,d,c,r)
            print(newR.name+" added to Hotel Room List at #"+str(newR.id)+".")

def populateHotelData_SQL(htlrs,rfeat,rtype):
    # Incoming data should be lists of tuples.
    for hotelier in htlrs:
        #print(hotelier)
        nid = hotelier[0]
        nam = hotelier[1]
        rat = hotelier[2]
        newH = Hotelier(nam,rat)

    for feature in rfeat:
        #print(feature)
        nid = feature[0]
        nam = feature[1]
        des = feature[2]
        rat = feature[3]
        newF = HotelFeature(nam,des,rat)

    for roomtype in rtype:
        #print(roomtype)
        nid = roomtype[0]
        nam = roomtype[1]
        des = roomtype[2]
        cap = roomtype[3]
        rat = roomtype[4]

        newR = HotelRoom(nam,des,cap,rat)

# Create products from Product CSV
def createHotelProduct_CSV(file,obj,comment="Hotel Products"):
    with open(file,newline="") as pFile:
        pr = csv.DictReader(pFile)
        for rowP in pr:
            # Get Name, Desc, and Hotelier object
            n = str(rowP["name"])
            d = str(rowP["desc"])
            h = db.hotelierList[int(rowP["hotelier"])]

            # Get Room Types and Features
            r = rowP["rooms"].split("|")
            f = rowP["features"].split("|")
            rl = []
            fl = []

            # Add Objects to Lists to build Product With
            for rn in r:
                rl.append(db.hotelRoomList[int(rn)])
            for fn in f:
                fl.append(db.hotelFeatureList[int(fn)])

            # Build Product!
            nObj = obj(h,rl,fl)
            nObj.updateName(n)
            nObj.updateDesc(d)
            nObj.calcRoomPrices()

def createHotelProduct_SQL(prods):
    for product in prods:
        #print(product)
        name = product[0]
        desc = product[1]
        hotelier  = db.getObjFromList("hotelierList",product[2])
        rooms_ids = product[3].split("|")
        feats_ids = product[4].split("|")
        rooms = []
        feats = []

        for room in rooms_ids:
            rooms.append(db.getObjFromList("hotelRoomList",int(room)))
        for feature in feats_ids:
            feats.append(db.getObjFromList("hotelFeatureList",int(feature)))

        newHotel = Hotel(hotelier,rooms,feats)
        newHotel.updateName(name)
        newHotel.updateDesc(desc)
        newHotel.calcRoomPrices()

# CSV Style (Depricated)
#populateHotelData_CSV([htlrCSV,featCSV,roomCSV])
#createHotelProduct_CSV(prodCSV,Hotel)

# DB Style (In Use)
dbCur.execute("SELECT * FROM hotel_hoteliers ORDER BY id")
htlrs = dbCur.fetchall()
dbCur.execute("SELECT * FROM hotel_features ORDER BY id")
rfeat = dbCur.fetchall()
dbCur.execute("SELECT * FROM hotel_rooms ORDER BY id")
rtype = dbCur.fetchall()

# Gonna have to try a join here between 'products' and 'prods_hotel'
# to make a more complete statement which will grab the data I need.
'''
dbCur.execute("""
SELECT --products.pid,
       products.name,                   -- 0
       products.desc,                   -- 1
       --prods_hotel.pid,
       --prods_hotel.id,
       prods_hotel.hotelier,            -- 2
       prods_hotel.room_types,          -- 3
       prods_hotel.hotel_features       -- 4
FROM products INNER JOIN prods_hotel
ON products.pid = prods_hotel.pid
ORDER BY prods_hotel.pid
""")
prods = dbCur.fetchall()
'''

populateHotelData_SQL(htlrs,rfeat,rtype)
#createHotelProduct_SQL(prods)

dbCon.close()
