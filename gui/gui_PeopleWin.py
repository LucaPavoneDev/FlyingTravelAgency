from tkinter import *
# To get pop-up messages you gotta be a bit wonky. Oh well.
import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox

from cl_Interface import Window
from cl_Data import database as db
from gui.gui_Helpers import *
import cl_People
import datetime as dt
import sqlite3

# Class for changing people lists (customers and staff)
#######################################################
class PeopleWindow(Window):
    def __init__(self,master=None,listName=""):
        Window.__init__(self,master)
        self.master   = master
        self.name     = ""                      # User friendly variable, set below before the window runs.
        self.listName = listName                # Not a User-Friendly variable. Programming name of incoming list.
        self.list     = db.getList(listName)
        self.person   = None

        devList  = db.getAllLists()
        nameList = db.getListNames()
        i = devList.index(self.listName)
        self.name = nameList[i]

        # This window can be summoned for either Customers, or Staff.
        # It'll load them in. I'll do the bolts and bananas on this.
        if(listName in ["customerList","staffList"]):
            self.peopleWindow()
        else:
            print("Hey a sec, this isn't meant to happen.\nPlease use this with \"customerList\" or \"staffList\" please. :(")

    def peopleWindow(self):
        # Main Window Setup/Pre-Pack
        self.master.title("Flying Travel Agency - People Management")
        outerPad = 4
        innerPad = 2
        self.pack(fill="both",expand=1,padx=outerPad,pady=outerPad)

        # GUI control variables and setter function
        ###########################################
        # List of people, user-friendly name of list,
        # and user-friendly name of currently selected person.
        GUI_people   = StringVar()
        GUI_listname = StringVar()
        GUI_person   = StringVar()

        # Person Details
        GUI_p_fname  = StringVar()
        GUI_p_lname  = StringVar()
        GUI_p_desc   = StringVar()

        # Address Info
        GUI_p_addr_zip        = StringVar()
        GUI_p_addr_state      = StringVar()
        GUI_p_addr_city       = StringVar()
        GUI_p_addr_streetName = StringVar()
        GUI_p_addr_streetNo   = StringVar()
        GUI_p_addr_unitNo     = StringVar()

        # Contact Info
        GUI_p_cont_email      = StringVar()
        GUI_p_cont_phoneH     = StringVar()
        GUI_p_cont_phoneM     = StringVar()

        #GUI_p_conts = StringVar()
        #UI_p_addrs = StringVar()

        def updateControlVars():
            # Variable gathering
            try:
                persName = str(self.person.fname)+" "+str(self.person.lname)
            except AttributeError:
                # Blank it when something goes wrong because self.person isn't set/isn't a person at all.
                print("updateControlVars: getting persName failed. Blanking.")
                persName = ""

            # Person's details
            try: GUI_p_fname.set(self.person.fname)
            except AttributeError: print("Warning: GUI_p_fname not set.")
            try: GUI_p_lname.set(self.person.lname)
            except AttributeError: print("Warning: GUI_p_lname not set.")
            try: GUI_p_desc.set(self.person.desc)
            except AttributeError: print("Warning: GUI_p_desc not set.")

            # Person's Address
            try: GUI_p_addr_zip.set(self.person.address["zipcode"])
            except AttributeError: print("Warning: GUI_p_addr_zip not set.")
            try: GUI_p_addr_state.set(self.person.address["state"])
            except AttributeError: print("Warning: GUI_p_addr_state not set.")
            try: GUI_p_addr_city.set(self.person.address["city"])
            except AttributeError: print("Warning: GUI_p_addr_city not set.")
            try: GUI_p_addr_streetName.set(self.person.address["streetName"])
            except AttributeError: print("Warning: GUI_p_addr_streetName not set.")
            try: GUI_p_addr_streetNo.set(self.person.address["streetNumber"])
            except AttributeError: print("Warning: GUI_p_addr_streetNo not set.")
            try: GUI_p_addr_unitNo.set(self.person.address["unitNumber"])
            except AttributeError: print("Warning: GUI_p_addr_unitNo not set.")

            # Person's Contacts
            try: GUI_p_cont_email.set(self.person.contacts["email"])
            except AttributeError: print("Warning: GUI_p_cont_email not set.")
            try: GUI_p_cont_phoneH.set(self.person.contacts["homePhone"])
            except AttributeError: print("Warning: GUI_p_cont_phoneH not set.")
            try: GUI_p_cont_phoneM.set(self.person.contacts["mobilePhone"])
            except AttributeError: print("Warning: GUI_p_cont_phoneM not set.")

            # Old versions. Unfortunately you can't load and iterate lists this way.
            # But these will be preserved for learnin' purposes.
            #try: GUI_p_conts.set(self.person.contacts)
            #except AttributeError: print("Warning: GUI_p_conts not set.")
            #try: GUI_p_addrs.set(self.person.address)
            #except AttributeError: print("Warning: GUI_p_addrs not set.")

            # Variable setting
            GUI_people.set(self.list)
            GUI_listname.set("Currently Viewing "+self.name+": "+persName)
            GUI_person.set(persName)

        viewList = Label(self,textvariable=GUI_listname)
        viewList.pack(side=TOP)

        # Set up main frames where everything will go.
        ##############################################
        leftFrame  = Frame(self)
        rightFrame = Frame(self)
        bottomFrame= Frame(self)
        bottomFrame.pack(side=BOTTOM,padx=outerPad,pady=outerPad,fill="x")
        leftFrame.pack(side=LEFT,padx=outerPad,pady=outerPad,fill="y")
        rightFrame.pack(side=RIGHT,padx=outerPad,pady=outerPad,fill="y")

        # Images for tabs
        detailsIcon = PhotoImage(file=r"./img/icon_perDetails.png")
        contactIcon = PhotoImage(file=r"./img/icon_perContacts.png")
        addressIcon = PhotoImage(file=r"./img/icon_perAddress.png")

        # Creating the tabs and tab controls for the right-side frame.
        # (Adding widgets to these comes later)
        #########################################
        tabControl = ttk.Notebook(rightFrame)
        tabDetails = Frame(tabControl)
        tabContact = Frame(tabControl)
        tabAddress = Frame(tabControl)
        # Adding the tab frames to the tab control.
        tabControl.add(tabDetails,text="Details",image=detailsIcon,compound=LEFT)
        tabControl.add(tabContact,text="Contacts",image=contactIcon,compound=LEFT)
        tabControl.add(tabAddress,text="Address",image=addressIcon,compound=LEFT)
        # Garbage collection prevention for tab images, and packing
        tabControl.detailsIcon = detailsIcon
        tabControl.contactIcon = contactIcon
        tabControl.addressIcon = addressIcon
        tabControl.pack(side=TOP,padx=outerPad,pady=outerPad)

        # Adding Widgets to the left-side frame.
        ########################################
        # Records view and scrollbar.
        perScroll = Scrollbar(leftFrame)
        perList   = Listbox(leftFrame,height=12,width=32,listvariable=GUI_people,
                            selectmode="SINGLE",activestyle="dotbox",yscrollcommand=perScroll.set)
        perScroll.config(command=perList.yview)
        perScroll.pack(side=RIGHT,fill="y")
        perList.bind("<Double-1>",lambda x: loadPerson(getRecord(self.list,getCurSel(perList),perList)))
        perList.pack(side=RIGHT)

        # Adding Widgets to the bottom-side frame.
        ##########################################
        # This is where the buttons live.
        firstButton  = Button(bottomFrame,text="First",command=lambda: loadPerson(getRecord(self.list,(0,0),perList)))
        prevButton   = Button(bottomFrame,text="Previous",command=lambda: loadPerson(getRecord(self.list,getCurSel(perList),perList,offset=-1)))
        loadButton   = Button(bottomFrame,text="Select",command=lambda: loadPerson(getRecord(self.list,getCurSel(perList),perList)))
        nextButton   = Button(bottomFrame,text="Next",command=lambda: loadPerson(getRecord(self.list,getCurSel(perList),perList,offset=1)))
        lastButton   = Button(bottomFrame,text="Last",command=lambda: loadPerson(getRecord(self.list,(perList.size()-1,0),perList)))

        newButton    = Button(bottomFrame,text="New Person", command=lambda: newPerson())
        updateButton = Button(bottomFrame,text="Update Person",command=lambda: savePerson(self.person))

        leftButtons = [firstButton,prevButton,loadButton,nextButton,lastButton]
        rightButtons = [updateButton,newButton]

        for bl in leftButtons:
            bl.pack(side=LEFT,fill="x")
        for br in rightButtons:
            br.pack(side=RIGHT,fill="x")

        # Right Side Frame Widgets
        ##########################
        # Details Tab
        lab_fname = Label(tabDetails,text="First Name:",width=12,anchor="w")
        lab_lname = Label(tabDetails,text="Last Name:",width=12,anchor="w")
        lab_desc  = Label(tabDetails,text="Description/Notes")
        ent_fname = Entry(tabDetails,textvariable=GUI_p_fname,width=20)
        ent_lname = Entry(tabDetails,textvariable=GUI_p_lname,width=20)
        ent_desc  = Text(tabDetails,height=5,wrap=WORD,width=20)
        #ent_scroll= Scrollbar(tabDetails,jump=1)
        #ent_scroll.config(command=ent_desc.yview)

        lab_fname.grid(row=0,column=0,sticky="w",padx=innerPad,pady=innerPad)
        lab_lname.grid(row=1,column=0,sticky="w",padx=innerPad,pady=innerPad)
        lab_desc.grid(row=2,column=0,columnspan=3,sticky="s",padx=innerPad,pady=innerPad)
        ent_fname.grid(row=0,column=2,sticky="e",padx=innerPad,pady=innerPad)
        ent_lname.grid(row=1,column=2,sticky="e",padx=innerPad,pady=innerPad)
        ent_desc.grid(row=3,column=0,columnspan=3,sticky="nesw",padx=innerPad,pady=innerPad)
        #ent_scroll.grid(row=3,column=0,sticky="w")

        # Contacts Tab
        lab_cont_email  = Label(tabContact,text="Email:",width=12,anchor="w")
        lab_cont_hphone = Label(tabContact,text="Home Phone:",width=12,anchor="w")
        lab_cont_mphone = Label(tabContact,text="Mobile Phone:",width=12,anchor="w")
        ent_cont_email  = Entry(tabContact,textvariable=GUI_p_cont_email,width=20)
        ent_cont_hphone = Entry(tabContact,textvariable=GUI_p_cont_phoneH,width=20)
        ent_cont_mphone = Entry(tabContact,textvariable=GUI_p_cont_phoneM,width=20)

        lab_cont_email.grid(row=0,column=0,sticky="w",padx=innerPad,pady=innerPad)
        lab_cont_hphone.grid(row=1,column=0,sticky="w",padx=innerPad,pady=innerPad)
        lab_cont_mphone.grid(row=2,column=0,sticky="w",padx=innerPad,pady=innerPad)

        ent_cont_email.grid(row=0,column=2,sticky="e",padx=innerPad,pady=innerPad)
        ent_cont_hphone.grid(row=1,column=2,sticky="e",padx=innerPad,pady=innerPad)
        ent_cont_mphone.grid(row=2,column=2,sticky="e",padx=innerPad,pady=innerPad)

        # Address Tab
        lab_addr_zip        = Label(tabAddress,text="Zipcode:",width=12,anchor="w")
        lab_addr_state      = Label(tabAddress,text="State:",width=12,anchor="w")
        lab_addr_city       = Label(tabAddress,text="City:",width=12,anchor="w")
        lab_addr_streetName = Label(tabAddress,text="Street Name:",width=12,anchor="w")
        lab_addr_streetNo   = Label(tabAddress,text="Street Number:",width=12,anchor="w")
        lab_addr_unitNo     = Label(tabAddress,text="Unit Number:",width=12,anchor="w")
        ent_addr_zip        = Entry(tabAddress,textvariable=GUI_p_addr_zip,width=20)
        ent_addr_state      = Entry(tabAddress,textvariable=GUI_p_addr_state,width=20)
        ent_addr_city       = Entry(tabAddress,textvariable=GUI_p_addr_city,width=20)
        ent_addr_streetName = Entry(tabAddress,textvariable=GUI_p_addr_streetName,width=20)
        ent_addr_streetNo   = Entry(tabAddress,textvariable=GUI_p_addr_streetNo,width=20)
        ent_addr_unitNo     = Entry(tabAddress,textvariable=GUI_p_addr_unitNo,width=20)

        lab_addr_zip.grid(row=0,column=0,sticky="w",padx=innerPad,pady=innerPad)
        lab_addr_state.grid(row=1,column=0,sticky="w",padx=innerPad,pady=innerPad)
        lab_addr_city.grid(row=2,column=0,sticky="w",padx=innerPad,pady=innerPad)
        lab_addr_streetName.grid(row=3,column=0,sticky="w",padx=innerPad,pady=innerPad)
        lab_addr_streetNo.grid(row=4,column=0,sticky="w",padx=innerPad,pady=innerPad)
        lab_addr_unitNo.grid(row=5,column=0,sticky="w",padx=innerPad,pady=innerPad)

        ent_addr_zip.grid(row=0,column=2,sticky="e",padx=innerPad,pady=innerPad)
        ent_addr_state.grid(row=1,column=2,sticky="e",padx=innerPad,pady=innerPad)
        ent_addr_city.grid(row=2,column=2,sticky="e",padx=innerPad,pady=innerPad)
        ent_addr_streetName.grid(row=3,column=2,sticky="e",padx=innerPad,pady=innerPad)
        ent_addr_streetNo.grid(row=4,column=2,sticky="e",padx=innerPad,pady=innerPad)
        ent_addr_unitNo.grid(row=5,column=2,sticky="e",padx=innerPad,pady=innerPad)

        # Helper functions
        ##################
        # And GUI vars?

        def getDesc(n=None):
            # Gets a dump of text from a given Text widget.
            try:
                return n.get((0.0),"end-1c")
            except:
                print("That wasn't a Text widget, fool!")

        # Person loading.
        def loadPerson(obj=self.person):
            print("loadPerson: Commencing.")
            self.person = obj
            if(checkObject(obj) in ["Customer","Staff"]):
                # The object given is a customer/staff. Go for it.
                print("loadPerson: Succeeded. Updating control vars.")
                ent_desc.delete((0.0),END)
                if(ent_desc != None):
                    ent_desc.insert(END,str(obj.desc))
                updateControlVars()
            else:
                # The object given is not a customer or staff.
                print("loadPerson: Failed. Given object is not a customer or staff.")

        def savePerson(obj=self.person):
            # Iterate through the various Control Vars, try and update accordingly.
            print("savePerson: Commencing.")
            
            dbCon = sqlite3.connect("./travelAgency.db")
            dbCur = dbCon.cursor()
            
            if(checkObject(obj) in ["Customer","Staff"]):
                obj.fname = GUI_p_fname.get()
                obj.lname = GUI_p_lname.get()
                obj.desc  = getDesc(ent_desc)

                obj.contacts["email"]       = GUI_p_cont_email.get()
                obj.contacts["homePhone"]   = GUI_p_cont_phoneH.get()
                obj.contacts["mobilePhone"] = GUI_p_cont_phoneM.get()
                obj.address["zipcode"]      = GUI_p_addr_zip.get()
                obj.address["state"]        = GUI_p_addr_state.get()
                obj.address["city"]         = GUI_p_addr_city.get()
                obj.address["streetName"]   = GUI_p_addr_streetName.get()
                obj.address["streetNumber"] = GUI_p_addr_streetNo.get()
                obj.address["unitNumber"]   = GUI_p_addr_unitNo.get()

                sql_tuple = (obj.fname,obj.lname,        # 0, 1
                             obj.desc,                   # 2
                             obj.contacts["email"],      # 3
                             obj.contacts["homePhone"],  # 4
                             obj.contacts["mobilePhone"],# 5
                             obj.address["zipcode"],     # 6
                             obj.address["state"],       # 7
                             obj.address["city"],        # 8
                             obj.address["streetName"],  # 9
                             obj.address["streetNumber"],# 10
                             obj.address["unitNumber"],  # 11
                             obj.id)                     # 12
                print(sql_tuple)

                if(checkObject(obj) in ["Customer"]):
                    dbCur.execute(
                    """UPDATE customers
                    SET fname        = ?, -- 0
                        lname        = ?, -- 1
                        desc         = ?, -- 2
                        email        = ?, -- 3
                        homePhone    = ?, -- 4
                        mobilePhone  = ?, -- 5
                        zipcode      = ?, -- 6
                        state        = ?, -- 7
                        city         = ?, -- 8
                        streetName   = ?, -- 9
                        streetNumber = ?, -- 10
                        unitNumber   = ?  -- 11
                    WHERE id = ?          -- 12
                    """,sql_tuple)
                elif(checkObject(obj) in ["Staff"]):
                    dbCur.execute(
                    """UPDATE staff
                    SET fname        = ?, -- 0
                        lname        = ?, -- 1
                        desc         = ?, -- 2
                        email        = ?, -- 3
                        homePhone    = ?, -- 4
                        mobilePhone  = ?, -- 5
                        zipcode      = ?, -- 6
                        state        = ?, -- 7
                        city         = ?, -- 8
                        streetName   = ?, -- 9
                        streetNumber = ?, -- 10
                        unitNumber   = ?  -- 11
                    WHERE id = ?          -- 12
                    """,sql_tuple)

                print("savePerson: Succeeded. Updating control vars.")
                updateControlVars()
                tkinter.messagebox.showinfo("Flying Travel Agency",str(obj)+"'s data was updated successfully.")
            else:
                print("savePerson: Failed. Incoming object not Customer or Staff.")
                tkinter.messagebox.showwarning("Flying Travel Agency",str(obj)+"'s data wasn't saved.")
            
            dbCon.commit()
            dbCon.close()

        def newPerson():
            check = tkinter.messagebox.askquestion("Create New Person",
                                                   "Are you sure you want to create a new person for "+str(self.name)+"?",
                                                   icon = 'question')
            if(check == "yes"):
                dbCon = sqlite3.connect("./travelAgency.db")
                dbCur = dbCon.cursor()
                
                # User is adding a new person.
                np = None
                
                if(self.listName == "customerList"):
                    # Create new customer object in program
                    np = cl_People.Customer("New","Customer")

                    # Create new SQL entry for new customer.
                    # First though, grab the highest ID from customers.
                    dbCur.execute("SELECT max(id) FROM customers")
                    id_tup = dbCur.fetchone()
                    id = id_tup[0]

                    # Set up SQL tuple.
                    sql_tuple = (id+1,"New","Customer")

                    # Execute SQL statement.
                    dbCur.execute("""
                    INSERT INTO customers (id,fname,lname)
                    VALUES (?,?,?)""",sql_tuple)
                    
                    dbCon.commit()
                elif(self.listName == "staffList"):
                    # Create new staff object in program
                    np = cl_People.Staff("New","Staff")

                    # Create new SQL entry for new staff.
                    # First though, grab the highest ID from staff.
                    dbCur.execute("SELECT max(id) FROM staff")
                    id_tup = dbCur.fetchone()
                    id = id_tup[0]

                    # Set up the SQL tuple.
                    sql_tuple = (id+1,"New","Staff")

                    # Execute SQL statement.
                    dbCur.execute("""
                    INSERT INTO staff (id,fname,lname)
                    VALUES (?,?,?)""",sql_tuple)
                    
                    dbCon.commit()
                if(np != None):
                    print("newPerson: New person successfully appended to list.")
                else:
                    print("newPerson: Couldn't identify where new person needed to go.")

                updateControlVars()
                self.person = getRecord(self.list,(perList.size()-1,0),perList)
                
                dbCon.commit()
                dbCon.close()
            else:
                # User doesn't want to add a new person.
                print("newPerson: User cancelled operation.")
                pass

        # Load last record in list.
        self.person = getRecord(self.list,(perList.size()-1,0),perList)
        loadPerson(self.person)