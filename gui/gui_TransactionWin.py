from tkinter import *
# To get pop-up messages you gotta be a bit wonky. Oh well.
import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox

from cl_Interface import Window
from cl_Data import database as db
from gui.gui_Helpers import *
import cl_Orders
import datetime as dt
import sqlite3

# Define transaction records window and functions.
##################################################
class TransactionWindow(Window):
    def __init__(self,master=None,listName="transacList"):
        Window.__init__(self,master)
        self.master    = master
        self.prodsWin  = None
        self.prodsApp  = None
        self.changeWin = None
        self.changeApp = None

        self.currentRec= None
        self.customerIDs = []
        self.staffIDs    = []
        self.productIDs  = []

        # Do the database/list name check before proceeding.
        if(checkDB(listName) == True):
            # Database check returned True.
            print("List '"+str(listName)+"' is where it needs to be. Opening...")
            # Start the Data window stuff.
            self.transactionsWindow(getattr(db,listName),listName)
            self.editView = None
        else:
            # Database check returned False. Delete self to save memory.
            print("List in database not found. Aborting window creation and deleting self.")
            del self

    def transactionsWindow(self,li,lis=""):
        # Since this window is looking specifically for Transactions
        # we don't have to be as broad when we grab records. We know what data we're after.
        titleText = "Flying Travel Agency - Transactions and Payments - "+str(lis)
        outerPad = 4
        innerPad = 2

        # Define window title.
        self.master.title(titleText)

        # Pre-pack the 'base' of the database.
        self.pack(fill="y",expand=1,padx=outerPad,pady=outerPad)

        # Now start putting other elements together
        # starting with the essential 'frames' for data.
        transacImage    = PhotoImage(file=r"./img/icon_Customers.png")
        commnoteImage   = PhotoImage(file=r"./img/icon_Staff.png")

        tabFrame        = ttk.Notebook(self)
        topFrame        = Frame(self)
        botFrame        = Frame(self)

        rightFrame      = Frame(self)
        rightFrame.pack(side=RIGHT)

        tabFrame.add(topFrame,text="Transaction Info",image=transacImage,compound=LEFT)
        tabFrame.add(botFrame,text="Communication and Notes",image=commnoteImage,compound=LEFT)

        tabFrame.transacImage  = transacImage
        tabFrame.commnoteImage = commnoteImage

        tabFrame.pack(side=BOTTOM,padx=outerPad,pady=outerPad)

        #topFrame.pack(side=TOP,fill="x")
        #botFrame.pack(side=BOTTOM,fill="x")

        recordFrame     = LabelFrame(self,text="Transaction Records")
        invoiceFrame    = LabelFrame(rightFrame,text="Invoice Preview")
        peopleFrame     = LabelFrame(topFrame,text="People in Transaction")
        dateFrame       = LabelFrame(topFrame,text="Record Data")
        productFrame    = LabelFrame(topFrame,text="Products in Transaction")
        commFrame       = LabelFrame(botFrame,text="Communication")
        notesFrame      = LabelFrame(botFrame,text="Transaction Notes")

        # Packing those frames before we get to work.
        invoiceFrame.pack(padx=outerPad,pady=outerPad)
        allFrames = [peopleFrame,dateFrame,productFrame]
        for fr in allFrames:
            fr.pack(fill="y",side=LEFT,padx=outerPad,pady=outerPad)
        else:
            notesFrame.pack(fill="x",side=BOTTOM,padx=outerPad,pady=outerPad)
            commFrame.pack(fill="x",side=BOTTOM,padx=outerPad,pady=outerPad)

        recordFrame.pack(fill="x",side=TOP,padx=outerPad,pady=outerPad)

        # Record frame objects
        ######################
        # Create record frame items, including the list of records, data listbox, etc.
        GUI_recordList      = StringVar()
        GUI_recordList.set(li)

        # Now to set up all the frames within this frame.
        reclistFrame        = Frame(recordFrame)
        rbuttFrame          = Frame(recordFrame)
        reclistFrame.pack(side="top",fill="x",pady=innerPad,padx=innerPad)
        rbuttFrame.pack(side="bottom",fill="x",pady=innerPad,padx=innerPad)

        # Setting up the scrollbar and the record listing.
        recordScroll        = Scrollbar(reclistFrame,jump=1)
        recordDatalist      = Listbox(reclistFrame,height=10,width=80,listvariable=GUI_recordList,
                                      selectmode="SINGLE",activestyle="dotbox",yscrollcommand=recordScroll.set)
        recordScroll.config(command=recordDatalist.yview)

        # Bind command to the data list.
        recordDatalist.bind("<Double-1>",lambda x: createTransView(getRecord(li,getCurSel(recordDatalist),recordDatalist)))

        # Then pack the scroll and list together in their frame.
        recordScroll.pack(side="right",fill="y")
        recordDatalist.pack(side="right",fill="both")

        # Create a container for the data object to live in and get used.
        # Maybe? Not sure if this is how it works...
        self.currentRec = getRecord(li,(recordDatalist.size()-1,0),recordDatalist)
        # currentRec is ALWAYS a transaction/bill object.

        GUI_currentRecVar = StringVar()
        GUI_currentRecVar.set("Viewing: "+str(self.currentRec))

        recordOpen  = Button(rbuttFrame,text="Open",command=lambda: createTransView(getRecord(li,getCurSel(recordDatalist),recordDatalist,offset=0)))
        recordFirst = Button(rbuttFrame,text="First",command=lambda: createTransView(getRecord(li,(0,0),recordDatalist)))
        recordPrev  = Button(rbuttFrame,text="Previous",command=lambda: createTransView(getRecord(li,getCurSel(recordDatalist),recordDatalist,offset=-1)))
        recordNext  = Button(rbuttFrame,text="Next",command=lambda: createTransView(getRecord(li,getCurSel(recordDatalist),recordDatalist,offset=1)))
        recordLast  = Button(rbuttFrame,text="Last",command=lambda: createTransView(getRecord(li,(recordDatalist.size()-1,0),recordDatalist)))
        recordNew   = Button(rbuttFrame,text="New",command=lambda: newTransaction())
        crecLabel   = Label(rbuttFrame,textvariable=GUI_currentRecVar)

        # Pack record frame objects.
        for widgesLeft in [recordFirst,recordPrev,recordOpen,recordNext,recordLast,recordNew]:
            widgesLeft.pack(side="left",fill="both")
        for widgesRight in [crecLabel]:
            widgesRight.pack(side="right",fill="both")

        # People frame objects.
        #######################
        # More of those funny string vars.
        # They don't do listvars, unfortunately.
        GUI_customerList = StringVar()
        GUI_staffList    = StringVar()

        # List of customer data.
        customerDatalist = Listbox(peopleFrame,height=4,width=25,listvariable=GUI_customerList)
        customerLabel    = Label(peopleFrame,text="Customers")

        # List of staff data.
        staffDatalist    = Listbox(peopleFrame,height=4,width=25,listvariable=GUI_staffList)
        staffLabel       = Label(peopleFrame,text="Staff")

        # Button stuff.
        changeButton = Button(peopleFrame,text="Change People",command=lambda: openChangeThings(self.currentRec))

        # Packing the people frame objects and widgets.
        customerLabel.pack()
        customerDatalist.pack()
        staffLabel.pack()
        staffDatalist.pack()
#        peopleButtons.pack(side="bottom",pady=innerPad,padx=innerPad)
        changeButton.pack(side="bottom",fill="x")
#        addButton.pack(side="left",fill="x")
#        remButton.pack(side="left",fill="x")

        # Date/Payment frame objects
        ############################
        GUI_obType    = StringVar()  # Name of the class being read (Bill or Transaction).
        GUI_dateTime  = StringVar()  # Datetime into a string here.
        GUI_prodPrice = DoubleVar()  # Price of products in transaction. Part 0 of the 'total' tuple.
        GUI_dueDate   = StringVar()  # Ditto.
        GUI_amoPaid   = DoubleVar()  # Float value of how much has been paid on the bill so far.
        GUI_paid      = BooleanVar() # Bool for whether or not the bill's considered paid.
        GUI_prodItems = IntVar()     # Number of products in transaction. Part 1 of the 'total' tuple.

        # https://docs.python.org/3/library/datetime.html?highlight=datetime#strftime-and-strptime-behavior
        # Useful guide on how I got datetimes into/out of strings.

        # Date Entry Field and Label.
        transacDateFrame = Frame(dateFrame)
        transacDateFrame.pack(fill="x",pady=innerPad,padx=innerPad)

        classLab  = Label(transacDateFrame,textvariable=GUI_obType)
        dateLabel = Label(transacDateFrame,text="Date Made: ",justify=LEFT)
        dateEntry = Entry(transacDateFrame,width=12,textvariable=GUI_dateTime)

        classLab.pack(side="top")
        dateLabel.pack(side="left")
        dateEntry.pack(side="right")

        # Due Date field and label
        transacDueFrame = Frame(dateFrame)
        transacDueFrame.pack(fill="x",pady=innerPad,padx=innerPad)

        dueLabel = Label(transacDueFrame,text="Date Due: ",justify=LEFT)
        dueEntry = Entry(transacDueFrame,width=12,textvariable=GUI_dueDate)

        dueLabel.pack(side="left")
        dueEntry.pack(side="right")

        # Price/Prods label
        priceFrame = Frame(dateFrame)
        priceFrame.pack(fill="x",pady=innerPad,padx=innerPad)

        priceLabel = Label(priceFrame,textvariable=GUI_prodPrice,justify=LEFT)
        priceLabel.pack(fill="x")

        prodsLabel = Label(priceFrame,textvariable=GUI_prodItems)
        prodsLabel.pack(fill="x")

        # Amount paid field and label
        amountPaidFrame = Frame(dateFrame)
        amountPaidFrame.pack(fill="x",pady=innerPad,padx=innerPad)

        ampLabel = Label(amountPaidFrame,text="Paid: ",justify=LEFT)
        ampEntry = Entry(amountPaidFrame,width=12,textvariable=GUI_amoPaid)
        ampCheck = Checkbutton(amountPaidFrame,variable=GUI_paid)

        ampLabel.pack(side="left")
        ampCheck.pack(side="right")
        ampEntry.pack(side="right")

        # Save Record Data
        saveFrame = Frame(dateFrame)
        saveButt  = Button(saveFrame,text="Save and Update Price",command=lambda: saveTransaction(self.currentRec))

        saveFrame.pack(side="bottom",fill="x",pady=innerPad,padx=innerPad)
        saveButt.pack(fill="both")

        # Product Frame objects
        #######################
        GUI_prodsList = StringVar() # List of products in transaction

        # Frames for buttons and list.
        prodList    = Frame(productFrame)
        prodList.pack(side="top",fill="x",pady=innerPad,padx=innerPad)

        # Scroll Bar and Datalist.
        productScroll = Scrollbar(prodList)
        productDatalist = Listbox(prodList,height=11,width=25,listvariable=GUI_prodsList,
                                  selectmode="SINGLE",activestyle="dotbox",yscrollcommand=productScroll.set)
        productScroll.config(command=productDatalist.yview)
        productScroll.pack(side="right",fill="y")
        productDatalist.pack(side="right",fill="y")

        # Number of prods and add/remove product buttons.
        changeProd = Button(productFrame,text="Change Products",command=lambda: openChangeThings(self.currentRec))
        changeProd.pack(side=BOTTOM,fill="x")

        # Communications Frame Objects
        ##############################
        commCont = Frame(commFrame)
        commCont.pack(fill="both",pady=innerPad,padx=innerPad)

        emailCusts = Button(commCont,text="Email Customers",command=lambda: sendEmail(self.currentRec,["c"]))
        emailStaff = Button(commCont,text="Email Staff",command=lambda: sendEmail(self.currentRec,["s"]))
        emailAll   = Button(commCont,text="Email All Involved",command=lambda: sendEmail(self.currentRec,["c","s"]))

        emailCusts.grid(row=0,column=0,sticky="ew",pady=innerPad,padx=innerPad)
        emailStaff.grid(row=0,column=1,sticky="ew",pady=innerPad,padx=innerPad)
        emailAll.grid(row=0,column=2,sticky="ew",pady=innerPad,padx=innerPad)

        custsComm = Listbox(commCont,width=25,height=4,listvariable=GUI_customerList)
        staffComm = Listbox(commCont,width=25,height=4,listvariable=GUI_staffList)

        custsComm.grid(row=1,column=0,pady=innerPad,padx=innerPad)
        staffComm.grid(row=1,column=1,pady=innerPad,padx=innerPad)

        emailTypeFrame = Frame(commCont)
        emailTypeFrame.grid(row=1,column=2,pady=innerPad,padx=innerPad)

        emailTypes = ["Order Receipt","Order Success","Order Fail","Order Cancellation","Billing Success",
                      "Billing Notice","Billing Warning","Billing Cancellation","Eviction"]

        GUI_emailType = StringVar()
        GUI_emailType.set(emailTypes[0])

        # Define a callback function for the dropdown menu
        def menuCallback(selection):
            try:
                ind = emailTypes.index(selection)
                print(selection+", Index: "+str(ind))
            except ValueError:
                print("menuCallback reported ValueError: Element not found in list.")

        # Set up widgets for Search Frame
        emailLabel  = Label(emailTypeFrame,text="Email Type").pack(side=TOP)
        emailDrop   = OptionMenu(emailTypeFrame,GUI_emailType,*emailTypes,command=menuCallback).pack(side=TOP)

        #for e in [emailCusts,emailStaff,emailAll]:
        #    e.pack(side="left",fill="both",expand=1)

        # Notes Frame Objects
        #####################
        noteCont = Frame(notesFrame)
        noteCont.pack(fill="both",pady=innerPad,padx=innerPad)

        noteScroll = Scrollbar(noteCont,jump=1)
        noteText   = Text(noteCont,height=5,width=50,wrap=WORD,yscrollcommand=noteScroll.set)
        noteScroll.config(command=noteText.yview)

        noteScroll.pack(side="right",fill="y")
        noteText.pack(side="right",fill="x",expand=1)

        # Invoice Frame Objects
        #######################
        invoiceCont   = Frame(invoiceFrame)
        invoiceCont.pack()

        invoiceScroll = Scrollbar(invoiceCont,jump=1)
        invoiceText   = Text(invoiceCont,height=28,width=48,wrap=WORD,yscrollcommand=invoiceScroll.set)
        invoiceScroll.config(command=invoiceText.yview)
        invGenButton  = Button(invoiceCont,text="Generate Invoice (Bill Only)",command=lambda: writeInvoice(self.currentRec))
        invSavButton  = Button(invoiceCont,text="Save Invoice to File (Bill Only)",command=lambda: saveInvoice(self.currentRec))

        invoiceText.grid(row=0,column=0,columnspan=2,padx=innerPad,pady=innerPad)
        invoiceScroll.grid(row=0,column=2,sticky=N+S)
        invGenButton.grid(row=1,column=0,padx=innerPad,pady=innerPad)
        invSavButton.grid(row=1,column=1,padx=innerPad,pady=innerPad)

        # Transaction Data Objects and Functions
        ########################################
        # Binding things to the main window?
        self.bind("<FocusIn>",lambda x: createTransView(self.currentRec))

        def writeInvoice(obj):
            invoiceText.delete((0.0),END)
            try:
                invoiceText.insert(END,obj.createInvoice())
            except:
                invoiceText.insert(END,"This transaction is not billable.\nPlease select a Bill to generate an invoice.")

        def saveInvoice(obj):
            choose = tkinter.messagebox.askyesno("Flying Travel Agency","Save this invoice to file?")
            if(choose == True):
                import os
                try:
                    # Create directory for invoices to live in.
                    os.mkdir("./invoices/")
                except FileExistsError:
                    # Directory for invoices already exists.
                    pass
                
                # Write Invoice
                try:
                    invoiceToWrite  = obj.createInvoice()
                    timeForm        = "%d-%m-%y_%I-%M-%S"
                    invoiceFilename = "./invoices/INVOICE__TID"+"_"+str(obj.tid)+"."+str(obj.id)+"_DT_"+dt.datetime.now().strftime(timeForm)+".txt"
                    print(invoiceFilename)
                    with open(invoiceFilename,"w") as text_file:
                        text_file.write(invoiceToWrite)
                    tkinter.messagebox.showinfo("Flying Travel Agency",str(obj)+"'s Invoice was successfully written to the following file:\n\""+invoiceFilename+"\"")
                except AttributeError:
                    tkinter.messagebox.showerror("Flying Travel Agency","This is not a billable transaction. Cannot create an invoice.")

        def updateNotes(obj,n):
            # Gets a dump of text from a given Text widget.
            try:
                return n.get((0.0),"end-1c")
            except:
                print("That wasn't a Text widget, fool!")

        def createTransView(obj):
            # This works after GetRecord() does its thing and returns the 'obj'.
            # to be unpacked by our GUI. The object we're expecting is a bill or
            # transaction to be viewed/processed, so we're expecting to find specific
            # attributes to report to the GUI.

            type = checkObject(obj)
            timeForm = "%d/%m/%y"  # "%a %d/%m/%y %H:%M"
            # Time format should read like: "Sun 16/06/2019"

            if(type in ["Transaction","Bill"]):
                #print("Updating controlled variables...")
                GUI_recordList.set(li)
                GUI_customerList.set(obj.customer)
                GUI_staffList.set(obj.staff)
                GUI_prodsList.set(obj.prods)

                # Clear and refresh indexing.
                tup = getObjListIDs(obj,self.customerIDs,self.staffIDs,self.productIDs)
                self.customerIDs = tup[0]
                self.staffIDs    = tup[1]
                self.productIDs  = tup[2]

                updatePrices(obj)
                GUI_dateTime.set(obj.datetime.strftime(timeForm))
                GUI_prodPrice.set("Price: "+str(obj.total[0]))
                GUI_prodItems.set("Items: "+str(obj.total[1]))
                GUI_obType.set(type)
                
                # format(0.00,".2f")

                # Preemptively blanking/disabling Bill-only items.
                for wid in [dueLabel,dueEntry,ampLabel,ampEntry,ampCheck]:
                    wid.config(state=DISABLED)

                # This will try for Bill attributes.
                # If it fails, it loads default values in.
                try:
                    GUI_dueDate.set(obj.dueDate.strftime(timeForm))
                    GUI_amoPaid.set(format(obj.amountPaid,".2f"))
                    GUI_paid.set(obj.paid)

                    # Those values exist where they're supposed to on a bill.
                    # So, go ahead with unblanking/re-enabling the fields.
                    for wid in [dueLabel,dueEntry,ampLabel,ampEntry,ampCheck]:
                        wid.config(state=NORMAL)
                except:
                    GUI_dueDate.set("N/A")
                    GUI_amoPaid.set("")
                    GUI_paid.set(False)

                # Make our 'current record' outside this function this.
                self.currentRec = obj
                GUI_currentRecVar.set("Viewing: "+str(self.currentRec))

                # Notes and stuff.
                noteText.delete((0.0),END)
                noteText.insert(END,self.currentRec.notes)

                # And a price update, just in case products change.
            else:
                print("Oops. That's not a transaction or bill you gave me.")

        def saveTransaction(obj):
            # Writes your changes to the DB, and to the program.
            # And calculates everything necessary as it goes.
            
            dbCon = sqlite3.connect("./travelAgency.db")
            dbCur = dbCon.cursor()

            timeForm = "%d/%m/%y"
            try:
                date         = GUI_dateTime.get()
                obj.datetime = dt.datetime.strptime(date,timeForm)
            except:
                print("WARNING: Time format not correct on datetime. Skipping.")
                tkinter.messagebox.showwarning("Flying Travel Agency",str(obj)+"'s date created field is incorrectly formatted. Skipping update.")

            # Turn Objects into IDs
            idsToObs      = getIDListObjs(obj,self.customerIDs,self.staffIDs,self.productIDs)
            print(idsToObs)
            obj.customer  = idsToObs[0]
            obj.staff     = idsToObs[1]
            obj.prods     = idsToObs[2]

            # To get products, must put them in a separate variable, and
            # iterate through the products list, matching entries.

            if(checkObject(obj) in ["Bill"]):
                try:
                    ddate          = GUI_dueDate.get()
                    obj.dueDate    = dt.datetime.strptime(ddate,timeForm)
                except:
                    print("WARNING: Time format not correct on due date. Skipping.")
                    tkinter.messagebox.showwarning("Flying Travel Agency",str(obj)+"'s due date field is incorrectly formatted. Skipping update.")
                obj.amountPaid = GUI_amoPaid.get()
                obj.paid       = GUI_paid.get()

            # Check if any changes have been made to the price/prods.
            # And update the notes.
            updatePrices(obj) # This updates/overwrites $obj.total
            obj.notes = updateNotes(obj,noteText)

            # Then refresh the record view.
            GUI_recordList.set(li)
            GUI_currentRecVar.set("Viewing: "+str(self.currentRec))

            # Prepare the SQL for this transaction.
            DTtimeTuple    = obj.datetime.timetuple()

            sql_dt_year  = DTtimeTuple[0]
            sql_dt_month = DTtimeTuple[1]
            sql_dt_day   = DTtimeTuple[2]

            sql_joiner         = "|"
            sql_custs_ids_list = self.customerIDs
            sql_staff_ids_list = self.staffIDs
            sql_prods_ids_list = self.productIDs

            sql_custs_ids_str  = ""
            sql_staff_ids_str  = ""
            sql_prods_ids_str  = ""

            for custs_int in sql_custs_ids_list:
                sql_custs_ids_str += str(custs_int)+sql_joiner
            for staff_int in sql_staff_ids_list:
                sql_staff_ids_str += str(staff_int)+sql_joiner
            for prods_int in sql_prods_ids_list:
                sql_prods_ids_str += str(prods_int)+sql_joiner

            sql_custs_ids_str = str(sql_custs_ids_str.rstrip(sql_joiner))
            sql_staff_ids_str = str(sql_staff_ids_str.rstrip(sql_joiner))
            sql_prods_ids_str = str(sql_prods_ids_str.rstrip(sql_joiner))

            if(checkObject(obj) in ["Bill"]):
                DDtimeTuple  = obj.dueDate.timetuple()
                sql_dd_year  = DDtimeTuple[0]
                sql_dd_month = DDtimeTuple[1]
                sql_dd_day   = DDtimeTuple[2]
                sql_bill     = "TRUE"
                sql_paid     = obj.paid
                sql_ampaid   = obj.amountPaid
            else:
                # Use stub data for 'paid'
                sql_dd_year  = 1970
                sql_dd_month = 1
                sql_dd_day   = 1
                sql_bill     = "FALSE"
                sql_paid     = obj.paid
                sql_ampaid   = obj.amountPaid
            
            # Get Description
            sql_notes = obj.notes

            # Create the SQL Tuple
            sql_tuple = (sql_dt_year,sql_dt_month,sql_dt_day,
                         sql_custs_ids_str,sql_staff_ids_str,sql_prods_ids_str,
                         sql_bill,sql_paid,
                         sql_dd_year,sql_dd_month,sql_dd_day,
                         sql_ampaid,sql_notes,obj.tid)

            # Update SQL database with tuple to pass through it
            dbCur.execute("""UPDATE transactions
            SET datetime_year  = ?, -- 0
                datetime_month = ?, -- 1
                datetime_day   = ?, -- 2
                customer_ids   = ?, -- 3
                staff_ids      = ?, -- 4
                prod_ids       = ?, -- 5
                bill           = ?, -- 6
                paid           = ?, -- 7
                duedate_year   = ?, -- 8
                duedate_month  = ?, -- 9
                duedate_day    = ?, -- 10
                amount_paid    = ?, -- 11
                notes          = ?  -- 12
            WHERE tid = ?           -- 13""",sql_tuple)

            # Provide a message that the operation was successful, one way or the other.
            try:
                tkinter.messagebox.showinfo("Flying Travel Agency",str(obj)+"'s data was updated successfully.")
            except:
                print(str(obj)+" was saved/updated. Showing a message box didn't for some reason though.")
            
            dbCon.commit()
            dbCon.close()

        def newTransaction():
            print("newTransaction: Starting...")
            check = tkinter.messagebox.askquestion("Create New Transaction",
                                                   "Are you sure you want to create a new Transaction?",
                                                   icon = 'question')
            if(check == "yes"):
                print("newTransaction: User said yes.")
                newTransac = None
                
                dbCon = sqlite3.connect("./travelAgency.db")
                dbCur = dbCon.cursor()
                
                print("newTransaction: Transaction or Bill?")
                torb = tkinter.messagebox.askyesnocancel("Transaction or Bill?",
                                                         "Will this new transaction be billable?\n(This cannot be changed once the object is set!)",
                                                         icon="question")
                
                if(torb == True or torb == False):
                    dbCur.execute("SELECT max(tid) FROM transactions")
                    tid_tup = dbCur.fetchone()
                    new_tid = tid_tup[0]+1
                
                if(torb == True):
                    # Billable!
                    print("newTransaction: This is a bill.")
                    newTransac = cl_Orders.Bill()
                    createTransView(newTransac)
                    
                    sql_tuple = (new_tid,"TRUE")
                    dbCur.execute("""
                    INSERT INTO transactions (tid,bill)
                    VALUES (?,?)
                    """,sql_tuple)
                    
                    dbCon.commit()
                    tkinter.messagebox.showinfo("Flying Travel Agency","New Bill was created successfully.")
                elif(torb == False):
                    # Not Billable!
                    print("newTransaction: This is a transaction.")
                    newTransac = cl_Orders.Transaction()
                    createTransView(newTransac)
                    
                    sql_tuple = (new_tid,"FALSE")
                    dbCur.execute("""
                    INSERT INTO transactions (tid,bill)
                    VALUES (?,?)
                    """,sql_tuple)
                    
                    dbCon.commit()
                    dbCon.close()
                    tkinter.messagebox.showinfo("Flying Travel Agency","New Transaction was created successfully.")
                else:
                    # Cancelled.
                    print("newTransaction: User Cancelled.")
            else:
                print("newTransaction: User Cancelled.")
            print("newTransaction: Finished.")
        
        def updatePrices(obj):
            try: obj.getTotalPrices()
            except: print("That's not a transaction/bill, because getTotalPrices() failed. Skipping.")

        def openChangeThings(obj):
            tup = getObjListIDs(obj,self.customerIDs,self.staffIDs,self.productIDs)

            self.changeWin = Toplevel(self.master)
            self.changeApp = ChangeThingsInTransac(self.changeWin,obj=self.currentRec,cil=tup[0],sil=tup[1],pil=tup[2])
            # Make the window non-resizeable and transient.
            self.changeApp.master.resizable(width=False, height=False)
            self.changeApp.master.transient(self.master)
            #self.changeApp.master.bind("<1>",lambda x: createTransView(self.currentRec))
            #self.changeApp.c_back = lambda x: createTransView(self.currentRec)
            #print(self.changeApp.parent.transactionsWindow)
            self.changeApp.parent = self

        def sendEmail(obj,args=[]):
            # obj = the transaction this window manipulates.
            # args = a list which can contain "c" and/or "s"
            # to address Customers and/or Staff.
            print("sendEmail: Starting...")

            check = tkinter.messagebox.askquestion("Send Emails",
                                       "Are you sure you want to send emails out?",
                                       icon = 'question')

            if(len(obj.customer) > 0 and len(obj.staff) > 0 and check == "yes"):
                import smtplib                          # For sending the message
                from email.message import EmailMessage  # For creating the message to send

                # Figure out what type of email to send based on user input.
                sel = GUI_emailType.get()
                ind = emailTypes.index(sel)

                # Important object info brought directly into strings for the email.
                dt = str(obj.datetime.date())
                try: cust = str(obj.customer[0])
                except IndexError: cu = "Sir/Madam"

                try: staf = str(obj.staff[0])
                except IndexError: st = "Travel Agency Staff"

                mailTitle = ""
                mailTexts = ""
                mailSig = "\n\nKind regards,\n-Flying Travel Agency"

                message = EmailMessage()

                '''
                emailTypes = ["Order Receipt","Order Success","Order Fail","Order Cancellation","Billing Success"
                              "Billing Notice","Billing Warning","Billing Cancellation"]
                '''

                # Define message content.
                mailTitle = emailTypes[ind]
                if(ind == 0):
                    mailTexts = "Dear "+cust+"\n\nHere is a billable receipt ("+str(obj)+") for your transaction with us, dated "+dt+" and written by "+staf+"."
                elif(ind == 1):
                    mailTexts = "Dear "+cust+"\n\nYour order ("+str(obj)+") was processed successfully."
                elif(ind == 2):
                    mailTexts = "Dear "+cust+"\n\nYour order ("+str(obj)+") has failed to process correctly. Flying Travel Agency would like to get in touch with you as soon as possible to clarify your financial data with us."
                elif(ind == 3):
                    mailTexts = "Dear "+cust+"\n\nWe are writing to confirm have chosen to cancel your order ("+str(obj)+"). We're sorry to see this come to pass, but we wish for your continued patronage in future."
                elif(ind == 4):
                    mailTexts = "Dear "+cust+"\n\nWe are writing to confirm that you have been successfully billed, and that your holiday awaits you! Please find attached to this email your (imaginary) docket."
                elif(ind == 5):
                    mailTexts = "Dear "+cust+"\n\nNow that your order on "+str(obj)+" has been processed and we're in the process of arranging for your holiday, Flying Travel Agency expects a payment for their service within fourteen business days."
                elif(ind == 6):
                    mailTexts = "Dear "+cust+"\n\nYou have three days left to pay Flying Travel Agency for their services on "+str(obj)+". Failure to do so may result in your holiday being dropped."
                    mailSig = "\n\nRegards,\n-Flying Travel Agency"
                elif(ind == 7):
                    mailTexts = "Dear "+cust+"\n\nYour billing for "+str(obj)+" has been cancelled, and your holiday has been dropped."
                    mailSig = "\n\nRegards,\n-Flying Travel Agency"
                elif(ind == 8):
                    mailTexts = "Dear "+cust+"\n\nYou've done something so horrible towards the staff or office of Flying Travel Agency that you're now forbidden from using our services to create holidays or entering our premises."
                    mailSig = "\n\nContact us again and we're pressing charges against you.\n\nHave a nice life,\n-Flying Travel Agency"

                custMails  = []
                staffMails = []
                allMails   = []

                for i in obj.customer:
                    custMails.append(i.contacts["email"])
                    allMails.append(i.contacts["email"])
                for i in obj.staff:
                    staffMails.append(i.contacts["email"])
                    allMails.append(i.contacts["email"])

                message.set_content(mailTexts+mailSig)
                message["Subject"] = "Flying Travel Agency - "+mailTitle+" re: "+str(obj)
                message["From"]    = "mail@travelagency.com.au"

                # Send Email.
                if("c" in args and "s" in args):
                    print("sendEmail: Sending to customers and staff...")
                    message["To"]  = str(allMails)
                elif("c" in args):
                    print("sendEmail: Sending to customers...")
                    message["To"]  = str(custMails)
                elif("s" in args):
                    print("sendEmail: Sending to staff...")
                    message["To"]  = str(staffMails)

                print(message)
                return message

                '''
                # Spin up and launch smtp
                # Can't actually do this due to security
                s = smtplib.SMTP('localhost')
                s.send_message(message)
                s.quit()
                '''
            elif(len(obj.customer) > 0 and len(obj.staff) > 0 and check == "no"):
                print("sendEmail: Operation cancelled.")
            else:
                print("sendEmail: Not enough customers or staff to send email.")
                tkinter.messagebox.showwarning("Flying Travel Agency","Sending emails requires there to be at least one customer, and one staff member involved in the transaction.\nPlease review your Transaction Info and try again.")

            print("sendEmail: Finished.")

        # Run transaction view function
        # on current record grabbed earlier.
        createTransView(self.currentRec)

# Class for changing things within a transaction's lists.
#########################################################
class ChangeThingsInTransac(Window):
    def __init__(self,master=None,obj=None,cil=[],sil=[],pil=[]):
        Window.__init__(self,master)
        self.master = master
        self.parent = None
        self.c_back = None
        self.object = obj
        self.custs  = cil
        self.staff  = sil
        self.prods  = pil

        # Populate IDs if they get passed through blank for some reason.
        # Or not. Generally we expect this stuff to have its things in order.

        self.thingWindow()

    def thingWindow(self):
        # Display people objs
        titleText = "Flying Travel Agency - Modifying Transaction Lists"
        outerPad = 4
        innerPad = 2

        # Define window title.
        self.master.title(titleText)
        # Pre-pack the 'base' of the database.
        self.pack(fill="y",expand=1,padx=outerPad,pady=outerPad)

        # Control Variables for this Window
        ###################################
        GUI_curRec   = StringVar(name="Current Record")
        GUI_trCusts  = StringVar(name="Transaction Customers")
        GUI_trStaff  = StringVar(name="Transaction Staff")
        GUI_trProds  = StringVar(name="Transaction Products")
        GUI_allCusts = StringVar(name="All Customers")
        GUI_allStaff = StringVar(name="All Staff")
        GUI_allProds = StringVar(name="All Products")

        # Simple function to make updating control vars easier.
        def updateControlVars():
            GUI_curRec.set("Modifying: "+str(self.object))
            GUI_allCusts.set(db.getList("customerList"))
            GUI_allStaff.set(db.getList("staffList"))
            GUI_allProds.set(db.getList("prodList"))
            GUI_trCusts.set(self.object.customer)
            GUI_trStaff.set(self.object.staff)
            GUI_trProds.set(self.object.prods)

        # So naturally we call it immediately after its written.
        updateControlVars()

        # Frames and Tabs for this Window
        #################################
        # Images for tabs
        custsIcon = PhotoImage(file=r"./img/icon_Customers.png")
        staffIcon = PhotoImage(file=r"./img/icon_Staff.png")
        prodsIcon = PhotoImage(file=r"./img/icon_Products.png")

        # Bit at the top of the window.
        topLabel  = Label(self,textvariable=GUI_curRec)
        topLabel.pack(side=TOP)

        # Tabs themselves.
        tabControl  = ttk.Notebook(self)
        tabCusts    = Frame(tabControl)  # Goes in $tabControl
        tabStaff    = Frame(tabControl)  # Ditto...
        tabProds    = Frame(tabControl)
        tabControl.add(tabCusts,text="Customers",image=custsIcon,compound=LEFT)
        tabControl.add(tabStaff,text="Staff",image=staffIcon,compound=LEFT)
        tabControl.add(tabProds,text="Products",image=prodsIcon,compound=LEFT)

        # Necessary step to prevent garbage control from deleting the images prematurely.
        tabControl.custsIcon = custsIcon
        tabControl.staffIcon = staffIcon
        tabControl.prodsIcon = prodsIcon
        tabControl.pack(side=TOP,padx=outerPad,pady=outerPad)

        # Frames for Customer Tab
        custs_allFrame     = LabelFrame(tabCusts,text="All Customers")
        custs_transFrame   = LabelFrame(tabCusts,text="Customers in Transaction")
        custs_allInFrame   = Frame(custs_allFrame)
        custs_transInFrame = Frame(custs_transFrame)
        # Frames for Staff Tab
        staff_allFrame     = LabelFrame(tabStaff,text="All Staff")
        staff_transFrame   = LabelFrame(tabStaff,text="Staff in Transaction")
        staff_allInFrame   = Frame(staff_allFrame)
        staff_transInFrame = Frame(staff_transFrame)
        # Frames for Products Tab
        prods_allFrame     = LabelFrame(tabProds,text="All Products")
        prods_transFrame   = LabelFrame(tabProds,text="Products in Transaction")
        prods_allInFrame   = Frame(prods_allFrame)
        prods_transInFrame = Frame(prods_transFrame)

        # Packing Frames, external and internal...
        allFrames = [custs_allFrame,custs_transFrame,
                     staff_allFrame,staff_transFrame,
                     prods_allFrame,prods_transFrame]

        for fo in allFrames:
            fo.pack(side=LEFT,fill="x",padx=innerPad,pady=innerPad)

        innerFrames = [custs_allInFrame,custs_transInFrame,
                       staff_allInFrame,staff_transInFrame,
                       prods_allInFrame,prods_transInFrame]

        for fi in innerFrames:
            fi.pack(side=TOP,fill="x",padx=innerPad,pady=innerPad)

        # Widgets within Frames
        #######################
        # Customer Tab Widgets
        # Starting with scrolling bars.
        custsScroll_all   = Scrollbar(custs_allInFrame)
        custsScroll_tra   = Scrollbar(custs_transInFrame)
        staffScroll_all   = Scrollbar(staff_allInFrame)
        staffScroll_tra   = Scrollbar(staff_transInFrame)
        prodsScroll_all   = Scrollbar(prods_allInFrame)
        prodsScroll_tra   = Scrollbar(prods_transInFrame)

        # Creating Datalists
        custsList_all     = Listbox(custs_allInFrame,height=16,width=30,listvariable=GUI_allCusts,
                                    selectmode="SINGLE",activestyle="dotbox",yscrollcommand=custsScroll_all.set)
        custsList_transac = Listbox(custs_transInFrame,height=16,width=30,listvariable=GUI_trCusts,
                                    selectmode="SINGLE",activestyle="dotbox",yscrollcommand=custsScroll_tra.set)
        staffList_all     = Listbox(staff_allInFrame,height=16,width=30,listvariable=GUI_allStaff,
                                    selectmode="SINGLE",activestyle="dotbox",yscrollcommand=staffScroll_all.set)
        staffList_transac = Listbox(staff_transInFrame,height=16,width=30,listvariable=GUI_trStaff,
                                    selectmode="SINGLE",activestyle="dotbox",yscrollcommand=staffScroll_tra.set)
        prodsList_all     = Listbox(prods_allInFrame,height=16,width=30,listvariable=GUI_allProds,
                                    selectmode="SINGLE",activestyle="dotbox",yscrollcommand=prodsScroll_all.set)
        prodsList_transac = Listbox(prods_transInFrame,height=16,width=30,listvariable=GUI_trProds,
                                    selectmode="SINGLE",activestyle="dotbox",yscrollcommand=prodsScroll_tra.set)

        # Configuring Scrolls
        custsScroll_all.config(command=custsList_all.yview)
        custsScroll_tra.config(command=custsList_transac.yview)
        staffScroll_all.config(command=staffList_all.yview)
        staffScroll_tra.config(command=staffList_transac.yview)
        prodsScroll_all.config(command=prodsList_all.yview)
        prodsScroll_tra.config(command=prodsList_transac.yview)

        # Creating Buttons
        custs_addButton   = Button(custs_allFrame,text="Add Customer",command=lambda:addToList("custs"))
        custs_remButton   = Button(custs_transFrame,text="Remove Customer",command=lambda:remFromList("custs"))
        staff_addButton   = Button(staff_allFrame,text="Add Staff",command=lambda:addToList("staff"))
        staff_remButton   = Button(staff_transFrame,text="Remove Staff",command=lambda:remFromList("staff"))
        prods_addButton   = Button(prods_allFrame,text="Add Product",command=lambda:addToList("prods"))
        prods_remButton   = Button(prods_transFrame,text="Remove Product",command=lambda:remFromList("prods"))

        # Packing everything together.
        for butts in [custs_addButton,custs_remButton,staff_addButton,staff_remButton,prods_addButton,prods_remButton]:
            butts.pack(side="bottom",fill="both",padx=innerPad,pady=innerPad)

        for scroll in [custsScroll_all,custsScroll_tra,staffScroll_all,staffScroll_tra,prodsScroll_all,prodsScroll_tra]:
            scroll.pack(side=RIGHT,fill="y")

        for widge_c in [custsList_all,custsList_transac]:
            widge_c.pack(padx=innerPad,pady=innerPad)

        for widge_s in [staffList_all,staffList_transac]:
            widge_s.pack(padx=innerPad,pady=innerPad)

        for widge_p in [prodsList_all,prodsList_transac]:
            widge_p.pack(padx=innerPad,pady=innerPad)

        '''
        print("Opening Changing Things window!")
        print(self.object)

        print(self.object.customer)
        print(self.object.staff)
        print(self.object.prods)

        print(self.custs)
        print(self.staff)
        print(self.prods)
        '''

        # Functions to manipulate data in this context.
        ###############################################

        def addToList(type):
            # Setting variables before we get started.
            addList = None
            traList = None  # Might not need this actually.

            # Step 1: Identify which list is being added to.
            if(type == "custs"):
                addList = custsList_all
                traList = custsList_transac
            elif(type == "staff"):
                addList = staffList_all
                traList = staffList_transac
            elif(type == "prods"):
                addList = prodsList_all
                traList = prodsList_transac
            else:
                print("Specify type from 'custs', 'staff', or 'prods' or don't call this function!")

            # Step 2: Add to that list, taking the option we've chosen from the all options list.
            if(type in ["custs","staff","prods"]):
                # Get the selection of the necessary list.
                lObj = False
                sel = getCurSel(addList)

                if(sel == ()):
                    # Tuple returned empty because no selection was made.
                    # So, default to first obj. in list to prevent meltdown.
                    sel = (0,0)

                if(type == "custs"):
                    #2A: Adding a new customer.
                    lObj = db.getObjFromList("customerList",sel[0])
                elif(type == "staff"):
                    #2B: Adding a new staff member.
                    lObj = db.getObjFromList("staffList",sel[0])
                elif(type == "prods"):
                    #2C: Adding a new product.
                    lObj = db.getObjFromList("prodList",sel[0])

                if(lObj != False):
                    # Step 3: We have an object. It has a list to go to... Add this new object to the relevant list.
                    # Before we get started though, let's make sure the object isn't already on the list.

                    objType = checkObject(lObj)
                    if(objType == "Customer"):
                        #3A: Customer
                        if(lObj not in self.object.customer):
                            self.object.customer.append(lObj)
                        else:
                            tkinter.messagebox.showwarning("Flying Travel Agency",str(lObj)+" is already involved in this transaction.")
                    elif(objType == "Staff"):
                        #3B: Staff
                        if(lObj not in self.object.staff):
                            self.object.staff.append(lObj)
                        else:
                            tkinter.messagebox.showwarning("Flying Travel Agency",str(lObj)+" is already involved in this transaction.")
                    elif(objType in ["Product","Hotel","Flight","Insurance","Activity","Vehicle"]):
                        #3C: Product
                        if(lObj not in self.object.prods):
                            self.object.prods.append(lObj)
                        else:
                            tkinter.messagebox.showwarning("Flying Travel Agency",str(lObj)+" is already a product in this transaction.")
                else:
                    print("Getting Object from List returned False. Winding down.")
            else:
                print("Skipping operation! Good day, sir!")

            # Try updating our parent window to reflect changes made here.
            #self.parent.transactionsWindow(db.getList("transacList"),"transacList").createTransView(self.parent.currentRec)
            # Even so, we'll give our control vars a quick scan after this.
            updateControlVars()
            #print(self.c_back)
            #self.c_back

        def remFromList(type):
            # Same as above but in reverse.
            remList = None

            # Step 1: Identify which list is being removed from.
            if(type == "custs"):
                remList = custsList_transac
            elif(type == "staff"):
                remList = staffList_transac
            elif(type == "prods"):
                remList = prodsList_transac
            else:
                print("Specify type from 'custs', 'staff', or 'prods'")

            if(type != ""):
                sel    = getCurSel(remList)
                remInd = sel[0]
                rObj   = None
                failed = False

                try:
                    # Step 2: Pick the object that needs to be removed from the list.
                    if(type == "custs"):
                        # 2A: Pick a customer.
                        rObj = self.object.customer[remInd]
                    elif(type == "staff"):
                        # 2B: Pick a staff member.
                        rObj = self.object.staff[remInd]
                    elif(type == "prods"):
                        # 2C: Pick a product.
                        rObj = self.object.prods[remInd]
                    else:
                        print("Specify type from 'custs', 'staff', or 'prods', please.")
                except IndexError:
                    print("remFromList: Out of range/record not selected.")
                    failed = True

                if(failed == False):
                    # Step 3: Remove that object from the object's list.
                    if(type == "custs"):
                        # 3A: Remove a customer.
                        self.object.customer.remove(rObj)
                    elif(type == "staff"):
                        # 3B: Remove a staff member.
                        self.object.staff.remove(rObj)
                    elif(type == "prods"):
                        # 3C: Remove a product.
                        self.object.prods.remove(rObj)
                else:
                    print("remFromList: Task failed due to index error in step 2.")
            else:
                print("Skipping operation! Good day, sir!")

            # Then update the interface accordingly.
            self.parent.transactionsWindow
            updateControlVars()