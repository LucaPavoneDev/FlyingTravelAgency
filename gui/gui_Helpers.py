from tkinter import *
# To get pop-up messages you gotta be a bit wonky. Oh well.
import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox

from cl_Interface import Window
import cl_Data
from cl_Data import database as db

# Helper Functions. Useful across multiple windows.
###################################################
def checkDB(li=None,data=db):
    # li = list within DB object to check for.
    # data = database to use. Defaults to 'db' as imported above.
    # returns True or False bools.ch

    # Check if database is valid first.
    if(isinstance(data,cl_Data.Database)):
        # Database is true blue. Check if given list is in db
        print("Database found. Checking for given List...")
        if(hasattr(data,li)):
            # List exists. Go for it!
            return True
        else:
            # List doesn't exist. Phooey!
            return False
    else:
        # Database not a DB object/no database to access. Abort!
        return False

def checkObject(obj=None):
    # obj = Object within a database list to inspect/sniff.
    # returns a string with its type name.
    return str(type(obj).__name__)

def getCurSel(dl):
    # dl = a tkinter listbox.
    # Returns a tuple with two spaces.
    try:
        return dl.curselection()
    except IndexError:
        print("Getting current selection from listbox failed? Oops?")
        pass

def getRecord(lis,ind,dl,offset=0):
    # Use the above function, getCurSel to get a suitable index/ind variable.
    # 'lis' is the [] list (not tkinter listbox) to check, loaded into the window as its made.
    # 'ind' is a Tuple from getting the current selection above.
    # 'dl' is the data listing/list info box to read from.
    # 'offset' determines how may places away from the selection it needs to be.
    # returns an object from the list, or string with error

    if(lis != []):
        # If the list isn't empty, go for it!
        try:
            tup = int(ind[0])
            #print("tup: "+str(tup))
        except IndexError:
            tup = dl.size()-1
        inum = tup+offset
        #print("inum: "+str(inum))
        try:
            i = lis[inum]
        except IndexError:
            if(inum > dl.size()-1):
                # list went above the limit
                inum = 0
            elif(inum < 0):
                # list went below 0.
                inum = dl.size()-1
            i = lis[inum]
        if(inum < 0):
            inum = dl.size()-1

        # Move the selection cursor in the listbox.
        dl.selection_clear(0,END)
        dl.selection_set(inum)
        dl.activate(inum)
        dl.see(inum)

        # Finally, a printout.
        try:
            print(str(i)+" is "+checkObject(i))
            return i
        except:
            # Not sure how, but if this fails, we're ready for such a possibility. Maybe.
            print("Aw, heck. That didn't work. That's not an object...?")
            return i
    else:
        # List is empty. Can't really go for it.
        print("Given object list is empty. Aborting.")
        return "No Record Loaded."

def getObjListIDs(obj,ci,si,pi):
    # Transforms the lists of objs in a transaction obj
    # into their respective IDs
    # Returns a tuple of 3 lists with integers in them.
    from cl_Orders import Transaction, Bill

    # Clear current IDs, as they may belong to a different product
    ci = []
    si = []
    pi = []

    if(isinstance(obj,(Transaction,Bill))):
        # Get lists from transaction object.
        custs = obj.customer
        staff = obj.staff
        prods = obj.prods

        print("Running List Objects in "+str(obj)+" into IDs...")

        # Now to iterate through these lists
        # and return each object's IDs into ci, si and pi.
        for c in custs:
            ci.append(c.id)
        #print("Customer IDs: "+str(ci))

        for s in staff:
            si.append(s.id)
        #print("Staff IDs: "+str(si))

        for p in prods:
            pi.append(p.pid)
        #print("Product IDs: "+str(pi))

        return (ci,si,pi)
    else:
        print("getObjListIDs Failed: Incoming object not a Transaction or Bill.")

def getIDListObjs(obj,ci,si,pi):
    # Transforms the lists of obj ids in the GUI
    # back into their respective objects

    # Returns a tuple with 3 lists of objects.

    cObj = []
    sObj = []
    pObj = []

    print("Running List IDs in "+str(obj)+" into Objects...")
    print("Custs Ids: "+str(ci))
    print("Staff Ids: "+str(si))
    print("Prods Ids: "+str(pi))

    for custs in ci:
        cObj.append(db.getObjFromList("customerList",custs))
    print("Customer Objects: "+str(cObj))

    for staff in si:
        sObj.append(db.getObjFromList("staffList",staff))
    print("Staff Objects: "+str(sObj))

    for prods in pi:
        pObj.append(db.getObjFromList("prodList",prods))
    print("Product Objects: "+str(pObj))

    return (cObj,sObj,pObj)