from tkinter import *
# To get pop-up messages you gotta be a bit wonky. Oh well.
import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox

from cl_Interface import Window
from cl_Data import database as db
from cl_Products import Vehicle
from cl_Transport import Car, Bike
import datetime as dt
import sqlite3
from gui.gui_Helpers import *

#############################################################################
## Notice: This GUI module was adapted/integrated with code by Aaron Chan. ##
##             So shout-outs to him, as he is a cool guy.                  ##
##  PS: I mean the Aaron Chan from Melbourne, not the one from Singapore.  ##
#############################################################################

class VehicleCreator(Window):
    def __init__(self,master=None):
        Window.__init__(self,master)
        #self.allVehicles  = db.getList("vehicleList")
        # Iterable lists for options. Subject to change depending on Depot/Vendor.
        self.depots      = db.getList("transpoList")
        self.depotIndex  = 0    # For choosing depots.
        self.depotObj    = self.depots[self.depotIndex] # First depot in list pre-loaded.
        self.company     = self.depotObj.transporter
        self.cars        = []   # Filled in as the user picks a depot.
        self.bikes       = []   # And whether or not they want a car or a bike.
        self.drives      = []   # Ditto above.
        self.gears       = []   # And double ditto.

        # User choices with which to make a vehicle.
        self.carOrBike   = 0    # 0 = Car, 1 = Bike
        self.chosenModel = None # Index for Model Object
        self.chosenDrive = None # Index for Drive Object
        self.chosenGears = None # Index for Gears Object
        self.price       = 0.0  # Float to hold the price for the vehicle.
                                # Determined once model/depot is selected.
        self.newName     = ""   # Name
        self.newDesc     = ""   # Description

        # Image Directory + Icons and Images
        self.imgDir      = "./img/vehicleCreator/"
        self.icons       = {"Car":"icon_Car.png",
                            "Bike":"icon_Bike.png",
                            "Manual":"icon_Gears.png",
                            "Automatic":"icon_Drive.png",
                            "Wheel":"icon_Wheel.png"}
        self.vehicleCreatorControl()

    def vehicleCreatorControl(self):
        # The Essentials
        ################
        outPad = 4
        inPad  = 2

        self.master.title("Flying Travel Agency - Vehicle Creator")
        self.pack(fill="both",padx=outPad,pady=outPad)

        # Main Frames
        #############
        allFrames  = Frame(self)
        allFrames.pack(fill="both",expand=1)

        imageFrame   = LabelFrame(allFrames,text="Your Vehicle",width=600)    # Shows current choices/images/eye candy for user.
        depotFrame   = LabelFrame(allFrames,text="Depot",width=200)           # Choose a vendor/depot to make from
        corbFrame    = LabelFrame(allFrames,text="Car/Bike",width=200)        # Choose Car/Bike checkboxes (corb = "Car or Bike?")
        modelFrame   = LabelFrame(allFrames,text="Model",width=200)           # Choose Model for Car/Bike
        driveFrame   = LabelFrame(allFrames,text="Drive",width=200)           # Choose Drive handiness/type
        gearsFrame   = LabelFrame(allFrames,text="Gears",width=200)           # Choose Gear Setup
        controlFrame = LabelFrame(allFrames,text="Control",width=600)         # Where the Clear/Save buttons and description entry go.

        imageFrame.grid(row=0,column=0,columnspan=3,    padx=inPad,pady=inPad,sticky=N+W+E+S)
        depotFrame.grid(row=1,column=0,                 padx=inPad,pady=inPad,sticky=N+W+E+S)
        corbFrame.grid(row=2,column=0,                  padx=inPad,pady=inPad,sticky=N+W+E+S)
        modelFrame.grid(row=1,column=1,rowspan=2,       padx=inPad,pady=inPad,sticky=N+W+E+S)
        driveFrame.grid(row=1,column=2,                 padx=inPad,pady=inPad,sticky=N+W+E+S)
        gearsFrame.grid(row=2,column=2,                 padx=inPad,pady=inPad,sticky=N+W+E+S)
        controlFrame.grid(row=3,column=0,columnspan=3,  padx=inPad,pady=inPad,sticky=N+W+E+S)

        allFrames.grid_columnconfigure(0,weight=1)
        allFrames.grid_columnconfigure(1,weight=1)
        allFrames.grid_columnconfigure(2,weight=1)

        """     Visualisation of main layout.
        +--------------------------------------+
        | imageFrame    (has its own grids!)   |
        +------------+------------+------------+
        | depotframe |            | driveFrame |
        +------------+ modelFrame +------------+
        | corbFrame  |            | gearsFrame |
        +------------+------------+------------+
        | controlFrame   (ditto imageFrame!)   |
        +--------------------------------------+
        """

        # GUI Vars
        ##########
        # List variables
        GUI_modelList   = StringVar()   # List of models from the chosen depot (below) to load in.
        GUI_driveList   = StringVar()   # List of drives from above.
        GUI_gearsList   = StringVar()   # List of gears from above.
        GUI_carBike     = IntVar()      # 0 = car, 1 = bike.
        GUI_carBikeStr  = StringVar()   # String/text representation of above.

        # Choices chosen variables.
        GUI_chosenDepot = StringVar()   # Chosen depot to Build From.
        GUI_chosenModel = StringVar()   # Model option selected.
        GUI_chosenDrive = StringVar()   # Drive option selected.
        GUI_chosenGears = StringVar()   # Gears option selected.
        GUI_name        = StringVar()   # Vehicle Name.
        GUI_description = StringVar()   # Vehicle Description.
        GUI_price       = DoubleVar()   # Price of the vehicle (from Depot and Model)

        # Item Descriptions variables.
        GUI_modelDesc   = StringVar()   # Description for model.
        GUI_driveDesc   = StringVar()   # Description for drive.
        GUI_gearsDesc   = StringVar()   # Description for gears.

        # Functions
        ###########
        def changeDepot(event):
            # Callback Function for which Vendor to request a car from.
            # Populates with vendor data from Models, Drive, and Gears.
            # Model data loaded is contingent on $self.carOrBike, too.
            self.depotIndex = self.depots.index(event)
            self.depotObj   = self.depots[self.depotIndex]
            self.company    = self.depotObj.transporter
            GUI_chosenDepot.set(str(self.depotObj))
            modelsList.selection_clear(0,END)
            createDepotOptions(True)

        def createDepotOptions(deselect=False):
            # Clear lists and repopulates them with the current depot
            # object's lists of objects into lists.
            self.cars       = []
            self.bikes      = []
            self.drives     = []
            self.gears      = []

            self.cars       = self.depotObj.vehicleCars
            self.bikes      = self.depotObj.vehicleBikes
            self.drives     = self.depotObj.vehicleDrives
            self.gears      = self.depotObj.vehicleGears
            self.price      = 0.0
            GUI_price.set("")

            self.chosenDrive = None
            self.chosenGears = None

            changeType()
            GUI_driveList.set(self.drives)
            GUI_gearsList.set(self.gears)
            GUI_chosenDrive.set("")
            GUI_chosenGears.set("")
            GUI_price.set("")

            GUI_modelDesc.set("")
            GUI_driveDesc.set("")
            GUI_gearsDesc.set("")

            if(deselect == True):
                # This is to make sure it doesn't break on first go,
                # As these Listbox objects won't exist yet.
                driveList.selection_clear(0,END)
                gearsList.selection_clear(0,END)
                modelsList.selection_clear(0,END)

        def changeType():
            # Callback Function for whether you're building a car or bike.
            # Populates with data from Cars or Bikes of the Vendor
            self.chosenModel = None
            GUI_chosenModel.set("")
            GUI_modelDesc.set("")

            self.price       = 0.0
            GUI_price.set("")

            self.carOrBike = GUI_carBike.get()
            populateModelList(self.carOrBike)

        def populateModelList(corb):
            # Populates the list with cars or bikes from the chosen depot.
            # 0 = load cars, and 1 = load bikes.
            if(corb == 0):
                # Grab Cars from Depot.
                GUI_carBikeStr.set("Car")
                GUI_modelList.set(self.cars)
            elif(corb == 1):
                # Grab Motorcycles from Depot.
                GUI_carBikeStr.set("Bike")
                GUI_modelList.set(self.bikes)

        def returnModelList():
            # Returns the Car or Bike models,
            # depending on $self.carOrBike's 0/1 status.
            if(self.carOrBike == 0):
                return self.cars
            elif(self.carOrBike == 1):
                return self.bikes

        def changeModel():
            # Callback function for changing the vehicle's base model.
            modelObj = getRecord(returnModelList(),getCurSel(modelsList),modelsList)
            GUI_chosenModel.set(str(modelObj))
            GUI_modelDesc.set(modelObj.desc)
            self.chosenModel = modelObj
            calcPrice()

        def changeDrive():
            # Callback function for changing the vehicle's drive type.
            driveObj = getRecord(self.drives,getCurSel(driveList),driveList)
            GUI_chosenDrive.set(str(driveObj))
            GUI_driveDesc.set(driveObj.desc)
            self.chosenDrive = driveObj
            calcPrice()

        def changeGears():
            # Callback function for changing the vehicle's gear setup.
            gearsObj = getRecord(self.gears,getCurSel(gearsList),gearsList)
            GUI_chosenGears.set(str(gearsObj))
            GUI_gearsDesc.set(gearsObj.desc)
            self.chosenGears = gearsObj
            calcPrice()

        def changeName(event):
            # Callback function for entry field: Name.
            name = nameEntry.get()
            GUI_name.set(name)
            self.newName = name
            print(name)

        def changeDesc(event):
            # Callback function for entry field: Description.
            desc = descEntry.get()
            GUI_description.set(desc)
            self.newDesc = desc
            print(desc)

        def calcPrice():
            # Attempts to calculate, set and display the price.
            try:
                newPrice    = self.depotObj.transporter.baseRate + self.chosenModel.rate
                self.price  = newPrice
                GUI_price.set(self.price)
            except AttributeError:
                # Occurs because a model hasn't been chosen, normally.
                # Or a transporter hasn't been chosen, somehow!
                pass

        def clearOptions():
            # Clears Model, Drive, Gears and Price fields.
            # And their respective GUI vars.
            self.newName = ""
            GUI_name.set("")

            self.newDesc = ""
            GUI_description.set("")

            self.chosenModel = None
            GUI_chosenModel.set("")
            GUI_modelDesc.set("")

            self.chosenDrive = None
            GUI_chosenDrive.set("")
            GUI_driveDesc.set("")

            self.chosenGears = None
            GUI_chosenGears.set("")
            GUI_gearsDesc.set("")

            self.price       = 0.0
            GUI_price.set("")

        def makeVehicle():
            # Create the vehicle, using the chosen bits and bobs.
            choose = tkinter.messagebox.askyesno("Flying Travel Agency","Build Vehicle using the given options?")
            if(choose == True):
                print("makeVehicle: Checking for all fields filled.")
                '''
                print(self.company)
                print(self.chosenModel)
                print(self.chosenDrive)
                print(self.chosenGears)
                print(self.newName)
                print(self.newDesc)
                '''

                if(self.chosenModel == None or self.chosenDrive == None or self.chosenGears == None):
                    print("makeVehicle: Missing fields.")
                    tkinter.messagebox.showerror("Flying Travel Agency","There are missing fields in your vehicle.\nPlease double-check your options and try again.")
                else:
                    # All details in place. Make car?
                    print("makeVehicle: All fields accounted for. Checking name and description lengths.")

                    # Do more verification.
                    ready = True
                    if(len(self.newDesc) < 12):
                        print("makeVehicle: Description not long enough.")
                        tkinter.messagebox.showerror("Flying Travel Agency","Your vehicle requires a description at least 12 characters long.")
                        ready = False

                    if(len(self.newName) < 3):
                        print("makeVehicle: Name not long enough.")
                        tkinter.messagebox.showerror("Flying Travel Agency","Your vehicle requires a name at least 3 characters long.")
                        ready = False

                    if(ready == True):
                        # Definitely make car now.
                        print("makeVehicle: Making vehicle now! Everything's ship-shape")
                        dbCon = sqlite3.connect("./travelAgency.db")
                        dbCur = dbCon.cursor()

                        # Execute statement for products table.
                        dbCur.execute("SELECT max(pid) FROM products")
                        pid_tup = dbCur.fetchone()
                        new_pid = pid_tup[0]+1

                        prodTuple       = (new_pid,self.newName,self.newDesc)
                        dbCur.execute("INSERT INTO products (pid,name,desc) VALUES (?,?,?)",prodTuple)

                        # Execute statement for vehicle products table.
                        dbCur.execute("SELECT max(id) FROM prods_vehicles")
                        id_tup      = dbCur.fetchone()
                        new_id      = id_tup[0]+1

                        trans_ind   = db.transporterList.index(self.company)
                        if(self.carOrBike == 0):
                            corb    = "car"
                            model   = db.carsList.index(self.chosenModel)
                        else:
                            corb    = "bike"
                            model   = db.bikesList.index(self.chosenModel)
                        drive       = db.driveList.index(self.chosenDrive)
                        gears       = db.gearList.index(self.chosenGears)

                        vehicleTuple    = (new_pid,new_id,trans_ind,corb,model,drive,gears)

                        dbCur.execute("INSERT INTO prods_vehicles (pid,id,transporter,vtype,model,drive,gears) VALUES (?,?,?,?,?,?,?)",vehicleTuple)

                        # Create object here, locally.
                        newVehicle = Vehicle(self.company,self.chosenModel,self.chosenDrive,self.chosenGears)
                        newVehicle.updateName(self.newName)
                        newVehicle.updateDesc(self.newDesc)
                        newVehicle.calcVehiclePrice(True)

                        # Wrap up and finish. Notify user.
                        dbCon.commit()
                        dbCon.close()

                        print("makeVehicle: Success! "+str(newVehicle)+" was created and added to the database!")
                        tkinter.messagebox.showinfo("Flying Travel Agency","Success! "+str(newVehicle)+" was created and added to the database!")
                        clearOptions()

                    else:
                        print("makeVehicle: Cancelled due to missing/insufficient name and/or description.")
            else:
                print("makeVehicle: User cancelled.")

        # Pre-populate the Depot options by calling
        createDepotOptions()
        # immediately after its written. :y

        # Widgets
        #########
        ## imageFrame Widgets
        # Where your choices are displayed/recorded.
        """ Layout for this area.
        +-----------+--------------+-------------+-------------+-------------+-------+
        | DepotName |   Car/Bike   | chosenModel | ChosenDrive | ChosenGears | Price |
        +-----------+--------------+-------------+-------------+-------------+-------+
        |   Depot   | Vehicle Type |    Model    |    Drive    |    Gears    | Price |
        +-----------+--------------+-------------+-------------+-------------+-------+
        6 columns, 2 rows, 46 px wide, each? (adding 2 to both sides from padding)
        """
        #comingsoon = Label(imageFrame,text="Eye candy/current choices coming soon!")
        #comingsoon.grid(row=0,column=0,     padx=inPad,pady=inPad)

        chosenDepot = Label(imageFrame,textvariable=GUI_chosenDepot,relief=GROOVE)
        depotLabel  = Label(imageFrame,text="Depot")

        corbChoice  = Label(imageFrame,textvariable=GUI_carBikeStr,relief=GROOVE)
        corbLabel   = Label(imageFrame,text="Car/Bike")

        modelChoice = Label(imageFrame,textvariable=GUI_chosenModel,relief=GROOVE)
        modelLabel  = Label(imageFrame,text="Model")

        driveChoice = Label(imageFrame,textvariable=GUI_chosenDrive,relief=GROOVE)
        driveLabel  = Label(imageFrame,text="Drive")

        gearsChoice = Label(imageFrame,textvariable=GUI_chosenGears,relief=GROOVE)
        gearsLabel  = Label(imageFrame,text="Gears")

        priceDisplay= Label(imageFrame,textvariable=GUI_price,relief=GROOVE)
        priceLabel  = Label(imageFrame,text="Price")

        chosenDepot.grid(row=1,column=0,    padx=inPad,pady=inPad,sticky=W+E)
        depotLabel.grid(row=0,column=0,     padx=inPad,pady=inPad,sticky=W+E)
        corbChoice.grid(row=1,column=1,     padx=inPad,pady=inPad,sticky=W+E)
        corbLabel.grid(row=0,column=1,      padx=inPad,pady=inPad,sticky=W+E)
        modelChoice.grid(row=1,column=2,    padx=inPad,pady=inPad,sticky=W+E)
        modelLabel.grid(row=0,column=2,     padx=inPad,pady=inPad,sticky=W+E)

        driveChoice.grid(row=1,column=3,    padx=inPad,pady=inPad,sticky=W+E)
        driveLabel.grid(row=0,column=3,     padx=inPad,pady=inPad,sticky=W+E)
        gearsChoice.grid(row=1,column=4,    padx=inPad,pady=inPad,sticky=W+E)
        gearsLabel.grid(row=0,column=4,     padx=inPad,pady=inPad,sticky=W+E)
        priceDisplay.grid(row=1,column=5,   padx=inPad,pady=inPad,sticky=W+E)
        priceLabel.grid(row=0,column=5,     padx=inPad,pady=inPad,sticky=W+E)

        imageFrame.grid_columnconfigure(0,weight=1)
        imageFrame.grid_columnconfigure(1,weight=1)
        imageFrame.grid_columnconfigure(2,weight=1)
        imageFrame.grid_columnconfigure(3,weight=1)
        imageFrame.grid_columnconfigure(4,weight=1)
        imageFrame.grid_columnconfigure(5,weight=1)

        ## depotFrame Widgets
        # Which Depot you're getting your vehicle from.
        GUI_chosenDepot.set(self.depots[self.depotIndex])        # Set GUI var.
        depotLabel = Label(depotFrame,text="Choosing a new Depot will change your available models, drives, and gears, and reset your current vehicle building options.",wraplength=180,anchor=N+W,justify=LEFT)
        depotMenu  = OptionMenu(depotFrame,GUI_chosenDepot,       # Create option menu.
                                *self.depots,command=changeDepot)
        depotMenu.grid(row=0,column=0,      padx=inPad,pady=inPad,sticky=N+W+S)
        depotLabel.grid(row=1,              padx=inPad,pady=inPad,sticky=N+W+S)

        ## corbFrame Widgets
        # Car or Bike selection.
        GUI_carBike.set(0)  # Set it to Car (0), by default.
        corbCar          = PhotoImage(file=self.imgDir+self.icons["Car"])
        carLabel         = Label(corbFrame,image=corbCar)
        carLabel.corbCar = corbCar
        carRadio         = Radiobutton(corbFrame,text="Car",variable=GUI_carBike,value=0,command=changeType)

        corbBike           = PhotoImage(file=self.imgDir+self.icons["Bike"])
        bikeLabel          = Label(corbFrame,image=corbBike)
        bikeLabel.corbBike = corbBike
        bikeRadio          = Radiobutton(corbFrame,text="Bike",variable=GUI_carBike,value=1,command=changeType)

        corbLabel = Label(corbFrame,text="Changing from Car to Bike and vice versa will change what models are available to you from the depot, and reset your currently chosen model.",wraplength=196,anchor=N+W,justify=LEFT)

        carLabel.grid(row=0,column=0,               padx=inPad,pady=inPad,sticky=W+E+N+S)
        carRadio.grid(row=0,column=1,               padx=inPad,pady=inPad,sticky=N+W+E+S)
        bikeLabel.grid(row=1,column=0,              padx=inPad,pady=inPad,sticky=W+E+N+S)
        bikeRadio.grid(row=1,column=1,              padx=inPad,pady=inPad,sticky=N+W+E+S)
        corbLabel.grid(row=2,column=0,columnspan=2, padx=inPad,pady=inPad,sticky=N+W+S)

        ## modelFrame Widgets
        # Which model (cars or bikes)
        modelsScroll = Scrollbar(modelFrame,jump=1) # Set GUI var.
        modelsList   = Listbox(modelFrame,height=12,width=24,listvariable=GUI_modelList,
                               selectmode="SINGLE",activestyle="dotbox",yscrollcommand=modelsScroll.set)
        modelsScroll.config(command=modelsList.yview)
        modelsList.bind("<Double-Button-1>",lambda x: changeModel())
        modelConfirm = Button(modelFrame,text="Choose Model",command=lambda: changeModel())
        modelDesc    = Label(modelFrame,textvariable=GUI_modelDesc,wraplength=160,anchor=N+W,justify=LEFT)

        modelsList.grid(row=0,column=0,                 padx=inPad,pady=inPad,sticky=N+E+S)
        modelsScroll.grid(row=0,column=1,               padx=inPad,pady=inPad,sticky=N+E+S)
        modelConfirm.grid(row=1,column=0,columnspan=2,  padx=inPad,pady=inPad,sticky=E+W)
        modelDesc.grid(row=2,column=0,columnspan=3,     padx=inPad,pady=inPad)

        ## driveFrame Widgets
        # What side of the car the steering 'wheel' is on.
        driveIcon            = PhotoImage(file=self.imgDir+self.icons["Wheel"])
        driveLabel           = Label(driveFrame,image=driveIcon)
        driveLabel.driveIcon = driveIcon

        driveScroll = Scrollbar(driveFrame,jump=1)
        driveList   = Listbox(driveFrame,height=5,width=24,listvariable=GUI_driveList,
                              selectmode="SINGLE",activestyle="dotbox",yscrollcommand=driveScroll.set)
        driveScroll.config(command=driveList.yview)
        driveList.bind("<Double-Button-1>",lambda x: changeDrive())
        driveConfirm = Button(driveFrame,text="Choose Drive",command=lambda: changeDrive())
        driveDesc    = Label(driveFrame,textvariable=GUI_driveDesc,wraplength=180,anchor=N+W,justify=LEFT)

        driveLabel.grid(row=0,column=0,                 padx=inPad,pady=inPad,sticky=N+W)
        driveList.grid(row=0,column=1,                  padx=inPad,pady=inPad,sticky=N+E+S+W)
        driveScroll.grid(row=0,column=2,                padx=inPad,pady=inPad,sticky=N+E+S)
        driveConfirm.grid(row=1,column=1,columnspan=2,  padx=inPad,pady=inPad,sticky=E+W)
        driveDesc.grid(row=2,column=0,columnspan=3,     padx=inPad,pady=inPad)

        ''' # Optionmenus are stupid. Don't use them for anything serious.
            # I found their limitations pretty freakin' quickly.
        driveMenu = OptionMenu(driveFrame,GUI_chosenDrive,
                               *self.drives,command=lambda event: changeDrive(event))
        driveMenu.grid(row=0,column=0,padx=inPad,pady=inPad)
        '''

        ## gearsFrame Widgets
        # What type of gearbox to use. List menu because option menus
        # are REALLY DUMB IF THEY CAN'T CHANGE AND PRESERVE FUNCTIONALITY.
        gearsIcon            = PhotoImage(file=self.imgDir+self.icons["Manual"])
        gearsLabel           = Label(gearsFrame,image=gearsIcon)
        gearsLabel.gearsIcon = gearsIcon

        gearsScroll = Scrollbar(gearsFrame,jump=1)
        gearsList   = Listbox(gearsFrame,height=5,width=24,listvariable=GUI_gearsList,
                              selectmode="SINGLE",activestyle="dotbox",yscrollcommand=gearsScroll.set)
        gearsScroll.config(command=gearsList.yview)
        gearsList.bind("<Double-Button-1>",lambda x: changeGears())
        gearsConfirm = Button(gearsFrame,text="Choose Gears",command=lambda: changeGears())
        gearsDesc    = Label(gearsFrame,textvariable=GUI_gearsDesc,wraplength=180,anchor=N+W,justify=LEFT)

        gearsLabel.grid(row=0,column=0,                 padx=inPad,pady=inPad,sticky=N+W)
        gearsList.grid(row=0,column=1,                  padx=inPad,pady=inPad,sticky=N+E+S+W)
        gearsScroll.grid(row=0,column=2,                padx=inPad,pady=inPad,sticky=N+E+S)
        gearsConfirm.grid(row=1,column=1,columnspan=2,  padx=inPad,pady=inPad,sticky=E+W)
        gearsDesc.grid(row=2,column=0,columnspan=3,     padx=inPad,pady=inPad)

        ''' # these damn optionmenus are more trouble than they're worth, and poorly documented.
        gearsMenu = OptionMenu(gearsFrame,GUI_chosenGears,
                               *self.gears,command=lambda event: changeGears(event))
        gearsMenu.grid(row=0,column=0,padx=inPad,pady=inPad)
        '''

        ## controlFrame Widgets
        # Description, clear car, and save car.
        nameLabel    = Label(controlFrame,text="Name:")
        nameEntry    = Entry(controlFrame,textvariable=GUI_name,width=30)
        nameEntry.bind("<FocusOut>",lambda event: changeName(event))

        descLabel    = Label(controlFrame,text="Description:")
        descEntry    = Entry(controlFrame,textvariable=GUI_description,width=60)
        descEntry.bind("<FocusOut>",lambda event: changeDesc(event))

        clearVehicle = Button(controlFrame,text="Clear Options",command=clearOptions)
        saveVehicle  = Button(controlFrame,text="Save Vehicle",command=makeVehicle)

        nameLabel.grid(row=0,column=0,              padx=inPad,pady=inPad,sticky=W)
        nameEntry.grid(row=0,column=1,              padx=inPad,pady=inPad,sticky=W)
        descLabel.grid(row=1,column=0,              padx=inPad,pady=inPad,sticky=W)
        descEntry.grid(row=1,column=1,columnspan=2, padx=inPad,pady=inPad,sticky=W)

        dontForget   = Label(controlFrame,text="Don't forget these fields either!",anchor=N+W,justify=LEFT)
        dontForget.grid(row=0,column=2,             padx=inPad,pady=inPad,sticky=W+E)
        requirements = Label(controlFrame,text="Name must be >3 characters long and description must be >12 characters long.",anchor=N+W,justify=LEFT)
        requirements.grid(row=2,column=0,columnspan=3, padx=inPad,pady=inPad,sticky=W)

        clearVehicle.grid(row=1,column=3,           padx=inPad,pady=inPad,sticky=N+E)
        saveVehicle.grid(row=1,column=4,            padx=inPad,pady=inPad,sticky=N+E)