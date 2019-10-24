# Orders, Sales, and Dockets Classes
from cl_Data import database as db
import cl_Products as pr
import datetime as dt

class Transaction(object):
    def __init__(self,cu=[],st=[],pr=[],
                 date=dt.datetime.now()):
        # Create Transaction ID Numer
        self.tid = db.appendToList(db.transacList,self)
        # Create Essential Transaction Data
        self.datetime       = date     # Date and time of transaction
        self.customer       = cu       # List of customers involved.
        self.staff          = st       # List of staff involved.
        self.prods          = pr       # List of products.
        self.total          = (0.00,0) # Tuple with cost, and number of objs in prods
        self.notes          = ""       # For where notes about the transaction go.
        self.getTotalPrices()

    def __repr__(self):
        timeForm = "%a %d/%m/%y"
        return("Transaction #"+str(self.tid)+", "+str(self.datetime.strftime(timeForm)))

    def changeDatetime(self,Y=1970,M=1,d=1,h=12,m=0,s=0):
        # Case sensitive, so watch out.
        # At minimum you need Y, M, and d.
        # Y = Year   (1970-2038)
        # M = Month  (01-12)
        # d = Day    (01-31)

        # These are optional.
        # h = hour   (00-23)
        # m = minute (00-59)
        # s = second (00-59)

        newDate = dt.datetime(Y,M,d,h,m,s)
        oldDate = self.date
        self.datetime = newDate

    def addPerson(self,newPers):
        # Add a person or staff member from involvement in the transaction.
        from cl_People import Customer as c
        from cl_People import Staff as s
        if(isinstance(newPers,c)):
            if(newPers not in self.customer):
                self.customer.append(newPers)
                print("New customer "+str(newPers.fname)+" "+str(newPers.lname)
                      +" was added to the transaction.")
            else:
                print("Customer "+str(newPers.fname)+" "+str(newPers.lname)
                      +" is already involved with this transaction.")
        elif(isinstance(newPers,s)):
            if(newPers not in self.staff):
                self.staff.append(newPers)
                print("New staff member "+str(newPers.fname)+" "+str(newPers.lname)
                      +" was added to the transaction.")
            else:
                print("Staff member "+str(newPers.fname)+" "+str(newPers.lname)
                      +" is already involved with this transaction.")
        else:
            print("Object must be a customer or staff member.")

    def remPerson(self,oldPers):
        # Remove a person or staff member from involvement in the transaction.
        from cl_People import Customer as c
        from cl_People import Staff as s
        if(isinstance(oldPers,c)):
            if(oldPers in self.customer):
                self.customer.remove(oldPers)
                print("Customer "+str(oldPers.fname)+" "+str(oldPers.lname)
                      +" was removed from this transaction.")
            else:
                print("Customer "+str(oldPers.fname)+" "+str(oldPers.lname)
                      +" is not involved in this transaction.")
        elif(isinstance(oldPers,s)):
            if(oldPers in self.staff):
                self.staff.remove(oldPers)
                print("Staff member "+str(oldPers.fname)+" "+str(oldPers.lname)
                      +" was removed from this transaction")
            else:
                print("Staff member "+str(oldPers.fname)+" "+str(oldPers.lname)
                      +" is not involved in this transaction.")
        else:
            print("Object must be a customer or staff member.")

    def addProd(self,newProd):
        # Add a product to the order.
        # newProd = new product to add to order
        if(isinstance(newProd,pr.Product)):
            self.prods.append(newProd)
            print("New product successfully added to transaction.")
        else:
            print("Specified object is not a product.")

    def remProd(self,oldProd):
        # Remove a product from the order.
        # oldProd = product to remove from order
        if(isinstance(oldProd,pr.Product)):
            if(oldProd in self.prods):
                self.prods.remove(oldProd)
                print("Product removed successfully.")
            else:
                print("Specified product is not in list.")
        else:
            print("Specified object is not a product.")

    def getTotalPrices(self):
        # Reads current list of products.
        # Returns a list with the total of all product costs
        # and how many objects there are in the list.
        # (0,1) 0 = total, 1 = items
        if(len(self.prods) > 0):
            it = len(self.prods)
            pr = 0.00
            for p in self.prods:
                pr += p.price
            self.total = (format(pr,".2f"),it)
        else:
            print("No products in product list.")
            self.total = (0.00,0)

class Bill(Transaction):
    def __init__(self,cu=[],st=[],pr=[],date=dt.datetime.now(),due=dt.datetime.now(),pay=0.0,paid=False):
        Transaction.__init__(self,cu,st,pr,date)
        # Create Order ID Number
        self.id = db.appendToList(db.orderList,self)
        # Create Order Data
        self.dueDate = due
        self.amountPaid = pay
        self.paid = paid

    def __repr__(self):
        timeForm = "%a %d/%m/%y"
        return("Transaction #"+str(self.tid)+", Bill #"+str(self.id)+", "+str(self.datetime.strftime(timeForm)))

    def updateDueDate(self,Y=1970,M=1,d=1,h=12,m=0,s=0):
        # Case sensitive, so watch out.
        # Y = Year   (1970-2038)
        # M = Month  (01-12)
        # d = Day    (01-31)
        # h = hour   (00-23)
        # m = minute (00-59)
        # s = second (00-59)

        newDate = dt.datetime(Y,M,d,h,m,s)
        oldDate = self.dueDate
        self.dueDate = newDate

    def changePaid(self,newStatus):
        if(isinstance(newStatus,bool)):
            self.paid = newStatus
            print("Bill paid status has been changed to "+str(newStatus)+".")
        else:
            print("New status must be a bool True or False.")

    def addToAmountPaid(self,add=0.0):
        # Add a float or int (a number) to the amount paid on the bill.
        # Can also act as a remove, if negative value is passed.
        try:
            prev = self.amountPaid
            new  = self.amountPaid + add
            self.amountPaid = new
            print("Amount Paid on this bill is: "+str(self.amountPaid))
            if(isPaid() == True):
                self.paid = True
        except:
            print("That didn't work at all. Gimme a float or int next time!")

    def isPaid(self):
        self.getTotalPrices()
        if(self.amountPaid >= float(self.total[0])):
            self.paid = True
            return True
        else:
            self.paid = False
            return False

    def isDue(self):
        # Checks if the due date has passed the due date, and by how much.
        # Returns a tuple with (True/False, due date or days since due date).
        if(dt.datetime.now() > self.dueDate):
            # The due date is passed the current time.
            cd = dt.datetime.now()
            over = cd - self.dueDate
            return (True,over.days)
        else:
            # Due date has not occurred yet. By how many days?
            cd = dt.datetime.now()    # Get the current datetime.
            left = self.dueDate - cd    # Get the number of days left.
            # by subtracting the current date from the due date.
            return (False,left.days)
    
    def createInvoice(self):
        # Write a long, multi line string which encapsulates the
        # Transaction Details into a suitable invoice.
        # Will define some design constants here.
        
        logoString      = """   ______     _
  / __/ /_ __(_)__  ___ _  Flying
 / _// / // / / _ \/ _ `/  Travel
/_/ /_/\_, /_/_//_/\_, /   Agency
 _____/___/       /___/  __     __
/_  __/______ __  _____ / /  __/_/_
 / / / __/ _ `/ |/ / -_) /  /_-/-_/
/_/_/_/  \_,_/|___/\__/_/    /_/
  / _ |___ ____ ___  ______ __
 / __ / _ `/ -_) _ \/ __/ // /
/_/ |_\_, /\__/_//_/\__/\_, /
     /___/             /___/\n"""
        headerDatetime  = "\n== Invoice Information =========\n"
        timeForm        = "%d-%m-%y %I:%M:%S"
        invID           = "Invoice ID:  "+str(self.tid)+"."+str(self.id)
        curDate         = "Date Issued: "+dt.datetime.now().strftime(timeForm)
        dueDate         = "Date Due:    "+self.dueDate.strftime(timeForm)
        headerCustomers = "\n== Customer Details ============\n"
        headerStaff     = "\n== Staff Serving ===============\n"
        headerProducts  = "\n== Your Products ===============\n"
        headerPricing   = "\n== Pricing and Totals ==========\n"
        
        separator_large = "\n\n================================\n"
        separator_med   = "\n\n========================\n"
        separator_small = "\n  ----------------\n"
        
        footerPayable   = "Payable To: Flying Travel Agency\nBSB: 09876 54321\nABN: 123 456"
        
        paidCheck     = self.isPaid() # Checks the payment status.
        dueCheck      = self.isDue()  # Checks whether the invoice is due. (Tuple, 2 items)
        
        # Each line should be no more than 32 characters long, ideally.
        # 32 characters = |                                | long.
        
        if(paidCheck == False):
            if(dueCheck[0] == True):
                # Its overdue! dueCheck[1] contains how many days over.
                timingString = "Your payment is overdue by "+str(dueCheck[1])+" days!"
            else:
                # Not due yet, X many days in dueCheck[1] to pay before due date is gotten.
                timingString = "Payment is due in "+str(dueCheck[1])+" days."
        else:
            timingString = "This bill is considered paid."
        
        custsNameList = []
        for customer in self.customer:
            custsNameList.append(" - "+str(customer.fname)+" "+str(customer.lname)+"\n("+customer.contacts["email"]+")")

        staffNameList = []
        for staff in self.staff:
            staffNameList.append(" - "+str(staff.fname)+" "+str(staff.lname)+"\n("+staff.contacts["email"]+")")
        
        prodDetailsList = []
        for product in self.prods:
            prodDetailsList.append(" - "+str(product.name)+"\n - "+str(type(product).__name__)+"\n $"+str(format(product.price,".2f")))
        
        totalCost     = float(self.total[0])    # Monetary cost of all items in transaction.
        totalPaid     = float(self.amountPaid)  # Money paid so far.
        #print(totalCost)
        #print(totalPaid)
        #print(type(totalCost))
        #print(type(totalPaid))
        totalOut      = totalCost - totalPaid   # Money outstanding.
        totalItems    = self.total[1]           # Number of items in the transaction.
        
        costString    = "Grand Total:     "+str(format(totalCost,".2f"))
        paidString    = "Paid So Far:     "+str(format(totalPaid,".2f"))
        outString     = "Pay Outstanding: "+str(format(totalOut,".2f"))
        itemsString   = "Items in Docket: "+str(totalItems)
        
        invString     = "" # String to be written to and returned.
        # Begin Invoice String Build
        ############################
        def addString(string,add="",nl=False):
            # Simple helper function.
            if(nl == False):
                # Do not add a new line. (Default functionality)
                string = string + str(add)
                return string
            else:
                # Add a "\n" newline to the end.
                string = string + str(add) + "\n"
                return string
        
        invString = addString(invString,logoString)      # Add Logo.
        invString = addString(invString,headerDatetime)  # Add Date/Time Heading.
        invString = addString(invString,invID,True)      # Add Invoice ID.
        invString = addString(invString,curDate,True)    # Add date/time of creation/issue.
        invString = addString(invString,dueDate,True)    # Add due date for bill.
        
        invString = addString(invString,headerCustomers) # Add customer heading.
        for custName in custsNameList:                   # Add customer detail rows.
            invString = addString(invString,custName)        # Add customer.
            invString = addString(invString,separator_small) # Add separator.
        invString = addString(invString,headerStaff)     # Add staff heading.
        for staffName in staffNameList:                  # Add staff detail rows.
            invString = addString(invString,staffName)       # Add staff member.
            invString = addString(invString,separator_small) # Add separator.
        invString = addString(invString,headerProducts)  # Add products heading.
        for prodInfo in prodDetailsList:                 # Add product detail rows.
            invString = addString(invString,prodInfo)        # Add product.
            invString = addString(invString,separator_small) # Add separator.
        
        invString = addString(invString,headerPricing)   # Add payment/pricing heading.
        invString = addString(invString,itemsString,True)# Add items in bill
        invString = addString(invString,costString)      # Add total cost of bill.
        invString = addString(invString,separator_small) # Add separator.
        invString = addString(invString,paidString,True) # Amount paid by customers so far.
        invString = addString(invString,outString)       # Amount left.
        invString = addString(invString,separator_small) # Add separator.
        invString = addString(invString,timingString)    # Comment about timing.
        invString = addString(invString,separator_small) # Add separator.
        invString = addString(invString,footerPayable)   # Payment details.
        
        # To test this from Main after the interface is gone:
        # cl_Data.database.orderList[3].createInvoice()
        
        #print(invString)
        return invString

import csv, os, sqlite3
csvDir   = os.getcwd()+"\\csv\\"
tranFile = csvDir+"transactions.csv"

dbCon = sqlite3.connect("./travelAgency.db")
dbCur = dbCon.cursor()

dbCur.execute("""
SELECT datetime_year,  -- 0
       datetime_month, -- 1
       datetime_day,   -- 2
       customer_ids,   -- 3
       staff_ids,      -- 4
       prod_ids,       -- 5
       bill,           -- 6
       paid,           -- 7
       notes,          -- 8
       amount_paid,    -- 9
       duedate_year,   -- 10
       duedate_month,  -- 11
       duedate_day     -- 12
FROM transactions
ORDER BY tid
""")
transac_list = dbCur.fetchall()


def populateTransactions_SQL(tuplelist):
    for transac in tuplelist:
        date_y   = int(transac[0])
        date_m   = int(transac[1])
        date_d   = int(transac[2])
        custIDs  = str(transac[3]).split("|")
        staffIDs = str(transac[4]).split("|")
        prodIDs  = str(transac[5]).split("|")
        bill     = str(transac[6])
        payStat  = str(transac[7])
        notes    = str(transac[8]).replace('\\n','\n')

        # Yes, its really dumb, but Python is also dumb.
        # You gotta spell out to it that a newline is a newline
        # because it auto-converts any instance of \ into \\.
        # Which is REALLY DUMB AND I HATE IT.

        if(bill in ["true","True","TRUE",True]):
            bill = True
        else: bill = False

        if(payStat in ["true","True","TRUE",True]):
            payStat = True
        else: payStat = False

        try:    ampaid = float(transac[9])
        except: ampaid = 0.00
        try:    due_y  = int(transac[10])
        except: due_y  = 1970
        try:    due_m  = int(transac[11])
        except: due_m  = 1
        try:    due_d  = int(transac[12])
        except: due_d  = 1

        custObjs  = []
        staffObjs = []
        prodsObjs = []

        for customer in custIDs: custObjs.append(db.getObjFromList("customerList",int(customer)))
        for staff in staffIDs:   staffObjs.append(db.getObjFromList("staffList",int(staff)))
        for product in prodIDs:  prodsObjs.append(db.getObjFromList("prodList",int(product)))

        if(bill == True):
            newObj = Bill(cu=custObjs,st=staffObjs,pr=prodsObjs,
                          date=dt.datetime(date_y,date_m,date_d),
                          due=dt.datetime(due_y,due_m,due_d),
                          pay=ampaid,paid=payStat)
            newObj.notes = notes
        else:
            newObj = Transaction(cu=custObjs,st=staffObjs,pr=prodsObjs,
                                 date=dt.datetime(date_y,date_m,date_d))
            newObj.notes = notes

populateTransactions_SQL(transac_list)
dbCon.close()

"""
class Sale(Transaction):
    def __init__(self,c,s):
        Transaction.__init__(c,s)
        # Create Sale ID Number
        self.id = db.appendToList(db.salesList,self)
        # Create Sales Data
        self.assocOrder = None

class Docket(Transaction):
    def __init__(self,c,s):
        Transaction.__init__(c,s)
        # Create Docket ID Number
        self.id = db.appendToList(db.docketList,self)
"""

'''
def populateTransactions_CSV(file):
    # Populate transactions table with some dummy data.
    with open(file,newline="") as tFile:
        tr = csv.DictReader(tFile)
        for rowT in tr:
            # Gather items in the CSV.
            date_y      = int(rowT["datetime_year"])
            date_m      = int(rowT["datetime_month"])
            date_d      = int(rowT["datetime_day"])
            custIDs     = rowT["customer_ids"].split("|")
            staffIDs    = rowT["staff_ids"].split("|")
            prodIDs     = rowT["prod_ids"].split("|")
            bill        = str(rowT["bill"])
            payStat     = str(rowT["paid"])
            notes       = str(rowT["notes"]).replace('\\n','\n')

            # Yes, its really dumb, but Python is also dumb.
            # You gotta spell out to it that a newline is a newline
            # because it auto-converts any instance of \ into \\.
            # Which is REALLY DUMB AND I HATE IT.

            if(bill in ["true","True","TRUE"]):
                bill = True
            else: bill = False

            if(payStat in ["true","True","TRUE"]):
                payStat = True
            else: payStat = False

            # Render optional numbers.
            # They might not agree, so might as well try/except them with defaults.
            try: ampaid = float(rowT["amount_paid"])
            except: ampaid = 0.00
            try: due_y  = int(rowT["duedate_year"])
            except: due_y = 1970
            try: due_m  = int(rowT["duedate_month"])
            except: due_m = 1
            try: due_d  = int(rowT["duedate_day"])
            except: due_d = 1

            # Iterate through the Customer, Staff, and Product IDs.
            # Return objects using the getObjFromList() method in database.
            # Into these empty lists below.
            custObjs  = []
            staffObjs = []
            prodsObjs = []

            for customer in custIDs: custObjs.append(db.getObjFromList("customerList",int(customer)))
            for staff in staffIDs: staffObjs.append(db.getObjFromList("staffList",int(staff)))
            for product in prodIDs: prodsObjs.append(db.getObjFromList("prodList",int(product)))

            if(bill == True):
                # Transaction is a bill/billable.
                newObj = Bill(cu=custObjs,st=staffObjs,pr=prodsObjs,
                              date=dt.datetime(date_y,date_m,date_d),
                              due=dt.datetime(due_y,due_m,due_d),
                              pay=ampaid,paid=payStat)
                newObj.notes = notes
                print("Transaction ID No. #"+str(newObj.tid)+", with Bill ID No. #"+str(newObj.id)+" created.")
            else:
                # Transaction is not billable.
                newObj = Transaction(cu=custObjs,st=staffObjs,pr=prodsObjs,
                                     date=dt.datetime(date_y,date_m,date_d))
                newObj.notes = notes
                print("Tranasction ID No. #"+str(newObj.tid)+" created.")

#populateTransactions_CSV(tranFile)
'''