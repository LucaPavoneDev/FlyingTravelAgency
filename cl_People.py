# People Object Classes
from cl_Data import database as db

class Person(object):
    def __init__(self,fn="Test",ln="Testington"):
        # Create Person's Attributes
        self.fname      = fn
        self.lname      = ln
        self.contacts   = {"email":"blank@test.com",
                           "homePhone":"03 1234 5678",
                           "mobilePhone":"0123 456 789"}
        self.address    = {"zipcode":"",
                           "state":"",
                           "city":"",
                           "streetName":"",
                           "streetNumber":"",
                           "unitNumber":""}
        self.desc       = ""

    def __repr__(self):
        return self.fname+" "+self.lname

    def updateContacts(self,newCont):
        # Overwrite current contact info with a dictionary.
        if(isinstance(newCont,dict)):
            self.contacts = newCont
            print(self.fname+" "+self.lname+"'s contact details have been updated to "
                  +str(self.contacts))
        else:
            print("That is not a dictionary object.")

    def updateAddress(self,newAdd):
        # Overwrite current address with a dictonary.
        if(isinstance(newAdd,dict)):
            self.address = newAdd
            print(self.fname+" "+self.lname+"'s address details have been updated to "
                  +str(self.address))
        else:
            print("That is not a dictionary object.")

    def enterAddress(self):
        # Enter new address for a customer, row by row.
        things = ["zipcode","state","city","streetName","streetNumber","unitNumber"]
        inputs = []

        for t in things:
            newInput = input("Input new "+str(t)+" for "
                             +self.fname+" "+self.lname+". (Leave blank for 'None')\n>")
            if(newInput == ""):
                newInput = None
            inputs.append(newInput)

        # Add inputs and things together to create an address dictionary.
        newAddress = {things[0]:inputs[0],
                      things[1]:inputs[1],
                      things[2]:inputs[2],
                      things[3]:inputs[3],
                      things[4]:inputs[4],
                      things[5]:inputs[5]}

        # Let user review address before committing update.
        choice = None
        while(choice == None):
            print(newAddress)
            preChoice = input("Is this new address data for "
                              +self.fname+" "+self.lname+" correct? (Y/N)\n>").upper()
            if(preChoice in ["Y","N"]):
                choice = preChoice
            else:
                print("Please enter Y or N.")

        # If user is happy with it, commit changes.
        if(choice == "Y"):
            self.address = newAddress
            print("New address details for "+self.fname
                  +" were successfully updated.")
        else:
            print("New address details for "+self.fname
                  +" were discarded.")

class Customer(Person):
    def __init__(self,
                 fn="Test",
                 ln="Testington"):
        # Create Customer ID Number
        Person.__init__(self,fn,ln)
        self.id = db.appendToList(db.customerList,self)
        self.contacts   = {"email":"testt@widgets.com",
                           "homePhone":"03 1234 5678",
                           "mobilePhone":"0404 123 456"}
        self.address    = {"zipcode":"",
                           "state":"",
                           "city":"",
                           "streetName":"",
                           "streetNumber":"",
                           "unitNumber":""}

class Staff(Person):
    def __init__(self,
                 fn="Toast",
                 ln="Toastersen"):
        Person.__init__(self,fn,ln)
        # Create Staff ID Number
        self.id = db.appendToList(db.staffList,self)
        # Create Staff Essentials
        self.fname      = fn
        self.lname      = ln
        self.contacts   = {"email":"toastt@travelagency.com",
                           "homePhone":"03 1234 5678",
                           "mobilePhone":"0404 789 012"}
        self.address    = {"zipcode":"",
                           "state":"",
                           "city":"",
                           "streetName":"",
                           "streetNumber":"",
                           "unitNumber":""}

# Start the fun - import csv, os, and set up directory vars.
import csv, os, sqlite3
from ast import literal_eval as leval

csvDir  = os.getcwd()+"\\csv\\"
custCSV  = csvDir+"customers.csv"
staffCSV = csvDir+"staff.csv"

dbCon = sqlite3.connect("./travelAgency.db")
dbCur = dbCon.cursor()

# Depricated CSV Imports
'''
# Populate Customer table
with open(custCSV,newline="") as custFile:
    custReader = csv.DictReader(custFile)
    for rowC in custReader:
        newCustomer = Customer(str(rowC["fname"]),
                               str(rowC["lname"]))
        litContacts = {"email":rowC["email"],
                       "homePhone":rowC["homePhone"],
                       "mobilePhone":rowC["mobilePhone"]}
        newCustomer.updateContacts(litContacts)
        litAddress = {"zipcode":rowC["zipcode"],
                      "state":rowC["state"],
                      "city":rowC["city"],
                      "streetName":rowC["streetName"],
                      "streetNumber":rowC["streetNumber"],
                      "unitNumber":leval(rowC["unitNumber"])}
        newCustomer.updateAddress(litAddress)

'''
'''
# Populate Staff Table
with open(staffCSV,newline="") as staffFile:
    staffReader = csv.DictReader(staffFile)
    for rowS in staffReader:
        newStaff = Staff(rowS["fname"],
                         rowS["lname"])
        litContacts = {"email":rowS["email"],
                       "homePhone":rowS["homePhone"],
                       "mobilePhone":rowS["mobilePhone"]}
        newStaff.updateContacts(litContacts)
'''

# Populate Customer table from SQL
dbCur.execute("""
SELECT fname,lname,email,desc,
       homePhone,mobilePhone,
       zipcode,state,city,
       streetName,streetNumber,
       unitNumber
FROM customers
ORDER BY id
""")
customers_tuple = dbCur.fetchall()

dbCur.execute("""
SELECT fname,lname,email,desc,
       homePhone,mobilePhone
from staff
ORDER BY id
""")
staff_tuple     = dbCur.fetchall()

def populateCustomers_SQL(custs_tup):
    for cust in custs_tup:
        fname = cust[0]
        lname = cust[1]
        email = cust[2]
        desc  = cust[3]

        hPhone = cust[4]
        mPhone = cust[5]

        zip   = cust[6]
        state = cust[7]
        city  = cust[8]
        sName = cust[9]
        sNumb = cust[10]
        uNumb = str(cust[11])

        newCust = Customer(fname,lname)
        newCust.desc = desc
        litContacts = {"email":email,
                       "homePhone":hPhone,
                       "mobilePhone":mPhone}
        newCust.updateContacts(litContacts)
        litAddress = {"zipcode":zip,
                      "state":state,
                      "city":city,
                      "streetName":sName,
                      "streetNumber":sNumb,
                      "unitNumber":uNumb}
        newCust.updateAddress(litAddress)

def populateStaff_SQL(staff_tup):
    for staff in staff_tup:
        fname  = staff[0]
        lname  = staff[1]
        email  = staff[2]
        desc   = staff[3]

        hPhone = staff[4]
        mPhone = staff[5]

        newStaff = Staff(fname,lname)
        newStaff.desc = desc
        litContacts = {"email":email,
                       "homePhone":hPhone,
                       "mobilePhone":mPhone}
        newStaff.updateContacts(litContacts)

populateCustomers_SQL(customers_tuple)
populateStaff_SQL(staff_tuple)

dbCon.close()