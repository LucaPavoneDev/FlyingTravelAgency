# Reference and Features Classes
from cl_Data import database as db
from cl_Products import Activity

##################
# FOR ACTIVITIES #
##################

class ActivityProvider(object):
    def __init__(self,
                 newName="UNNAMED ACTIVITY PROVIDER",
                 newDesc="UNDESCRIBED ACTIVITY PROVIDER",
                 newRate=0.00):
        # Create Activity Provider ID Number
        self.id = db.appendToList(db.actProvidersList,self)
        # Add Activity Provider Attributes
        self.name = newName
        self.desc = newDesc
        self.rate = newRate

    def __repr__(self):
        return(self.name)

class ActivityType(object):
    def __init__(self,
                 newName="UNNAMED ACTIVITY TYPE",
                 newDesc="UNDESCRIBED ACTIVITY TYPE",
                 newRate=0.00):
        # Create Activity Type ID Number
        self.id = db.appendToList(db.actTypesList,self)
        # Add Activity Type Attributes
        self.name = newName
        self.desc = newDesc
        self.rate = newRate

    def __repr__(self):
        return(self.name)

import csv, os, sqlite3
from ast import literal_eval as leval

csvDir  = os.getcwd()+"\\csv\\activities\\"
typeCSV = csvDir+"activityTypes.csv"
provCSV = csvDir+"activityProviders.csv"

dbCon = sqlite3.connect("./travelAgency.db")
dbCur = dbCon.cursor()

def getActivities_CSV(files):
    with open(files[0],newline="") as tFile:
        tr = csv.DictReader(tFile)
        for rowT in tr:
            n = rowT["name"]
            d = rowT["desc"]
            r = rowT["rate"]
            newT = ActivityType(n,d,r)

    with open(files[1],newline="") as pFile:
        pr = csv.DictReader(pFile)
        for rowP in pr:
            n = rowP["name"]
            d = rowP["desc"]
            r = rowP["rate"]
            newP = ActivityProvider(n,d,r)

def getActivities_SQL(types,providers):
    for type in types:
        name = type[0]
        desc = type[1]
        rate = float(type[2])

        newType = ActivityType(name,desc,rate)

    for provider in providers:
        name = provider[0]
        desc = provider[1]
        rate = float(provider[2])

        newProvider = ActivityProvider(name,desc,rate)

    '''
    for product in products:
        name = product[0]
        desc = product[1]

        provider = db.getObjFromList("actProvidersList",int(product[2]))
        activity = db.getObjFromList("actTypesList",int(product[3]))

        newAct = Activity(provider,activity)
        newAct.updateName(name)
        newAct.updateDesc(desc)
    '''

# Depricated
#getActivities_CSV([typeCSV,provCSV])

dbCur.execute("SELECT name, desc, rate FROM activity_type ORDER BY id")
types_tuple = dbCur.fetchall()
dbCur.execute("SELECT name, desc, rate FROM activity_provider ORDER BY id")
providers_tuple = dbCur.fetchall()
'''
dbCur.execute("""
SELECT products.name,
       products.desc,
       prods_activities.act_provider,
       prods_activities.act_type
FROM products INNER JOIN prods_activities
ON products.pid = prods_activities.pid
ORDER BY prods_activities.pid
""")
products_tuple = dbCur.fetchall()
'''

getActivities_SQL(types_tuple,providers_tuple)

dbCon.close()