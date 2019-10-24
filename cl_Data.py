import sqlite3

dbCon = sqlite3.connect("./travelAgency.db")
dbCur = dbCon.cursor()

# Data Handling/Storage Classes
class Database(object):
    def __init__(self):
        # This is where the data lives. Get you some!
        # People Lists
        self.customerList     = []
        self.staffList        = []
        # Transactions Lists
        self.transacList      = []
        self.orderList        = []
        self.salesList        = []
        self.docketList       = []
        # Product Lists
        self.prodList         = []
        self.hotelList        = []
        self.flightList       = []
        self.vehicleList      = []
        self.actList          = []
        self.insList          = []
        # Country Lists
        self.countryList      = []
        self.locationList     = []
        # Feature Lists for...
        #   HOTELS
        self.hotelierList     = []
        self.hotelRoomList    = []
        self.hotelFeatureList = []
        #   FLIGHTS
        self.airportList      = []
        self.airlineList      = []
        self.airTicketList    = []
        #   TRANSPORT
        self.transpoList      = []
        self.transporterList  = []
        self.carsList         = []
        self.bikesList        = []
        self.driveList        = []
        self.gearList         = []
        #   ACTIVITIES
        self.actProvidersList = []
        self.actTypesList     = []
        #   INSURANCE
        self.insProvidersList = []
        self.insCoverList     = []

        print("Database is alive!")

        # Other DB control stuff. These are encapsulated.
        # Because you shouldn't be able to change what sort of
        # data object goes into which list normally on the fly.
        self._defaultAttrs   = ["tid","pid","id","name","fname","lname","desc"]
        # Yes, I know they're hard coded. They're attributes that many objects have/share.
        self._listNames      = []
        self._allLists       = []
        self._allowedObjs    = []
        self._attributes     = []
        self._associatedFile = []
        # For serialising/de-serialising
        self._serials          = []
        self._serialAttributes = []
        self._sqlTables        = []
        self.populateDBControlOpts()

    # Luca's Database Functions
    ###########################
    # These getter attributes get a soft copy of the encapsulated lists.
    # These don't link to or modify the originals when called.
    def getDefaultAttributes(self): return self._defaultAttrs.copy()
    def getListNames(self):         return self._listNames.copy()
    def getAllLists(self):          return self._allLists.copy()
    def getAllowedObjs(self):       return self._allowedObjs.copy()
    def getAssociatedFile(self):    return self._associatedFile.copy()
    def getAttributes(self):        return self._attributes.copy()
    def getSerials(self):           return self._serials.copy()
    def getSerialAttrs(self):       return self._serialAttributes.copy()
    def getSQLTables(self):         return self._sqlTables.copy()

    def getList(self,l=""):
        # Pass a text argument of which list to use, then return that list.
        # If list doesn't exist, print a warning and return false, otherwise return list.
        try:
            g = getattr(self,l)
            if(type(g).__name__ == "list"):
                # Attribute in obj is a list.
                return g
            else:
                # Attribute in obj is not a list!
                return False
        except AttributeError:
            # Attribute in database doesn't exist.
            print("List not found in database.")
            return False

    def getObjFromList(self,l="",ind=0):
        # Check a list, and get an object from the specified index.
        # Does similar to the above.
        # Returns an object from a list (0th object on index error)
        # or a bool False if no such list exists in the db.
        li = self.getList(l)

        if(li != False):
            # List found, go looking for object now.
            try:
                # Hopefully the given index is right, right?
                return li[ind]
            except IndexError:
                try:
                    print("IndexError encountered. Defaulting to first object in list.")
                    print("Tried: "+l+", "+str(ind))
                    return li[0]
                except IndexError:
                    print("Second IndexError encountered. Aw hell! Return poop.")
                    return False
        else:
            print("List not found in database.")
            return False

    def populateDBControlOpts(self,file="./csv/databaseObjectTypes.csv"):
        # Grabs all the lists' names, and names the object types allowed in them.
        # The zeroth column of the CSV is 'name' - which has the lists' user-friendly names.
        # The first column of the CSV is 'list' - which has the lists' dev-friendly names.
        # The second column is 'objs' - which has strings separated by |'s
        # for allowed object types in that list, found by the type() function.

        def appendToListNames(n):
            # Setter function for user-friendly list of names of lists.
            self._listNames.append(n)
        def appendToAllLists(l):
            # Setter function for list of list names.
            # Index sensitive, intended to run in tandem with below function.
            self._allLists.append(l)
        def appendToAllowedObjs(o):
            # Setter function for allowed types in lists.
            # Index sensitive, intended to run in tandem with above function.
            self._allowedObjs.append(o)
        def appendToAssociatedFile(f):
            # Setter function for files where types are.
            # Index sensitive, running in tandem with the above.
            self._associatedFile.append(f)
        def appendToAttributes(a):
            # Setter function for attribute names.
            # Index sensitive, running in tandem with the above.
            self._attributes.append(a)
        def appendToSerials(s):
            # Setter function, for serialised attributes.
            # Index sensitive, running in tandem with the above.
            self._serials.append(s)
        def appendToSerialAttrs(sa):
            # Setter function, for attribute to serialise objects by.
            # Index sensitive, running in tandem with the above.
            self._serialAttributes.append(sa)
        def appendToSQLTables(sq):
            # Setter function, for names of SQL tables these key to.
            # Index sensitive, running in tandem with the above.
            self._sqlTables.append(sq)

        dbCur.execute("""
        SELECT name,        -- 0
               list,        -- 1
               objs,        -- 2
               file,        -- 3
               attr,        -- 4
               serials,     -- 5
               serial_attr, -- 6
               sql_table    -- 7
        FROM metadata
        ORDER BY id
        """)
        metadata_list = dbCur.fetchall()

        for meta in metadata_list:
            na = str(meta[0])
            li = str(meta[1])
            ob = str(meta[2])
            fi = str(meta[3])
            at = meta[4].split("|")
            se = meta[5].split("|")
            sa = str(meta[6])
            sq = str(meta[7])

            appendToListNames(na)
            appendToAllLists(li)
            appendToAllowedObjs(ob)
            appendToAssociatedFile(fi)
            appendToAttributes(at)
            appendToSerials(se)
            appendToSerialAttrs(sa)
            appendToSQLTables(sq)

        '''
        import csv
        with open(file,newline="") as dbFile:
            reader = csv.DictReader(dbFile)
            for r in reader:
                na = str(r["name"])
                li = str(r["list"])
                ob = str(r["objs"])
                fi = str(r["file"])
                at = r["attr"].split("|")
                se = r["serials"].split("|")
                sa = str(r["serial_attr"])
                sq = str(r["sql_table"])

                appendToListNames(na)
                appendToAllLists(li)
                appendToAllowedObjs(ob)
                appendToAssociatedFile(fi)
                appendToAttributes(at)
                appendToSerials(se)
                appendToSerialAttrs(sa)
                appendToSQLTables(sq)
        '''

    def appendToList(self,l,o):
        # Appends a newly created object to the 'database' of lists
        # and returns the new ID number

        # l = list within Database to append to
        # o = object/instance to append to list
        # Returns the ID assigned to the object.
        if(isinstance(l,list)):
            l.append(o)
            i = l.index(o)
            return i
        else:
            print("Specified list does not exist in database.")

    def joinLists(self,l1=[],l2=[]):
        # Join two .copy()'d lists together with .extend()
        # Returns an extended list object. Lobject?
        list1 = l1.copy()
        list2 = l2.copy()
        try:
            return list1.extend(list2)
        except:
            pass

    def serialiseObjs(obj):
        # Serialise the objects inside of lists in an object.
        pass

    # Andrew's Search Functions
    ###########################
    def searchFlightsOneWay(departApCode, arriveApCode, depDate):
        matchFlights = []
        for flight in self.flights:
            if (flight.airport_dep == departApCode and
                flight.airport_arr == arriveApCode and
                flight.departDate == depDate):
                matchFlights.append( flight )
        return matchFlights

    def searchFlightsReturn(ApCode_A, ApCode_B, depDate, returnDate):
        matchFlights_there = []
        for flight in self.flights:
            if (flight.airport_dep == ApCode_A and
                flight.airport_arr == ApCode_B and
                flight.departDate == depDate):
                matchFlights_there.append( flight )
        matchFlights_back = []
        for flight in self.flights:
            if (flight.airport_dep == ApCode_B and
                flight.airport_arr == ApCode_A and
                flight.departDate == returnDate):
                matchFlights_back.append( flight )
        return (matchFlights_there, matchFlights_back)

    def searchActivitiesByPriceLocation(maxPrice, location):
        acts_to_return = []
        for act in self.actTypesList:
            if act.rate <= maxPrice and act.location == location:
                acts_to_return.append(act)
        return acts_to_return

    def searchActivitiesByLocation(location):
        acts_to_return = []
        for act in self.actTypesList:
            if act.location == location:
                acts_to_return.append(act)
        return acts_to_return

    def searchVehiclesByPriceLocation(maxPrice, location):
        vehicles_to_return = []
        for vehicle in self.carsList:
            if vehicle.rate <= maxPrice and vehicle.location == location:
                vehicles_to_return.append( vehicle )
        return vehicles_to_return

    def searchVehiclesByLocation(location):
        vehicles_to_return = []
        for vehicle in self.carsList:
            if vehicle.location == location:
                vehicles_to_return.append( vehicle )
        return vehicles_to_return

    def searchHotelsByLocation(location):
        hotels_to_return = []
        for hotel in self.hotelsList:
            if hotel.location == location:
                hotels_to_return.append( hotel )
        return hotels_to_return


    def searchHotelsByPriceLocation(maxPrice, location):
        hotels_to_return = []
        for hotel in self.hotelsList:
            if hotel.rate <= maxPrice and hotel.location == location:
                hotels_to_return.append( hotel )
        return hotels_to_return

    def searchHotelRoomsByLocation(location):
        rooms_to_return = []
        for hotel in self.hotelsList:
            if hotel.location == location:
                for room in hotel.roomTypes:
                    rooms_to_return.append( room )
        return rooms_to_return

    def searchHotelRoomsByPriceLocation(maxPrice, location):
        rooms_to_return = []
        for hotel in self.hotelsList:
            if hotel.location == location:
                for room in hotel.roomTypes:
                    if room.rate <= maxPrice:
                        rooms_to_return.append( room )
        return rooms_to_return

    def searchInsuranceByPrice( maxPrice ):
        ins_to_return = []
        for ins in self.insList:
            if ins.calcInsurancePrice() <= maxPrice:
                ins_to_return.append(ins)
        return ins_to_return

class DataLoader():
    pass

class DataSaver():
    pass

database = Database()

dbCon.close()