from tkinter import *
# To get pop-up messages you gotta be a bit wonky. Oh well.
import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox

from cl_Interface import Window
from cl_Data import database as db
from cl_Products import Hotel
import datetime as dt
from gui.gui_Helpers import *

# Class for hotel searches.
########################################
class HotelSearchWindow(Window):
    def __init__(self,master=None):
        Window.__init__(self,master)
        # Variable setup.
        self.hotels     = db.getList("hotelList")
        self.hoteliers  = db.getList("hotelierList")
        self.rooms      = db.getList("hotelRoomList")
        self.features   = db.getList("hotelFeatureList")
        self.locations  = db.getList("locationList")
        
        self.hotelierObj    = self.hoteliers[0]
        self.roomObj        = self.rooms[0]
        self.locationObj    = self.locations[0]
        self.featuresChosen = []
        
        self.priceMax       = 0.0
        self.priceMin       = 0.0
        self.results        = []
        
        self.hotelSearch()
        
    def hotelSearch(self):
        ##################
        # The Essentials #
        ##################
        outerPad = 4
        innerPad = 2
        
        self.master.title("Flying Travel Agency - Detailed Hotel Search")
        self.pack(fill="both",expand=1,padx=outerPad,pady=outerPad)
        
        # Main Frames
        leftFrame = Frame(self)
        rightFrame = Frame(self)
        # Left left, right right, yadda yadda.
        leftFrame.pack(side=LEFT,padx=outerPad,pady=outerPad,fill="both",expand=1)
        rightFrame.pack(side=RIGHT,padx=outerPad,pady=outerPad,fill="both",expand=1)
        # Major frames within said frames.
        searchFrame = LabelFrame(leftFrame,text="Search")
        recordFrame = LabelFrame(rightFrame,text="Results")
        searchFrame.pack(side=TOP,padx=innerPad,pady=innerPad,fill="both",expand=1)
        recordFrame.pack(side=TOP,padx=innerPad,pady=innerPad,fill="both",expand=1)
        
        #################
        # GUI Variables #
        #################
        # Search Criteria Checkboxes
        GUI_byHotelier  = BooleanVar(False)
        GUI_byRoom      = BooleanVar(False)
        GUI_byFeatures  = BooleanVar(False)
        GUI_byLocation  = BooleanVar(False)
        GUI_byPrice     = BooleanVar(False)
        
        # Search Criteria Fields
        GUI_hotelier    = StringVar()
        GUI_room        = StringVar()
        GUI_features    = StringVar()
        GUI_location    = StringVar()
        
        GUI_minPrice    = DoubleVar()
        GUI_maxPrice    = DoubleVar()
        
        # Results View
        GUI_results     = StringVar()

        #############
        # Functions #
        #############
        # TBD
        def executeSearch():
            print("executeSearch: Starting...")
            # Clear existing results
            GUI_results.set("")
            self.results = []
            recordsList.delete(0,END)
            
            def addToResults(item,type="parameter"):
                # Helper function.
                if(item not in self.results):
                    print("Match for "+type+" on "+str(item)+".")
                    self.results.append(item)
                    recordsList.insert(END,str(item))
                else:
                    print("Additional match for "+type+" on "+str(item)+".")
            
            print("executeSearch: Searching...")
            for h in self.hotels:
                if(GUI_byHotelier.get() == True):
                    # Search by Hotelier/Operator.
                    hotlr = h.hotelier
                    if(self.hotelierObj == hotlr):
                        addToResults(h,"hotelier")
                
                if(GUI_byRoom.get() == True):
                    # Search by Room Type.
                    roomt = h.roomTypes
                    if(self.roomObj in roomt):
                        addToResults(h,"room")
                
                if(GUI_byFeatures.get() == True):
                    # Search by Hotel Features.
                    feats = h.hotelFeatures
                    for f in self.featuresChosen:
                        if(f in feats):
                            addToResults(h,"features")
                
                if(GUI_byLocation.get() == True):
                    # Search by Location.
                    locat = h.location
                    if(self.locationObj == locat):
                        addToResults(h,"location")
                
                if(GUI_byPrice.get() == True):
                    # Search by price range.
                    if(self.priceMin < h.price < self.priceMax):
                        addToResults(h,"price")
            
        def menuCB_Hotelier(event):
            #print(event)
            # Callback for hotelier selection.
            self.hotelierObj = db.getObjFromList("hotelierList",self.hoteliers.index(event))
        
        def menuCB_Room(event):
            #print(event)
            # Callback for room selection.
            self.roomObj = db.getObjFromList("hotelRoomList",self.rooms.index(event))
        
        def menuCB_Location(event):
            #print(event)
            # Callback for location selection.
            self.locationObj = db.getObjFromList("locationList",self.locations.index(event))
        
        def updateFeatures():
            # Callback for updating selected features.
            self.featuresChosen = []
            features = featList.curselection()
            for f in features:
                self.featuresChosen.append(self.features[f])
            #print(self.featuresChosen)
        
        def clearFeatures():
            # Callback for removing all features.
            featList.selection_clear(0,END)
            updateFeatures()
        
        def entryCB_MinPrice(event):
            # Callback for minimum price entry.
            f = priceMinField
            try:
                p = GUI_minPrice.get()
                self.priceMin = p
            except:
                f.delete(0,END)
                f.insert(INSERT,self.priceMin)
            
        def entryCB_MaxPrice(event):
            # Callback for maximum price entry.
            f = priceMaxField
            try:
                p = GUI_maxPrice.get()
                self.priceMax = p
            except:
                f.delete(0,END)
                f.insert(INSERT,self.priceMax)
            
            
        #########################
        # 'searchFrame' Widgets #
        #########################
        # Search Criteria Selection
        labelSearchBy   = Label(searchFrame,text="By...")
        labelCriteria   = Label(searchFrame,text="Criteria")
        byHotelier      = Checkbutton(searchFrame,variable=GUI_byHotelier)
        byRoom          = Checkbutton(searchFrame,variable=GUI_byRoom)
        byFeatures      = Checkbutton(searchFrame,variable=GUI_byFeatures)
        byLocation      = Checkbutton(searchFrame,variable=GUI_byLocation)
        byPrice         = Checkbutton(searchFrame,variable=GUI_byPrice)
        searchButton    = Button(searchFrame,text="Search",command=lambda: executeSearch())
        
        # Packing all that up.
        labelSearchBy.grid(row=0,column=0)          # Label Row.
        labelCriteria.grid(row=0,column=1)          # Label Row.
        
        byHotelier.grid(row=1,column=0,sticky=E+W)  # Hotelier Search.
        byRoom.grid(row=2,column=0,sticky=E+W)      # Room Search.
        byFeatures.grid(row=3,column=0,sticky=E+W)  # Feature Search.
        byLocation.grid(row=4,column=0,sticky=E+W)  # Location Search.
        byPrice.grid(row=5,column=0,sticky=E+W)     # Price Search
        searchButton.grid(row=6,column=0,columnspan=2,sticky=E+W)
        
        # Saerch Criteria Detail Subframes
        htlrSearchFrame = LabelFrame(searchFrame,text="By Hotelier")
        htlrSearchFrame.grid(row=1,column=1,sticky=E+W)
        
        roomSearchFrame = LabelFrame(searchFrame,text="By Room")
        roomSearchFrame.grid(row=2,column=1,sticky=E+W)
        
        featSearchFrame = LabelFrame(searchFrame,text="By Features")
        featSearchFrame.grid(row=3,column=1,sticky=E+W)
        
        locaSearchFrame = LabelFrame(searchFrame,text="By Location")
        locaSearchFrame.grid(row=4,column=1,sticky=E+W)
        
        pricSearchFrame = LabelFrame(searchFrame,text="By Price")
        pricSearchFrame.grid(row=5,column=1,sticky=E+W)
        
        #############################
        # 'htlrSearchFrame' Widgets #
        #############################
        GUI_hotelier.set(self.hoteliers[0])
        
        hotelierLabel   = Label(htlrSearchFrame,text="Hotelier: ")
        hotelier        = OptionMenu(htlrSearchFrame,GUI_hotelier,*self.hoteliers,command=menuCB_Hotelier)
        
        hotelierLabel.grid(row=0,column=0,sticky=W)
        hotelier.grid(row=0,column=1,sticky=W)
        
        #############################
        # 'roomSearchFrame' Widgets #
        #############################
        GUI_room.set(self.rooms[0])
        
        roomLabel   = Label(roomSearchFrame,text="Room: ")
        room        = OptionMenu(roomSearchFrame,GUI_room,*self.rooms,command=menuCB_Room)
        
        roomLabel.grid(row=0,column=0,sticky=W)
        room.grid(row=0,column=1,sticky=W)
        
        #############################
        # 'featSearchFrame' Widgets #
        #############################
        GUI_features.set(self.features)
        
        featScroll  = Scrollbar(featSearchFrame,jump=1)
        featList    = Listbox(featSearchFrame,height=12,width=25,listvariable=GUI_features,exportselection=False,
                              selectmode=MULTIPLE,activestyle="dotbox",yscrollcommand=featScroll.set)
        featScroll.config(command=featList.yview)
        featList.bind("<<ListboxSelect>>",lambda e: updateFeatures())
        featNone    = Button(featSearchFrame,text="Select None",command=lambda: clearFeatures())
        
        featList.grid(row=0,column=0,sticky=W)
        featScroll.grid(row=0,column=1,sticky=N+S)
        featNone.grid(row=1,column=0,columnspan=2,sticky=E+W)
        
        #############################
        # 'locaSearchFrame' Widgets #
        #############################
        GUI_location.set(self.locations[0])
        
        locationLabel   = Label(locaSearchFrame,text="Location: ")
        location        = OptionMenu(locaSearchFrame,GUI_location,*self.locations,command=menuCB_Location)
        
        locationLabel.grid(row=0,column=0,sticky=W)
        location.grid(row=0,column=1,sticky=W)
        
        #############################
        # 'pricSearchFrame' Widgets #
        #############################
        GUI_minPrice.set(0.0)
        GUI_maxPrice.set(0.0)
        
        priceMinLabel   = Label(pricSearchFrame,text="Min: ")
        priceMaxLabel   = Label(pricSearchFrame,text="Max: ")
        priceMinField   = Entry(pricSearchFrame,textvariable=GUI_minPrice)
        priceMaxField   = Entry(pricSearchFrame,textvariable=GUI_maxPrice)
        priceMinField.bind("<FocusOut>",entryCB_MinPrice)
        priceMaxField.bind("<FocusOut>",entryCB_MaxPrice)
        
        priceMinLabel.grid(row=0,column=0,sticky=W)
        priceMaxLabel.grid(row=1,column=0,sticky=W)
        priceMinField.grid(row=0,column=1,sticky=W)
        priceMaxField.grid(row=1,column=1,sticky=W)
        
        #########################
        # 'recordFrame' Widgets #
        #########################
        recordsScroll   = Scrollbar(recordFrame)
        recordsList     = Listbox(recordFrame,height=24,width=50,listvariable=GUI_results,
                                  selectmode="SINGLE",activestyle="dotbox",yscrollcommand=recordsScroll.set)
        recordsScroll.config(command=recordsList.yview)
        
        recordsList.grid(row=0,column=0,sticky=W)
        recordsScroll.grid(row=0,column=1,sticky=N+W+S)
        
        
        