# Product Building Script
# Meant to decentralise the way products are built currently, and allow for products to be introduced into the system out of strict order.

import sqlite3
from cl_Data import database as db
dbCon = sqlite3.connect("./travelAgency.db")
dbCur = dbCon.cursor()

# First, get max number of product ids.
dbCur.execute("SELECT max(pid) FROM products")
pid_tup = dbCur.fetchone()

# Because I'll be using range() to create the For Loop,
# I have to add one to it, or it won't find the last iterable.
# (This is according to something on the function online)
pids_to_iterate = pid_tup[0]+1

print("cl_buildProds: Running!")
for p in range(pids_to_iterate):
    # First, try hotels
    print("Iterating PID = "+str(p))
    dbCur.execute("SELECT * FROM prods_hotel WHERE pid = ?",(p,))
    result = dbCur.fetchall()
    if(result != []):
        print("Hotel found at "+str(p)+"! Building product.")
        dbCur.execute("""
            SELECT products.name,               -- 0
                   products.desc,               -- 1
                   prods_hotel.hotelier,        -- 2
                   prods_hotel.room_types,      -- 3
                   prods_hotel.hotel_features,  -- 4
                   prods_hotel.location         -- 5
            FROM products INNER JOIN prods_hotel
            ON products.pid = prods_hotel.pid
            WHERE products.pid = ?
        """,(p,))
        product = dbCur.fetchone()
        
        # Build Hotel Product
        name = str(product[0])
        desc = str(product[1])
        hotelier  = db.getObjFromList("hotelierList",product[2])
        rooms_ids = product[3].split("|")
        feats_ids = product[4].split("|")
        loc_id    = int(product[5])
        rooms = []
        feats = []
        
        for room in rooms_ids:
            rooms.append(db.getObjFromList("hotelRoomList",int(room)))
        for feature in feats_ids:
            feats.append(db.getObjFromList("hotelFeatureList",int(feature)))
        
        from cl_Products import Hotel
        newHotel = Hotel(hotelier,rooms,feats)
        newHotel.updateName(name)
        newHotel.updateDesc(desc)
        newHotel.location = db.getObjFromList("locationList",loc_id)
        newHotel.calcRoomPrices()
        
        continue
#    else:
#        print("Nothing returned for PID: "+str(p)+" in Hotels.")

    # Then, try insurance.
    dbCur.execute("SELECT * FROM prods_insurance WHERE pid = ?",(p,))
    result = dbCur.fetchall()
    if(result != []):
        print("Insurance found at "+str(p)+"! Building product.")
        dbCur.execute("""
            SELECT products.name,                   -- 0
                   products.desc,                   -- 1
                   prods_insurance.ins_provider,    -- 2
                   prods_insurance.ins_cover        -- 3
            FROM products INNER JOIN prods_insurance
            ON products.pid = prods_insurance.pid
            WHERE products.pid = ?
        """,(p,))
        product = dbCur.fetchone()
        
        # Build Insurance Product
        name = str(product[0])
        desc = str(product[1])
        provider = db.getObjFromList("insProvidersList",int(product[2]))
        if(product[3] != "None"):
            cover_ids = product[3].split("|")
        else: cover_ids = []
        covers = []
        
        for option in cover_ids:
            covers.append(db.getObjFromList("insCoverList",int(option)))
        
        from cl_Products import Insurance
        newInsurance = Insurance(provider,covers)
        newInsurance.updateName(name)
        newInsurance.updateDesc(desc)
        newInsurance.calcInsurancePrice()
        
        continue
#    else:
#        print("Nothing returned for PID: "+str(p)+" in Insurance.")

    # Then, try transportation.
    dbCur.execute("SELECT * FROM prods_vehicles WHERE pid = ?",(p,))
    result = dbCur.fetchall()
    if(result != []):
        print("Transport found at "+str(p)+"! Building product.")
        dbCur.execute("""
            SELECT products.name,               -- 0
                   products.desc,               -- 1
                   prods_vehicles.transporter,  -- 2
                   prods_vehicles.vtype,        -- 3
                   prods_vehicles.model,        -- 4
                   prods_vehicles.drive,        -- 5
                   prods_vehicles.gears         -- 6
            FROM products INNER JOIN prods_vehicles
            ON products.pid = prods_vehicles.pid
            WHERE products.pid = ?
        """,(p,))
        product = dbCur.fetchone()
        
        # Build Transport/Vehicle Product
        name  = str(product[0])
        desc  = str(product[1])
        trans = db.getObjFromList("transporterList",int(product[2]))
        vtype = str(product[3])
        mod   = int(product[4])
        drive = db.getObjFromList("driveList",int(product[5]))
        gears = db.getObjFromList("gearList",int(product[6]))
        
        if(vtype.lower() == "car"):
            model = db.getObjFromList("carsList",mod)
        elif(vtype.lower() == "bike"):
            model = db.getObjFromList("bikesList",mod)
        else:
            print("Either 'car' or 'bike' expected from vtype. Skipping vehicle.")
            continue
        
        from cl_Products import Vehicle
        newVehicle = Vehicle(trans,model,drive,gears)
        newVehicle.updateName(name)
        newVehicle.updateDesc(desc)
        newVehicle.calcVehiclePrice(True)
        
        continue
#    else:
#        print("Nothing returned for PID: "+str(p)+" in Transport/Vehicles.")

    # Then, try flights.
    dbCur.execute("SELECT * FROM prods_flights WHERE pid = ?",(p,))
    result = dbCur.fetchall()
    if(result != []):
        print("Flight found at "+str(p)+"! Building product.")
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
            WHERE products.pid = ?
        """,(p,))
        product = dbCur.fetchone()
        
        # Two mini-functions are needed for this one.
        def getAirportObj(airport_code):
            # Checks the database for an Airport which matches the code given.
            # Returns an airport object, or None
            for airport in db.airportList:
                try:
                    if(airport_code == airport.code):
                        return airport
                except ValueError:
                    print("Banana! ValueError in getting an Airport Object!")
                    continue
            return None

        def getAirlineObj(airline_code):
            for airline in db.airlineList:
                try:
                    if(airline_code.upper() == airline.code.upper()):
                        return airline
                except ValueError:
                    print("Banana! ValueError in getting an Airline Object!")
                    continue
            return None
        
        # Build Flight Product.
        name        = str(product[0])
        airp_dep_id = str(product[1])
        airp_arr_id = str(product[2])
        airport_dep = getAirportObj(airp_dep_id)
        airport_arr = getAirportObj(airp_arr_id)
        airline_id  = str(product[3])
        airline     = getAirlineObj(airline_id)
        flight_code = str(product[4])
        
        timeForm    = "%d/%m/%Y %H%M"
        dep_date    = str(product[5])
        dep_time    = str(product[6])
        arr_date    = str(product[7])
        arr_time    = str(product[8])
        from datetime import datetime as dt
        dep_dt      = dt.strptime(dep_date+" "+dep_time,timeForm)
        arr_dt      = dt.strptime(arr_date+" "+arr_time,timeForm)
        ticket      = db.getObjFromList("airTicketList",int(product[9]))
        
        from cl_Products import Flight
        newFlight = Flight()
        newFlight.updateName(name)
        newFlight.airportDep  = airport_dep
        newFlight.airportArr  = airport_arr
        newFlight.airline     = airline
        newFlight.flightCode  = flight_code
        newFlight.depDatetime = dep_dt
        newFlight.arrDatetime = arr_dt
        newFlight.ticket      = ticket
        newFlight.price       = newFlight.ticket.rate
        
        continue
#    else:
#        print("Nothing returned for PID: "+str(p)+" in Flights.")

    # Then, try activities.
    dbCur.execute("SELECT * FROM prods_activities WHERE pid = ?",(p,))
    result = dbCur.fetchall()
    if(result != []):
        print("Activity found at "+str(p)+"! Building product.")
        dbCur.execute("""
            SELECT products.name,                   -- 0
                   products.desc,                   -- 1
                   prods_activities.act_provider,   -- 2
                   prods_activities.act_type        -- 3
            FROM products INNER JOIN prods_activities
            ON products.pid = prods_activities.pid
            WHERE products.pid = ?
        """,(p,))
        product = dbCur.fetchone()
        
        name     = str(product[0])
        desc     = str(product[1])
        
        provider = db.getObjFromList("actProvidersList",int(product[2]))
        activity = db.getObjFromList("actTypesList",int(product[3]))
        
        from cl_Products import Activity
        newActivity = Activity(provider,activity)
        newActivity.updateName(name)
        newActivity.updateDesc(desc)
        
        continue
#    else:
#        print("Nothing returned for PID: "+str(p)+" in Activities.")
    
    # Finally, if that all comes up empty...
    print("Oh dear! No corresponding product was found for PID = "+str(p))
    # Maybe make an error loggy thing here later ... ?
print("cl_buildProds: Finishing!")

dbCon.commit()
dbCon.close()