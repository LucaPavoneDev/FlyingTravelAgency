from tkinter import *
# To get pop-up messages you gotta be a bit wonky. Oh well.
import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox

from cl_Interface import Window
from cl_Data import database as db
from gui.gui_Helpers import *

from gui.gui_DatabaseWin import DatabaseWindow
from gui.gui_TransactionWin import TransactionWindow
from gui.gui_PeopleWin import PeopleWindow
from gui.gui_SearchWin import SearchWindow
from gui.gui_FlightSearchWin import FlightSearchWindow
from gui.gui_VehicleCreator import VehicleCreator
from gui.gui_HotelSearch import HotelSearchWindow

# Create the introduction window.
#################################
class IntroWindow(Window):
    def __init__(self,master=None):
        Window.__init__(self,master)
        self.master = master
        self.introWindow()
        self.dataWin = None

    def introWindow(self):
        # Define a window title.
        self.master.title("Luca and Andrew's Flying Travel Agency")
        # Figure out how to pack it.
        self.pack(fill="both",expand=1)

        # Create menu bar, bind it to the window
        menuBar = Menu(self.master)
        self.master.config(menu=menuBar)

        # Create file menu, bind it to Menu Bar
        fileMenu = Menu(menuBar,tearoff=0)
        fileMenu.add_command(label="Home",command=self.goHome)
        fileMenu.add_separator()
        fileMenu.add_command(label="Quit",command=self.closeWindow)

        # Create splash screen
        # For some reason you gotta append the file as a new attribute
        # to prevent the image getting thrown out by Python cause it's dumb
        splashImg = PhotoImage(file="./img/SplashScreen.png")
        splash = Label(self,image=splashImg)
        splash.splashImg = splashImg
        splash.pack()

        # Create people/bills database menus
        peopleMenu = Menu(menuBar,tearoff=0)
        peopleMenu.add_command(label="Staff",command=lambda: self.openPeople("staffList"))
        peopleMenu.add_command(label="Customers",command=lambda: self.openPeople("customerList"))
        peopleMenu.add_separator()
        peopleMenu.add_command(label="All Transactions",command=lambda: self.openTransacs("transacList"))
        peopleMenu.add_command(label="Billable Transactions",command=lambda: self.openTransacs("orderList"))
        #peopleMenu.add_command(label="Bills",command=lambda: self.openTransacs("salesList"))
        #peopleMenu.add_command(label="Dockets",command=lambda: self.openTransacs("docketList"))
        #peopleMenu.add_separator()
        #peopleMenu.add_command(label="Pending Payments")
        #peopleMenu.add_command(label="Outstanding Payments")
        #peopleMenu.add_command(label="Completed Payments")
        #peopleMenu.add_command(label="Failed Payments")

        # Create product menu for database sub-menu
        prodMenu = Menu(menuBar,tearoff=0)
        prodMenu.add_command(label="Search All Products/Items...",command=self.openSearch)
        prodMenu.add_separator()
        prodMenu.add_command(label="All Products",command=lambda: self.openDB("prodList"))
        prodMenu.add_separator()
        prodMenu.add_command(label="Activity Products",command=lambda: self.openDB("actList"))
        prodMenu.add_command(label="Flight Products",command=lambda: self.openDB("flightList"))
        prodMenu.add_command(label="Hotel Products",command=lambda: self.openDB("hotelList"))
        prodMenu.add_command(label="Insurance Products",command=lambda: self.openDB("insList"))
        prodMenu.add_command(label="Transport Products",command=lambda: self.openDB("vehicleList"))
        prodMenu.add_separator()
        prodMenu.add_command(label="Detailed Flight Search",command=lambda: self.openFlightSearch())
        prodMenu.add_command(label="Detailed Hotel Search",command=lambda: self.openHotelSearch())
        prodMenu.add_command(label="Vehicle Creator",command=lambda: self.openVehicleCreator())

        # Create product feature database
        featMenu = Menu(menuBar,tearoff=0)
        featMenu.add_command(label="Countries", command=lambda:self.openDB("countryList"))
        featMenu.add_command(label="Locations", command=lambda:self.openDB("locationList"))
        featMenu.add_separator()
        featMenu.add_command(label="  ACTIVITIES",state=DISABLED)     # This serves as a header.
        featMenu.add_command(label="Activity Providers",command=lambda: self.openDB("actProvidersList"))
        featMenu.add_command(label="Activity Types",command=lambda: self.openDB("actTypesList"))
        featMenu.add_separator()
        featMenu.add_command(label="  FLIGHTS",state=DISABLED)
        featMenu.add_command(label="Airports",command=lambda: self.openDB("airportList"))
        featMenu.add_command(label="Airlines",command=lambda: self.openDB("airlineList"))
        featMenu.add_command(label="Air Tickets",command=lambda: self.openDB("airTicketList"))
        featMenu.add_separator()
        featMenu.add_command(label="  HOTELS",state=DISABLED)
        featMenu.add_command(label="Hoteliers",command=lambda: self.openDB("hotelierList"))
        featMenu.add_command(label="Hotel Rooms",command=lambda: self.openDB("hotelRoomList"))
        featMenu.add_command(label="Hotel Features",command=lambda: self.openDB("hotelFeatureList"))
        featMenu.add_separator()
        featMenu.add_command(label="  INSURANCE",state=DISABLED)
        featMenu.add_command(label="Insurance Providers",command=lambda: self.openDB("insProvidersList"))
        featMenu.add_command(label="Insurance Cover Options",command=lambda: self.openDB("insCoverList"))
        featMenu.add_separator()
        featMenu.add_command(label="  TRANSPORTATION",state=DISABLED)
        featMenu.add_command(label="Transport Depots",command=lambda: self.openDB("transpoList"))
        featMenu.add_command(label="Transporters",command=lambda: self.openDB("transporterList"))
        featMenu.add_command(label="Car Types",command=lambda: self.openDB("carsList"))
        featMenu.add_command(label="Bike Types",command=lambda: self.openDB("bikesList"))
        featMenu.add_command(label="Drive Configs",command=lambda: self.openDB("driveList"))
        featMenu.add_command(label="Gear Configs",command=lambda: self.openDB("gearList"))

        # Add the new drop-down menus to the main menu bar
        menuBar.add_cascade(label="File",menu=fileMenu)
        menuBar.add_cascade(label="People and Payment",menu=peopleMenu)
        menuBar.add_cascade(label="Products and Services",menu=prodMenu)
        menuBar.add_cascade(label="Product Features and Data",menu=featMenu)

        # Add a Quit Button
        '''
        quitButton = Button(self,text="Quit",command=self.closeWindow)
        quitButton.place(x=16,y=16)
        '''

    def goHome(self):
        # Currently redundant, but I'll keep this here for a rainy day.
        print("Going home...")

    def openDB(self,l=None):
        # Open a database.
        self.dataWin = Toplevel(self.master)
        self.app     = DatabaseWindow(master=self.dataWin,listName=l)
        # Make the window non-resizeable.
        self.app.master.transient(self.master)
        self.app.master.resizable(width=False, height=False)

    def openTransacs(self,l=None):
        # Open the transactions window.
        self.dataWin = Toplevel(self.master)
        self.app     = TransactionWindow(master=self.dataWin,listName=l)
        # Make window non resizeable once its up.
        self.app.master.transient(self.master)
        self.app.master.resizable(width=False, height=False)

    def openSearch(self):
        # Open a Search Window
        self.dataWin = Toplevel(self.master)
        self.app     = SearchWindow(master=self.dataWin)
        #Make window non-resizeable once up.
        self.app.master.transient(self.master)
        self.app.master.resizable(width=False, height=False)

    def openPeople(self,l=None):
        # Open a people changing window.
        # Specify which database list to use
        # Using 'customerList' or 'staffList'
        self.dataWin = Toplevel(self.master)
        self.app     = PeopleWindow(master=self.dataWin,listName=l)
        # Make window non-resizeable once up.
        self.app.master.transient(self.master)
        self.app.master.resizable(width=False, height=False)
    
    def openFlightSearch(self):
        # Open a detailed Flight Search.
        self.dataWin = Toplevel(self.master)
        self.app     = FlightSearchWindow(master=self.dataWin)
        # Make window non-resizeable once up.
        self.app.master.transient(self.master)
        self.app.master.resizable(width=False, height=False)
    
    def openHotelSearch(self):
        self.dataWin = Toplevel(self.master)
        self.app     = HotelSearchWindow(master=self.dataWin)
        # Make window non-resizeable once up.
        self.app.master.transient(self.master)
        self.app.master.resizable(width=False, height=False)
    
    def openVehicleCreator(self):
        # Open a vehicle creator.
        self.dataWin = Toplevel(self.master)
        self.app     = VehicleCreator(master=self.dataWin)
        # Make window non-resizeable once up
        self.app.master.transient(self.master)
        self.app.master.resizable(width=False, height=False)

    def closeWindow(self):
        # Quit the program, gracefully as possible by closing all previous windows.
        exit()