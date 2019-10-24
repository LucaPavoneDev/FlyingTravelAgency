# Reference and Features Classes
from cl_Data import database as db
from cl_Products import Insurance

#################
# FOR INSURANCE #
#################

class InsuranceProvider(object):
    def __init__(self,
                 n="UNNAMED INSURANCE PROVIDER",
                 d="UNDESCRIBED INSURANCE PROVIDER.",
                 r=0.00):
        # Create Insurance Provider ID Number
        self.id = db.appendToList(db.insProvidersList,self)
        # Create Attributes
        self.name = n
        self.desc = d
        self.rate = r

    def __repr__(self):
        return self.name

class InsuranceCover(object):
    def __init__(self,n,d,r):
        # Create Insurance Cover ID Number
        self.id = db.appendToList(db.insCoverList,self)
        # Create Attributes
        self.name = n
        self.desc = d
        self.rate = r

    def __repr__(self):
        return self.name

# Start the fun - import csv, os, and set up directory vars.
import csv, os, sqlite3
from ast import literal_eval as leval

csvDir  = os.getcwd()+"\\csv\\insurance\\"
provCSV = csvDir+"insuranceProviders.csv"
coveCSV = csvDir+"insuranceCovers.csv"
prodCSV = csvDir+"insuranceProducts.csv"

dbCon = sqlite3.connect("./travelAgency.db")
dbCur = dbCon.cursor()

def populateInsurance_CSV(file,obj,comment="The Database"):
    with open(file,newline="") as fFile:
        fr = csv.DictReader(fFile)
        for rowF in fr:
            n = rowF["name"]
            d = rowF["desc"]
            r = float(rowF["rate"])
            newObj = obj(n,d,r)
            print(newObj.name+" added to "+comment+" at #"+str(newObj.id)+" for "+str(newObj.rate)+".")

def populateInsurance_SQL(ins_tuple,obj,comment="The Database"):
    for thing in ins_tuple:
        name = thing[0]
        desc = thing[1]
        rate = thing[2]
        newObj = obj(name,desc,rate)


# Depricated CSV
#populateInsurance_CSV(provCSV,InsuranceProvider,"Insurance Providers")
#populateInsurance_CSV(coveCSV,InsuranceCover,"Insurance Covers")

dbCur.execute("SELECT name, desc, rate FROM insurance_covers ORDER BY id")
covers = dbCur.fetchall()
dbCur.execute("SELECT name, desc, rate FROM insurance_providers ORDER BY id")
providers = dbCur.fetchall()
populateInsurance_SQL(providers,InsuranceProvider)
populateInsurance_SQL(covers,InsuranceCover)


# Create product based off product csv.
# Provider, Package Name, Package Description, Rates
'''
def createInsuranceProduct_CSV(file,obj,comment=""):
    # This one's gonna be a doozy!
    with open(file,newline="") as pFile:
        pr = csv.DictReader(pFile)
        for rowP in pr:
            n = rowP["name"]
            d = rowP["desc"]
            p = rowP["prov"]
            c = rowP["covers"]

            insProv = db.insProvidersList[int(p)]

            insCover = []
            if(c != "None"):
                cL = c.split("|")
                for cover in cL:
                    insCover.append(db.insCoverList[int(cover)])

            nObj = obj(insProv,insCover)
            nObj.updateName(n)
            nObj.updateDesc(d)
            nObj.calcInsurancePrice()
'''
# For creating multiple insurance products based off one SQL query.
# Deprecated.
'''
def createInsuranceProduct_SQL(prod_tuple):
    for insurance_product in prod_tuple:
        name = insurance_product[0]
        desc = insurance_product[1]

        prov = db.getObjFromList("insProvidersList",int(insurance_product[2]))
        if(insurance_product[3] != "None"):
            cover_ids = insurance_product[3].split("|")
        else: cover_ids = []
        covers = []

        for cover_opt in cover_ids:
            covers.append(db.getObjFromList("insCoverList",int(cover_opt)))

        new_insurance = Insurance(prov,covers)
        new_insurance.updateName(name)
        new_insurance.updateDesc(desc)
        new_insurance.calcInsurancePrice()
'''

# Depricated code.
#createInsuranceProduct_CSV(prodCSV,Insurance,"Insurance Products")
'''
dbCur.execute("""
SELECT products.name,
       products.desc,
       prods_insurance.ins_provider,
       prods_insurance.ins_cover
FROM products INNER JOIN prods_insurance
ON products.pid = prods_insurance.pid
ORDER BY prods_insurance.pid
""")
products = dbCur.fetchall()

createInsuranceProduct_SQL(products)
'''
dbCon.close()