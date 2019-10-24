# Reference and Features Classes
from cl_Data import database as db
from cl_Products import Flight

###############
# FOR FLIGHTS #
###############
class Airport(object):
    def __init__(self,
                 newName="UNNAMED AIRPORT",
                 newDesc="UNDESCRIBED.",
                 newCode="N/A",
                 newCtry=None):
        # Create Airport ID Number
        self.id = db.appendToList(db.airportList,self)
        # Create Airport attributes
        self.name = newName # Airport Name.
        self.desc = newDesc # Airport description.
        self.code = newCode # Airport IATA code. (MEL, JFK, LAX, etc.)
        self.ctry = newCtry # One Airport can only exist in one country.

    def __repr__(self):
        return self.name+" ("+self.code+")"

    def assignCode(self,newCode):
        if(isinstance(newCode,str)):
            if(newCode.len() == 3):
                self.code = newCode.upper()
                print(self.name+"'s IATA airport code is now "+self.code+".")
            else:
                print("Given airport code is not equal to 3 characters in length.")
        else:
            print("Specified text is not a string.")

    def assignCountry(self,newCountry):
        from cl_Country import Country
        if(isinstance(newCountry,Country)):
            self.ctry = newCountry
            print(self.name+" is now located in "+newCountry.name+".")
        else:
            print("Specified object is not a country.")

class Airline(object):
    def __init__(self,
                 newName="UNNAMED AIRLINE",
                 newDesc="UNDESCRIBED AIRLINE.",
                 newCode="--",
                 newCtry="---",
                 tickets=[]):
        # Create Airport ID Number
        self.id = db.appendToList(db.airlineList,self)
        # Create Airline attributes
        self.name  = newName # Airline name.
        self.desc  = newDesc # Airline description/blurb.
        self.code  = newCode # Airline IATA code. (Two characters)
        self.ctry  = newCtry # One Airline can only be based in one country.
        self.tix   = tickets # One airline can offer many types of tickets.
        self.ports = []      # One Airline can offer services in multiple airports.

    def __repr__(self):
        return (self.name+" ("+self.code+")")

    def assignCode(self,newCode):
        if(isinstance(newCode,str)):
            if(newCode.len() == 2):
                self.code = newCode.upper()
                print(self.name+"'s IATA airline code is now "+self.code+".")
            else:
                print("Given airliner code is not equal to 2 characters in length.")
        else:
            print("Specified text is not a string.")

    def assignCountry(self,newCountry):
        from cl_Country import Country
        if(isinstance(newCountry,Country)):
            self.ctry = newCountry
            print(self.name+" is now located in "+newCountry.name+".")
        else:
            print("Specified object is not a Country.")

    def addPort(self,newPort):
        if(isinstance(newPort,Airport)):
            if(newPort in self.ports):
                print("This airport already hosts "+newPort.name+".")
            else:
                self.ports.append(newPort)
                print(newPort.name+" was added to "+self.name+"'s airport list.")
        else:
            print("That is not an Airport object.")

    def removePort(self,oldPort):
        if(isinstance(oldPort,Airport)):
            if(newPort in self.ports):
                self.ports.append(newPort)
                print(newPort.name+" was removed from "+self.name+"'s airport list.")
            else:
                print("This airport doesn't exist in "+self.name+"'s airport list.")
        else:
            print("That is not an Airport object.")

    def addTicket(self,newTicket):
        if(isinstance(newTicket,AirTicket)):
            if(newTicket in self.tix):
                print("That type of ticket is already sold by this airliner.")
            else:
                self.tix.append(newTicket)
                print("New ticket "+str(newTicket.name)+" added to Airliner "+self.name+".")
        else:
            print("New ticket must be an AirTicket object.")

    def removeTicket(self,oldTicket):
        if(isinstance(oldTicket,AirTicket)):
            if(oldTicket not in self.tix):
                print("This type of ticket isn't sold by this airliner.")
            else:
                self.tix.remove(oldTicket)
                print("Ticket "+str(oldTicket.name)+" removed from Airliner"+self.name+".")
        else:
            print("New ticket must be an AirTicket object.")

class AirTicket(object):
    def __init__(self,
                 newName="UNNAMED AIR TICKET",
                 newDesc="UNDESCRIBED AIR TICKET.",
                 newRate=0.00):
        # Create Ticket ID Number
        self.id = db.appendToList(db.airTicketList,self)
        # Create Ticket Attributes
        self.name = newName
        self.desc = newDesc
        self.rate = newRate

    def __repr__(self):
        return self.name+" ($"+str(self.rate)+")"

    def setTicketInfo(self, newInfo):
        try:
            (   flightID,
                ticketClass,
                customerID,
                seatCode    ) = newInfo
            self.flightID       = flightID
            self.ticketClass    = ticketClass
            self.customerID     = customerID
            self.seatCode       = seatCode
        except:
            print("Error extracting ticket info from newInfo tuple.")

# import csv of Flights information
import csv, os, sqlite3

csvDir  = os.getcwd()+"\\csv\\"
flightCSV  = csvDir+"flights\\flights.csv"
dbCon = sqlite3.connect("./travelAgency.db")
dbCur = dbCon.cursor()

def populateFlights_SQL(al,ap,ti):
    from datetime import datetime as dt
    def getCountryFromCode(code):
        # Checks a string against ISO 3166-1 codes in Country objects.
        # Returns a Country object, or None.
        for c in db.countryList:
            if(code == c.codeWord):
                country = c
                return country
        return None

    def splitTickets(tickets):
        # Splits a pipe-separated ticket ID string in into Ticket objects.
        tix   = tickets.split("|")
        tlist = []
        for t in tix:
            try:
                tlist.append(db.getObjFromList("airTicketList",int(t)))
            except ValueError:
                print("Banana! ValueError in splitting tickets!")
                continue
        return tlist

    for ticket in ti:
        name = str(ticket[0])
        desc = str(ticket[1])
        rate = float(ticket[2])

        newTicket = AirTicket(name,desc,rate)

    for airline in al:
        name        = str(airline[0])
        desc        = str(airline[1])
        aircode     = str(airline[2])
        ctrycode    = str(airline[3])
        ticket_ids  = str(airline[4])
        country = getCountryFromCode(ctrycode)
        tickets = splitTickets(ticket_ids)

        newLine = Airline(name,desc,aircode,country,tickets)

    for airport in ap:
        name     = airport[0]
        desc     = airport[1]
        code     = airport[2]
        ctrycode = airport[3]
        country  = getCountryFromCode(ctrycode)

        newPort  = Airport(name,desc,code,country)

    '''
    for flight in fl:
        # Gather data, turn IDs into objects
        name        = str(flight[0])
        airp_dep_id = str(flight[1])
        airp_arr_id = str(flight[2])
        airport_dep = getAirportObj(airp_dep_id)
        airport_arr = getAirportObj(airp_arr_id)
        airline_id  = str(flight[3])
        airline     = getAirlineObj(airline_id)
        flight_code = str(flight[4])

        # Create date/time object.
        dep_date    = str(flight[5])
        dep_time    = str(flight[6])
        arr_date    = str(flight[7])
        arr_time    = str(flight[8])
        timeForm = "%d/%m/%Y %H%M"
        dep_dt      = dt.strptime(dep_date+" "+dep_time,timeForm)
        arr_dt      = dt.strptime(arr_date+" "+arr_time,timeForm)

        ticket      = db.getObjFromList("airTicketList",int(flight[9]))

        newFlight = Flight()
        newFlight.name        = name
        newFlight.airportDep  = airport_dep
        newFlight.airportArr  = airport_arr
        newFlight.airline     = airline
        newFlight.flightCode  = flight_code
        newFlight.depDatetime = dep_dt
        newFlight.arrDatetime = arr_dt
        newFlight.ticket      = ticket
        newFlight.price       = newFlight.ticket.rate
    '''

# SQL data gathering
dbCur.execute("SELECT name, desc, aircode, countrycode, tickets FROM flight_airlines ORDER BY id")
airlines = dbCur.fetchall()
dbCur.execute("SELECT name, desc, code, ctry FROM flight_airports ORDER BY id")
airports = dbCur.fetchall()
dbCur.execute("SELECT name, desc, rate FROM flight_tickets ORDER BY id")
tickets  = dbCur.fetchall()
'''
dbCur.execute("""
SELECT products.name,                -- 0
       prods_flights.airport_depart, -- 1
       prods_flights.airport_arrive, -- 2
       prods_flights.airline,        -- 3
       prods_flights.flight_code,    -- 4
       prods_flights.depart_date,    -- 5
       prods_flights.depart_time,    -- 6
       prods_flights.arrive_date,    -- 7
       prods_flights.arrive_time,    -- 8
       prods_flights.ticket_id       -- 9
FROM products INNER JOIN prods_flights
ON products.pid = prods_flights.pid
ORDER BY prods_flights.pid
""")
flights  = dbCur.fetchall()
'''

#populateFlights_CSV()
populateFlights_SQL(airlines,airports,tickets)

dbCon.close()

'''
    # Andrew's custom CSV Iterator

    for (i,flightLine) in enumerate(flightFile):
        if i == 0: continue   # Skip the header line
        flight_list = flightLine.strip().split(',')
        flight_tuple = tuple( flight_list )
        newFlight = fl()
        newFlight.setFlightInfo( flight_tuple )
        db.appendToList(db.flightList, newFlight)

    print(db.flightList)
'''

'''
# Populate Flight Table
def populateFlights_CSV():
    with open(flightCSV,newline="") as flightFile:
        fReader = csv.DictReader(flightFile)
        for rowF in fReader:
            from datetime import datetime as dt
            # Read rows of Flight Data.
            portDep = rowF["airport_dep"]
            portArr = rowF["airport_arr"]
            airline = rowF["airline"]
            code    = rowF["flightCode"]

            # Date/Time Information to be converted into a datetime object.
            depDate = rowF["departDate"]
            arrDate = rowF["arriveDate"]
            depTime = rowF["departTime"]
            arrTime = rowF["arriveTime"]
            timeForm = "%d/%m/%Y %H%M"

            depDT   = dt.strptime(depDate+" "+depTime,timeForm)
            arrDT   = dt.strptime(arrDate+" "+arrTime,timeForm)

            newFlight = fl()
            newFlight.airportDep  = portDep
            newFlight.airportArr  = portArr
            newFlight.airline     = airline
            newFlight.flightCode  = code
            newFlight.depDatetime = depDT
            newFlight.arrDatetime = arrDT
'''
