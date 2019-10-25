import sqlite3
dbCon = sqlite3.connect("../travelAgency.db")
dbCur = dbCon.cursor()

# Will import all people as lists of tuples.
# Then interpret those into their own objects.
custsSQL = []
staffSQL = []

dbCur.execute('''SELECT fname, lname, email, homePhone, mobilePhone, desc
FROM customers ORDER BY id''')
custsSQL = dbCur.fetchall()
dbCur.execute('''SELECT fname, lname, email, homePhone, mobilePhone, desc
FROM staff ORDER BY id''')
staffSQL = dbCur.fetchall()

allList = []
allList.extend(custsSQL)
allList.extend(staffSQL)

class Person():
    def __init__(self,fn="",ln="",em="",ho="",mo="",de="",ty="Customer"):
        self.id    = 0
        self.fname = fn
        self.lname = ln
        self.email = em
        self.home  = ho
        self.mobile= mo
        self.desc  = de
        self.type  = ty
        self.handle= self.lname.replace(" ","").lower()+self.fname[:1].lower()
        
    def __repr__(self):
        return(self.fname+" "+self.lname)

# Create people objects and place them in lists.
# Give them incrementing ID numbers too.
# Staff
staffID   = 0
staffList = []
for p in staffSQL:
    np = Person(p[0],p[1],p[2],p[3],p[4],p[5],"Staff")
    np.id = staffID
    staffList.append(np)
    staffID += 1

# Customers
custID    = 0
custsList = []
for p in custsSQL:
    np = Person(p[0],p[1],p[2],p[3],p[4],p[5],"Customer")
    np.id = custID
    custsList.append(np)
    custID += 1

# Everyone (Staff + Customers)
peopleList = []

peopleList.extend(staffList)
peopleList.extend(custsList)

'''
allID      = 0
peopleList = []
for p in allList:
    np = Person(p[0],p[1],p[2],p[3],p[4],p[5])
    np.id = allID
    peopleList.append(np)
    allID += 1
'''

dbCon.commit()
dbCon.close()

# Todo: Split staff/customers, make separate lists.
