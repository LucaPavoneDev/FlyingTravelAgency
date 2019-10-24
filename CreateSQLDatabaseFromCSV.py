# This program should only be run once.
# Because this creates a database from all the CSV crap.
# I hope it'll actually do what I think it does.
# But weh. I'll salt this function once I'm done with it.
import sqlite3
import csv

dbCon = sqlite3.connect("./travelAgency.db")
dbCur = dbCon.cursor()

# Drop everything in the pre-existing DB and overwrite it.
# Go nuclear or go home, I says!
print("Deleting all existing tables for replacement.")
dbCur.executescript('''
-- Database Metadata
DROP TABLE IF EXISTS metadata;
-- Business Data
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS locations;
-- Products Data
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS prods_hotel;
DROP TABLE IF EXISTS prods_flights;
DROP TABLE IF EXISTS prods_vehicles;
DROP TABLE IF EXISTS prods_activities;
DROP TABLE IF EXISTS prods_insurance;
-- Product Feature Data
-- Hotels
DROP TABLE IF EXISTS hotel_rooms;
DROP TABLE IF EXISTS hotel_features;
DROP TABLE IF EXISTS hotel_hoteliers;
-- Flights
DROP TABLE IF EXISTS flight_airlines;
DROP TABLE IF EXISTS flight_airports;
DROP TABLE IF EXISTS flight_tickets;
-- Vehicles
DROP TABLE IF EXISTS vehicle_transporters;
DROP TABLE IF EXISTS vehicle_depots;
DROP TABLE IF EXISTS vehicle_cars;
DROP TABLE IF EXISTS vehicle_bikes;
DROP TABLE IF EXISTS vehicle_drives;
DROP TABLE IF EXISTS vehicle_gears;
-- Insurance
DROP TABLE IF EXISTS insurance_covers;
DROP TABLE IF EXISTS insurance_providers;
-- Activities
DROP TABLE IF EXISTS activity_type;
DROP TABLE IF EXISTS activity_provider;
''')

# Database Metadata
###################
metadata_file = "./csv/databaseObjectTypes.csv"
metadata_numb = 0
print("Reloading Metadata from '"+metadata_file+"'.")
dbCur.execute('''
CREATE TABLE metadata (id INTEGER PRIMARY KEY NOT NULL,
                       name,list,file,objs,attr,
                       serials,serial_attr,sql_table)''')
with open(metadata_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        na = str(r["name"])
        li = str(r["list"])
        fi = str(r["file"])
        ob = str(r["objs"])
        at = str(r["attr"])
        se = str(r["serials"])
        sa = str(r["serial_attr"])
        sq = str(r["sql_table"])

        metadata = (metadata_numb,na,li,fi,ob,at,se,sa,sq)
        dbCur.execute("""INSERT INTO metadata (id,name,list,file,objs,attr,
                                               serials,serial_attr,sql_table)
                         VALUES (?,?,?,?,?,?,?,?,?)""",metadata)
        metadata_numb += 1

# Customers
###########
customers_file = "./csv/customers.csv"
customers_numb = 0
print("Reloading Customers from '"+customers_file+"'.")
dbCur.execute('''
CREATE TABLE customers (id INTEGER PRIMARY KEY NOT NULL,
                        fname,lname,desc,email,
                        homePhone,mobilePhone,
                        zipcode,state,city,streetName,
                        streetNumber,unitNumber)''')
with open(customers_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        fn  = str(r["fname"])
        ln  = str(r["lname"])
        em  = str(r["email"])
        hp  = str(r["homePhone"])
        mp  = str(r["mobilePhone"])
        zi  = str(r["zipcode"])
        st  = str(r["state"])
        ci  = str(r["city"])
        sna = str(r["streetName"])
        snu = str(r["streetNumber"])
        un  = str(r["unitNumber"])
        de  = str(r["desc"])

        customer = (customers_numb,fn,ln,em,hp,mp,zi,st,ci,sna,snu,un,de)
        dbCur.execute("""INSERT INTO customers (id,fname,lname,email,homePhone,
                                                mobilePhone,zipcode,state,
                                                city,streetName,streetNumber,unitNumber,desc)
                         VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",customer)
        customers_numb += 1

# Staff
#######
staff_file = "./csv/staff.csv"
staff_numb = 0
print("Reloading Staff from '"+staff_file+"'.")
dbCur.execute('''
CREATE TABLE staff (id INTEGER PRIMARY KEY NOT NULL,
                    fname,lname,desc,email,
                    homePhone,mobilePhone,
                    zipcode,state,city,streetName, 
                    streetNumber,unitNumber)''')
with open(staff_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        fn = str(r["fname"])
        ln = str(r["lname"])
        em = str(r["email"])
        hp = str(r["homePhone"])
        mp = str(r["mobilePhone"])
        de = str(r["desc"])

        staff = (staff_numb,fn,ln,em,hp,mp,de)
        dbCur.execute("""INSERT INTO staff
                         (id,fname,lname,email,homePhone,mobilePhone,desc)
                         VALUES (?,?,?,?,?,?,?)""",staff)
        staff_numb += 1

# Transactions
##############
transac_file = "./csv/transactions.csv"
transac_numb = 0
print("Reloading Transactions from '"+transac_file+"'.")
dbCur.execute('''
CREATE TABLE transactions (tid INTEGER PRIMARY KEY NOT NULL,
                           datetime_year,datetime_month,datetime_day,
                           customer_ids,staff_ids,prod_ids,
                           bill,duedate_year,duedate_month,duedate_day,
                           amount_paid,paid,notes)''')
with open(transac_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        dt_y = int(r["datetime_year"])
        dt_m = int(r["datetime_month"])
        dt_d = int(r["datetime_day"])
        cust = str(r["customer_ids"])
        staf = str(r["staff_ids"])
        prod = str(r["prod_ids"])
        bill = str(r["bill"])

        # These rows may be empty. Use placeholders if empty.
        # Happens when the transaction is _not_ a bill.
        try: dd_y = int(r["duedate_year"])
        except: dd_y = 1970
        try: dd_m = int(r["duedate_month"])
        except: dd_m = 1
        try: dd_d = int(r["duedate_day"])
        except: dd_d = 1
        try: ampa = float(r["amount_paid"])
        except: ampa = 0.0

        paid = str(r["paid"])
        note = str(r["notes"])

        transaction = (transac_numb,
                       dt_y,dt_m,dt_d,
                       cust,staf,prod,
                       bill,dd_y,dd_m,dd_d,
                       ampa,paid,note)
        dbCur.execute("""INSERT INTO transactions (tid,datetime_year,datetime_month,datetime_day,
                                                   customer_ids,staff_ids,prod_ids,bill,
                                                   duedate_year,duedate_month,duedate_day,
                                                   amount_paid,paid,notes)
                         VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",transaction)
        transac_numb += 1

# Countries
###########
country_file = "./csv/countries.csv"
country_numb = 0
print("Reloading Countries from '"+country_file+"'.")
dbCur.execute('''
CREATE TABLE countries (id INTEGER PRIMARY KEY NOT NULL,
                        name,codeword,codenum)''')
with open(country_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        na = str(r["name"])
        cw = str(r["codeword"])
        cn = int(r["codenum"])

        country = (country_numb,na,cw,cn)
        dbCur.execute("INSERT INTO countries (id,name,codeword,codenum) VALUES (?,?,?,?)",country)
        country_numb += 1

# Locations
###########
location_file = "./csv/locations.csv"
location_numb = 0
print("Reloading locations from '"+location_file+"'.")
dbCur.execute('''
CREATE TABLE locations (id INTEGER PRIMARY KEY NOT NULL,
                        name,code,capital)''')
with open(location_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        na = str(r["name"])
        co = str(r["code"])
        ca = str(r["capital"])

        location = (location_numb,na,co,ca)
        dbCur.execute("INSERT INTO locations (id,name,code,capital) VALUES (?,?,?,?)",location)
        location_numb += 1

# Products
##########
# All Products
# For counting up the PID for all the products.
all_prods = 0

dbCur.execute('''
CREATE TABLE products (pid INTEGER PRIMARY KEY NOT NULL,
                       name,desc,price,startDate,endDate,days,location)''')
# This gets populated simultaneously as the other products come in.

# Hotels
hotels_file  = "./csv/hotels/hotelProducts.csv"
hotels_prods = 0
print("Reloading Hotel Products from '"+hotels_file+"'.")
dbCur.execute('''
CREATE TABLE prods_hotel (id INTEGER PRIMARY KEY NOT NULL,
                          pid INTEGER NOT NULL,
                          hotelier,
                          room_types,
                          hotel_features,
                          location,
                          FOREIGN KEY (pid) REFERENCES products(pid)
                          FOREIGN KEY (location) REFERENCES locations(id))''')
with open(hotels_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        na = str(r["name"])
        de = str(r["desc"])

        ho = int(r["hotelier"])
        ro = str(r["rooms"])
        fe = str(r["features"])

        hotel_prod = (all_prods,na,de)
        hotel_info = (all_prods,hotels_prods,ho,ro,fe)

        dbCur.execute("INSERT INTO products (pid,name,desc) VALUES (?,?,?)",hotel_prod)
        dbCur.execute("INSERT INTO prods_hotel (pid,id,hotelier,room_types,hotel_features) VALUES (?,?,?,?,?)",hotel_info)
        hotels_prods += 1
        all_prods += 1

# Insurance
insurance_file  = "./csv/insurance/insuranceProducts.csv"
insurance_prods = 0
print("Reloading Insurance Products from '"+insurance_file+"'.")
dbCur.execute('''
CREATE TABLE prods_insurance (id INTEGER PRIMARY KEY NOT NULL,
                              pid INTEGER NOT NULL,
                              ins_provider,ins_cover,
                              FOREIGN KEY (pid) REFERENCES products(pid))''')
with open(insurance_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        na = str(r["name"])
        de = str(r["desc"])

        co = str(r["covers"])
        pr = int(r["prov"])

        insurance_prod = (all_prods,na,de)
        insurance_info = (insurance_prods,all_prods,pr,co)

        dbCur.execute("INSERT INTO products (pid,name,desc) VALUES (?,?,?)",insurance_prod)
        dbCur.execute("INSERT INTO prods_insurance (id,pid,ins_provider,ins_cover) VALUES (?,?,?,?)",insurance_info)
        insurance_prods += 1
        all_prods += 1

# Vehicles
vehicles_file = "./csv/vehicles/vehicles.csv"
vehicles_prods = 0
print("Reloading Vehicle Products from '"+vehicles_file+"'.")
dbCur.execute('''
CREATE TABLE prods_vehicles (id INTEGER PRIMARY KEY NOT NULL,
                             pid INTEGER NOT NULL,
                             transporter,vtype,model,
                             drive,gears,
                             FOREIGN KEY (pid) REFERENCES products(pid))''')
with open(vehicles_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        na = str(r["name"])
        de = str(r["desc"])

        tr = int(r["transporter"])
        vt = str(r["vtype"])
        mo = int(r["model"])
        dr = int(r["drive"])
        gi = int(r["gears"])

        vehicle_prod = (all_prods,na,de)
        vehicle_info = (vehicles_prods,all_prods,tr,vt,mo,dr,gi)

        dbCur.execute("INSERT INTO products (pid,name,desc) VALUES (?,?,?)",vehicle_prod)
        dbCur.execute("INSERT INTO prods_vehicles (id,pid,transporter,vtype,model,drive,gears) VALUES (?,?,?,?,?,?,?)",vehicle_info)
        vehicles_prods += 1
        all_prods += 1

# Flights
flights_file = "./csv/flights/flights.csv"
flights_prods = 0
print("Reloading Flights Products from '"+flights_file+"'.")
dbCur.execute('''
CREATE TABLE prods_flights (id INTEGER PRIMARY KEY NOT NULL,
                            pid INTEGER KEY NOT NULL,
                            airport_depart,airport_arrive,
                            airline,flight_code,
                            depart_date,depart_time,
                            arrive_date,arrive_time,
                            ticket_id,
                            FOREIGN KEY (pid) REFERENCES products(pid))''')
with open(flights_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n   = str(r["airport_dep"]+" to "+r["airport_arr"]+
                  " by "+r["airline"]+" ("+r["flightCode"]+
                  ") - "+r["departDate"]+":"+r["departTime"]+
                  " / "+r["arriveDate"]+":"+r["arriveTime"])

        ade = str(r["airport_dep"])
        aar = str(r["airport_arr"])
        arl = str(r["airline"])
        dda = str(r["departDate"])
        dti = str(r["departTime"])
        ada = str(r["arriveDate"])
        ati = str(r["arriveTime"])
        fco = str(r["flightCode"])
        tix = str(r["ticket_id"])

        flight_prod = (all_prods,n)
        flight_info = (flights_prods,all_prods,ade,aar,arl,fco,dda,dti,ada,ati,tix)

        dbCur.execute("INSERT INTO products (pid,name) VALUES (?,?)",flight_prod)
        dbCur.execute("""INSERT INTO prods_flights (id,pid,airport_depart,airport_arrive,
                         airline,flight_code,depart_date,depart_time,arrive_date,arrive_time,ticket_id)
                         VALUES (?,?,?,?,?,?,?,?,?,?,?)""",flight_info)
        flights_prods += 1
        all_prods += 1

# Activities
activities_file = "./csv/activities/activities.csv"
activities_prods = 0
print("Reloading Activities Products from '"+activities_file+"'.")
dbCur.execute('''
CREATE TABLE prods_activities (id INTEGER PRIMARY KEY NOT NULL,
                               pid INTEGER NOT NULL,
                               act_provider,act_type,
                               FOREIGN KEY (pid) REFERENCES products(pid))''')
with open(activities_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        na = str(r["name"])
        de = str(r["desc"])

        pr = int(r["prov"])
        ty = int(r["act"])

        activity_prod = (all_prods,na,de)
        activity_info = (activities_prods,all_prods,pr,ty)

        dbCur.execute("""INSERT INTO products (pid,name,desc) VALUES (?,?,?)""",activity_prod)
        dbCur.execute("""INSERT INTO prods_activities (id,pid,act_provider,act_type) VALUES (?,?,?,?)""",activity_info)

        activities_prods += 1
        all_prods += 1

# Product Features
##################
# holy shit this'll take forever.
# At least these bits don't need individual product IDs.
# Thank goodness for that.

#################
# Hotels Features
# Hotel Rooms
hotelrooms_file = "./csv/hotels/hotelRooms.csv"
hotelrooms_id   = 0
print("Reloading Hotel Rooms from '"+hotelrooms_file+"'.")
dbCur.execute('''
CREATE TABLE hotel_rooms (id INTEGER PRIMARY KEY NOT NULL,
                          name,desc,cap,rate)''')
with open(hotelrooms_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])
        c = int(r["cap"])
        r = float(r["rate"])

        hotel_room = (hotelrooms_id,n,d,c,r)
        dbCur.execute("INSERT INTO hotel_rooms (id,name,desc,cap,rate) VALUES (?,?,?,?,?)",hotel_room)
        hotelrooms_id += 1

# Hotel Features
hotelfeatures_file = "./csv/hotels/hotelFeatures.csv"
hotelfeatures_id   = 0
print("Reloading Hotel Features from '"+hotelfeatures_file+"'.")
dbCur.execute('''
CREATE TABLE hotel_features (id INTEGER PRIMARY KEY NOT NULL,
                             name,desc,rate)''')
with open(hotelfeatures_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])
        r = float(r["rate"])

        hotel_feature = (hotelfeatures_id,n,d,r)
        dbCur.execute("INSERT into hotel_features (id,name,desc,rate) VALUES (?,?,?,?)",hotel_feature)
        hotelfeatures_id += 1

# Hoteliers
hoteliers_file = "./csv/hotels/hoteliers.csv"
hoteliers_id   = 0
print("Reloading Hoteliers from '"+hoteliers_file+"'.")
dbCur.execute('''
CREATE TABLE hotel_hoteliers (id INTEGER PRIMARY KEY NOT NULL,
                              name,rate)''')
with open(hoteliers_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        r = float(r["rate"])

        hotelier = (hoteliers_id,n,r)
        dbCur.execute("INSERT INTO hotel_hoteliers (id,name,rate) VALUES (?,?,?)",hotelier)
        hoteliers_id += 1

##################
# Flights Features
# Airlines
airlines_file = "./csv/flights/airliners.csv"
airlines_id   = 0
print("Reloading Airlines from '"+airlines_file+"'.")
dbCur.execute('''
CREATE TABLE flight_airlines (id INTEGER PRIMARY KEY NOT NULL,
                              name,desc,aircode,
                              countrycode,tickets)''')
with open(airlines_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])
        ac = str(r["aircode"])
        cc = str(r["countrycode"])
        ti = str(r["tickets"])

        airline = (airlines_id,n,d,ac,cc,ti)
        dbCur.execute("INSERT INTO flight_airlines (id,name,desc,aircode,countrycode,tickets) VALUES (?,?,?,?,?,?)",airline)
        airlines_id += 1

# Airports
airports_file = "./csv/flights/airports.csv"
airports_id   = 0
print("Reloading Airports from '"+airports_file+"'.")
dbCur.execute('''
CREATE TABLE flight_airports (id INTEGER PRIMARY KEY NOT NULL,
                              name,desc,code,ctry)''')
with open(airports_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])
        co = str(r["code"])
        ct = str(r["ctry"])

        airport = (airports_id,n,d,co,ct)
        dbCur.execute("INSERT INTO flight_airports (id,name,desc,code,ctry) VALUES (?,?,?,?,?)",airport)
        airports_id += 1

# Air Tickets
airtickets_file = "./csv/flights/airTickets.csv"
airtickets_id   = 0
print("Reloading Ticket Types from '"+airtickets_file+"'.")
dbCur.execute('''
CREATE TABLE flight_tickets (id INTEGER PRIMARY KEY NOT NULL,
                             name,desc,rate)''')
with open(airtickets_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])
        r = float(r["rates"])

        air_ticket = (airtickets_id,n,d,r)
        dbCur.execute("INSERT INTO flight_tickets (id,name,desc,rate) VALUES (?,?,?,?)",air_ticket)
        airtickets_id += 1

###################
# Vehicles Features
# Transporters
transporters_file = "./csv/vehicles/transporters.csv"
transporters_id   = 0
print("Reloading Transporter Companies from '"+transporters_file+"'.")
dbCur.execute('''
CREATE TABLE vehicle_transporters (id INTEGER PRIMARY KEY NOT NULL,
                                   name,desc,rate)''')
with open(transporters_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])
        r = float(r["rate"])

        transporter = (transporters_id,n,d,r)
        dbCur.execute("INSERT INTO vehicle_transporters (id,name,desc,rate) VALUES (?,?,?,?)",transporter)
        transporters_id += 1

# Transport Depots
# This one doesn't need a count up. Its foreign keyed to Transporters
# Even if the transporter info could handle holding this too, but there could be multiple depots.
# Yeah, these need more information to link them, like locations and such, but eh.
depots_file = "./csv/vehicles/transports.csv"
print("Reloading Transporter Depots from '"+depots_file+"'.")
dbCur.execute('''
CREATE TABLE vehicle_depots (transporter_id INTEGER NOT NULL,
                             cars,bikes,drives,gears,
                             FOREIGN KEY(transporter_id) REFERENCES vehicle_transporters(id))''')
with open(depots_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        td = int(r["trans"])
        ca = str(r["cars"])
        bi = str(r["bikes"])
        dr = str(r["drives"])
        ge = str(r["gears"])

        depot = (td,ca,bi,dr,ge)
        dbCur.execute("INSERT INTO vehicle_depots (transporter_id,cars,bikes,drives,gears) VALUES (?,?,?,?,?)",depot)

# Cars
cars_file = "./csv/vehicles/cars.csv"
cars_id   = 0
print("Reloading Cars from '"+cars_file+"'.")
dbCur.execute('''
CREATE TABLE vehicle_cars (id INTEGER PRIMARY KEY NOT NULL,
                           name,desc,rate)''')
with open(cars_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])
        r = float(r["rate"])

        car = (cars_id,n,d,r)
        dbCur.execute("INSERT INTO vehicle_cars (id,name,desc,rate) VALUES (?,?,?,?)",car)
        cars_id += 1

# Bikes
bikes_file = "./csv/vehicles/bikes.csv"
bikes_id   = 0
print("Reloading Bikes from '"+bikes_file+"'.")
dbCur.execute('''
CREATE TABLE vehicle_bikes (id INTEGER PRIMARY KEY NOT NULL,
                            name,desc,rate)''')
with open(bikes_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])
        r = float(r["rate"])

        bike = (bikes_id,n,d,r)
        dbCur.execute("INSERT INTO vehicle_bikes (id,name,desc,rate) VALUES (?,?,?,?)",bike)
        bikes_id += 1

# Drives
drives_file = "./csv/vehicles/drives.csv"
drives_id   = 0
print("Reloading Drive Types from '"+drives_file+"'.")
dbCur.execute('''
CREATE TABLE vehicle_drives (id INTEGER PRIMARY KEY NOT NULL,
                             name,desc)''')
with open(drives_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])

        drive = (drives_id,n,d)
        dbCur.execute("INSERT INTO vehicle_drives (id,name,desc) VALUES (?,?,?)",drive)
        drives_id += 1

# Gears
gears_file = "./csv/vehicles/gears.csv"
gears_id   = 0
print("Reloading Gear Configurations from '"+gears_file+"'.")
dbCur.execute('''
CREATE TABLE vehicle_gears(id INTEGER PRIMARY KEY NOT NULL,
                           name,desc)''')
with open(gears_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])

        gears = (gears_id,n,d)
        dbCur.execute("INSERT INTO vehicle_gears (id,name,desc) VALUES (?,?,?)",gears)
        gears_id += 1


####################
# Insurance Features
# Cover Options
insurancecovers_file = "./csv/insurance/insuranceCovers.csv"
insurancecovers_id   = 0
print("Reloading Insurance Covers from '"+insurancecovers_file+"'.")
dbCur.execute('''
CREATE TABLE insurance_covers (id INTEGER PRIMARY KEY NOT NULL,
                               name,desc,rate)''')
with open(insurancecovers_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])
        r = float(r["rate"])

        cover = (insurancecovers_id,n,d,r)
        dbCur.execute("INSERT INTO insurance_covers (id,name,desc,rate) VALUES (?,?,?,?)",cover)
        insurancecovers_id += 1

# Providers
insuranceprovs_file = "./csv/insurance/insuranceProviders.csv"
insuranceprovs_id   = 0
print("Reloading Insurance Providers from '"+insuranceprovs_file+"'.")
dbCur.execute('''
CREATE TABLE insurance_providers (id INTEGER PRIMARY KEY NOT NULL,
                                  name,desc,rate)''')
with open(insuranceprovs_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])
        r = float(r["rate"])

        provider = (insuranceprovs_id,n,d,r)
        dbCur.execute("INSERT INTO insurance_providers (id,name,desc,rate) VALUES (?,?,?,?)",provider)
        insuranceprovs_id += 1

#####################
# Activities Features
# Types
activitytypes_file = "./csv/activities/activityTypes.csv"
activitytypes_id   = 0
print("Reloading Activity Types from '"+activitytypes_file+"'.")
dbCur.execute('''
CREATE TABLE activity_type (id INTEGER PRIMARY KEY NOT NULL,
                            name,desc,rate)''')
with open(activitytypes_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])
        r = float(r["rate"])

        act_type = (activitytypes_id,n,d,r)
        dbCur.execute("INSERT INTO activity_type (id,name,desc,rate) VALUES (?,?,?,?)",act_type)
        activitytypes_id += 1

# Providers
activityproviders_file = "./csv/activities/activityProviders.csv"
activityproviders_id   = 0
print("Reloading Activity Providers from '"+activityproviders_file+"'.")
dbCur.execute('''
CREATE TABLE activity_provider (id INTEGER PRIMARY KEY NOT NULL,
                                name,desc,rate)''')
with open(activityproviders_file,newline="") as file:
    reader = csv.DictReader(file)
    for r in reader:
        n = str(r["name"])
        d = str(r["desc"])
        r = float(r["rate"])

        act_prov = (activityproviders_id,n,d,r)
        dbCur.execute("INSERT INTO activity_provider (id,name,desc,rate) VALUES (?,?,?,?)",act_prov)
        activityproviders_id += 1

#####################################
# And that should be it. Holy shit. #
#######################################
# That's an entire folder of CSV data #
#   turned into a proper Database!    #
#######################################

print("Executing Query: 'SELECT * FROM metadata'\nFetching first row.")

dbCur.execute('''
SELECT * FROM metadata
''')
print(dbCur.fetchone())

dbCon.commit()
dbCon.close()
print("You have a database now. Congratulations!")
exit()
