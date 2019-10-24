# Product Object Classes
from cl_Data import database as db
from datetime import datetime as dt

class Product(object):
    def __init__(self):
        # Create Product ID Number
        self.pid = db.appendToList(db.prodList,self)
        # Create Product Essentials
        self.name       = ""
        self.desc       = ""
        self.price      = -0.00
        self.startDate  = dt.now()
        self.endDate    = dt.now()
        self.days       = 0
        self.location   = None

    def __repr__(self):
        return self.name

    def updateName(self,newName,p=False):
        if(isinstance(newName,str)):
            self.name = newName
            if(p == True):
                print("Name changed successfully to '"+newName+"'.")
        else:
            print("New name must be a string.")

    def updateDesc(self,newDesc,p=False):
        if(isinstance(newDesc,str)):
            self.desc = newDesc
            if(p == True):
                print("Description updated successfully.")
        else:
            print("New description must be a string.")

    '''
    def updateDuration(self,newDur):
        if(isinstance(newDur,int)):
           oldDur = self.days
           self.days = newDur
           print("Duration of product changed from "+str(oldDur)+
                 " to "+str(self.days)+".")
        else:
            print("New duration must be an integer.")
    '''

    def updateDate(self,newDate):
        pass

    # Date + Duration = End Date

    def getEndDate(self):
        pass

    def updateLocation(self,newLoc):
        from cl_Country import Location
        if(isinstance(newLoc,Location)):
            oldLoc = self.location
            self.location = newLoc
            print("Location of product changed from "+str(oldLoc.name)+
                  " to "+str(self.location.name)+".")
        else:
            print("New location must be a Location object.")

    def removeLocation(self):
        self.location = None
        print(str(self.name)+" is no longer in a location.")

    def updatePrice(self,newPrice):
        if(isinstance(newPrice,(int,float))):
            oldPrice = self.price
            self.price = newPrice
            print("Price updated successfully. Was "
                  +str(oldPrice)+", now "+str(self.price))
        else:
            print("New price must be a number: whole or decimal.")

class Hotel(Product):
    def __init__(self,hot=None,rty=[],htf=[]):
        Product.__init__(self)
        # Create Hotel ID
        self.id = db.appendToList(db.hotelList,self)
        # Create Hotel Details
        self.hotelier       = hot   # One Hotelier may operate many hotels.
        self.roomTypes      = rty   # One hotel may have many room types.
        self.roomPrices     = []    # Room prices run parallel here.
        self.chosenRoom     = 0     # Room chosen to stay in. -1 = no choice.
        self.hotelFeatures  = htf   # One hotel may have many features.

    def assignHotelier(self,newHotelier):
        from cl_Hotels import Hotelier
        if(isinstance(newHotelier,Hotelier)):
            self.hotelier = newHotelier
            print(self.name+"'s Hotelier/Operator is now "+newHotelier.name)
        else:
            print("Specified object is not a Hotelier.")

    def addToHotel(self,newObject):
        # Add hotel features or room types.
        from cl_Hotels import HotelFeature
        from cl_Hotels import HotelRoom
        if(isinstance(newObject,HotelFeature)):
            if(newObject in self.hotelFeatures):
                # That feature already exists here.
                print("That feature is already a part of this hotel.")
            else:
                # Feature doesn't exist, add.
                self.hotelFeatures.append(newObject)
                print(newObject.name+" has been added to this hotel's features.")
        elif(isinstance(newObject,HotelRoom)):
            if(newObject in self.roomTypes):
                # That room is already on offer
                print("That room type is already on offer in this hotel.")
            else:
                # Room isn't on offer here. Add.
                self.roomTypes.append(newObject)
                print(newObject.name+" has been added to this hotel's room types.")
        else:
            print("Specified object is not a Hotel Feature or Hotel Room.")

    def remFromHotel(self,oldObject):
        # Remove hotel features or room types.
        from cl_Hotels import HotelFeature
        from cl_Hotels import HotelRoom
        if(isinstance(newFeat,HotelFeature)):
            if(oldObject in self.hotelFeatures):
                # Feature is in the list. Remove.
                self.hotelFeatures.remove(oldObject)
                print(oldObject.name+" has been removed from the hotel's features.")
            else:
                print("That feature is not a part of this hotel.")
        elif(isinstance(oldObject,HotelRoom)):
            if(oldObject in self.roomTypes):
                # Room is in the list. Remove.
                self.roomTypes.remove(oldObject)
                print(oldObject.name+" has been removed from this hotel's rooms.")
            else:
                # Room isn't here.
                print("That room is not available at this hotel.")
        else:
            print("Specified object is not a Hotel Feature or Hotel Room.")

    def calcRoomPrices(self,p=False):
        # Calculate room costs based on Hotelier, Room Type, and Hotel Features.
        # Does this for all room types currently in the Hotel product.
        if(self.hotelier != None):
            if(len(self.roomTypes) > 0):
                # Clear current room prices to make new ones.
                self.roomPrices = []
                print("Hotelier Rate: "+str(self.hotelier.rate))

                # And figure out one-time feature cost
                featureCost = 0.00
                if(len(self.hotelFeatures) > 0):
                    for hf in self.hotelFeatures:
                        featureCost += float(hf.rate)
                    print("Feature Cost: "+str(featureCost)
                          + str(len(self.hotelFeatures)))
                else:
                    print("No features.")

                # Make Room Prices, add hotelier rate, then add feature cost.
                for rt in self.roomTypes:
                    # Figure out faked Logarithmic Cap Multiplier. 1=1, 2=1.25, 3=1.50...
                    cap = float(rt.cap)
                    capBase = 1.0
                    capMult = 0.125
                    capMod = capBase+(cap*capMult)

                    price = (float(rt.rate) + float(self.hotelier.rate)
                             + featureCost + len(self.hotelFeatures))*float(capMod)
                    price = float("{0:.2f}".format(price))
                    print("Room Price for "+str(rt.name)+": "
                          +str(price)+" | Capacity: "+str(rt.cap))
                    self.roomPrices.append(price)

                    self.price = self.roomPrices[self.chosenRoom]

                if(p == True):
                    print(self.roomTypes)
                    print(self.roomPrices)
            else:
                print("Hotel needs at least 1 room type to calculate room prices.")
        else:
            print("Hotelier needed to do room price calculations.")

class Flight(Product):
    def __init__(self):
        Product.__init__(self)
        # Create Flight ID
        self.id = db.appendToList(db.flightList,self)
        # Create Flight Details
        self.airportDep     = None
        self.airportArr     = None
        self.airline        = None
        self.flightCode     = None
        self.depDatetime    = None
        self.arrDatetime    = None
        self.ticket         = None

    def __repr__(self):
        return self.name
    
    def renameSelf(self):
        self.name = str(self.airportDep)+" to "+str(self.airportArr)+" by "+str(self.airline)+" ("+str(self.flightCode)+") - "+str(depDatetime.date())+":"+str(depDatetime.time())+" / "+str(arrDatetime.date())+":"+str(arrDatetime.time())

    '''
    def setFlightInfo(self, newInfo):
        try:
            (id,
             airportDep,
             airportArr,
             airline,
             arriveDate,
             arriveTime,
             flightCode) = newInfo

            self.id           = newInfo[0]
            self.airportDep   = airportDep
            self.airportArr   = airportArr
            self.airline      = airline
            self.departDate     = departDate
            self.departTime     = departTime
            self.arriveDate     = arriveDate
            self.arriveTime     = arriveTime
            self.flightCode     = flightCode
        except:
            print("Error extracting flight info from newInfo tuple.")
    '''

class Vehicle(Product):
    def __init__(self,t=None,m=None,d=None,g=None):
        Product.__init__(self)
        # Create Vehicle ID
        self.id = db.appendToList(db.vehicleList,self)
        # Create vehicle attributes.
        self.transporter = t # Transport Company
        self.model       = m # Car/Bike Type
        self.drive       = d # Drive Type
        self.gears       = g # Gears Type

    def calcVehiclePrice(self,p=False):
        if(self.transporter != None):
            tranRate = self.transporter.baseRate
        else:
            print("No transporter company has been selected for this vehicle.")
            print("Using base rate of 0.")
            tranRate = 0
        vehicRate = self.model.rate
        self.price = tranRate + vehicRate
        if(p == True):
            print("Price for "+self.name+" from "+self.transporter.name
                  +" changed to: "+str(self.price)+" per day")

class Activity(Product):
    def __init__(self,prov=None,acts=None):
        Product.__init__(self)
        # Create Activity ID
        self.id = db.appendToList(db.actList,self)
        # Create activity attributes
        self.actProvider    = prov
        self.actType        = acts

        self.price = self.actProvider.rate + self.actType.rate

class Insurance(Product):
    def __init__(self,prov=None,covs=[]):
        Product.__init__(self)
        # Create Insurance ID
        self.id = db.appendToList(db.insList,self)
        # Create insurance Attributes
        self.insProvider = prov
        self.insCover    = covs

    def changeProvider(self,prov,p=False):
        from cl_Insurance import InsuranceProvider as ip
        if(isinstance(prov,ip)):
            self.insProvider = prov
            if(p == True):
                print("This Insurance Product's provider is now "
                      +str(self.insprovider.name)+".")
        else:
            print("New provider must be an insurance provider object.")

    def addCover(self,cov,p=False):
        from cl_Insurance import InsuranceCover as ic
        if(isinstance(cov,ic)):
            if(cov in self.insCover):
                # Cover already in list. Skipping.
                if(p == True):
                    print("That insurance cover is already in this product.")
            else:
                # Cover not in list. Add and recalc price.
                self.insCover.append(cov)
                self.calcInsurancePrice()
                if(p == True):
                    print("Insurance cover added successfully.")
        else:
            # Item is not cover.
            print("New cover must be an insurance cover object.")

    def remCover(self,cov,p=False):
        from cl_Insurance import InsuranceCover as ic
        if(isinstance(cov,ic)):
            # Check if item to remove is in list.
            if(cov in self.insCover):
                # Item is in list. Remove and recalc price.
                self.insCover.remove(cov)
                self.calcInsurancePrice()
                if(p == True):
                    print("Insurance cover removed successfully.")
            else:
                # Item is not in list. Skipping.
                print("Given insurance cover item not in list.")
        else:
            # Item is not an insurance cover.
            print("Cover to remove must be an insurance cover object.")

    def calcInsurancePrice(self):
        # Calculate price based off of provider and cover items in Product.
        if(self.insProvider == None):
            print("Can't calculate price without a provider.")
        else:
            # Start with base multiplier. Add to it then multiply by base rate.
            if(len(self.insCover) > 0):
                multi = 1
                for c in self.insCover:
                    multi += c.rate
                self.price = self.insProvider.rate*multi
            else:
                print("No cover areas in this product. Using base rate only.")
                self.price = self.insProvider.rate

            print("The price of "+str(self.name)+" is now "+str(self.price)+" per day.")
