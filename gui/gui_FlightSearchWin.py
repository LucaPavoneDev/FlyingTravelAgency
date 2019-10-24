from tkinter import *
# To get pop-up messages you gotta be a bit wonky. Oh well.
import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox

from cl_Interface import Window
from cl_Data import database as db
from cl_Products import Flight
import datetime as dt
from gui.gui_Helpers import *

# Class for flight searches.
########################################
class FlightSearchWindow(Window):
    def __init__(self,master=None):
        Window.__init__(self,master)
        # Set up variables for searching through and adding to dropdowns, etc.
        self.flights  = db.getList("flightList")
        self.airports = db.getList("airportList")
        self.airlines = db.getList("airlineList")
        self.tickets  = db.getList("airTicketList")
        
        self.dateFromDateObj   = None
        self.dateToDateObj     = None
        self.airportsDep_index = -1
        self.airportsArr_index = -1
        self.airline_index     = 0
        self.ticketType_index  = 0
        self.priceFromFloat    = 0.0
        self.priceToFloat      = 0.0
        self.results           = []
        
        self.flightSearch()
        
    def flightSearch(self):
        # The Essentials
        ################
        outerPad = 4
        innerPad = 2
        
        self.master.title("Flying Travel Agency - Detailed Flight Search")
        self.pack(fill="both",expand=1,padx=outerPad,pady=outerPad)
        
        # Main halves of the window.
        leftFrame  = Frame(self)
        rightFrame = Frame(self)
        # Left to left, right to right.
        leftFrame.pack(side=LEFT,padx=outerPad,pady=outerPad,fill="both",expand=1)
        rightFrame.pack(side=RIGHT,padx=outerPad,pady=outerPad,fill="both",expand=1)
        # Now for internal frames.
        searchFrame = LabelFrame(leftFrame,text="Search")
        recordFrame = LabelFrame(rightFrame,text="Results")
        recButtonFrame = Frame(recordFrame)
        searchFrame.pack(side=TOP,padx=innerPad,pady=innerPad,fill="both",expand=1)
        recordFrame.pack(side=TOP,padx=innerPad,pady=innerPad,fill="both",expand=1)
        
        # GUI Variables
        ###############
        # Main record returning list
        GUI_recordList  = StringVar()   # List of returned search items.
        # Entries/Dropdown Boxes
        GUI_airline     = StringVar()   # List of Airlines + Blank
        GUI_airportsDep = StringVar()   # List of Airports to depart from
        GUI_airportsArr = StringVar()   # List of Airports to arrive to
        GUI_ticketType  = StringVar()   # List of ticket types
        #GUI_flightCode  = StringVar()   # Entry for Flight Codes
        GUI_priceFrom   = DoubleVar()   # Minimum Price
        GUI_priceTo     = DoubleVar()   # Maximum Price
        
        # Search Criteria Checkboxes
        GUI_byDatetime  = BooleanVar(False)  # Search by Date and Time (True/False)
        GUI_byAirport   = BooleanVar(False)  # Search by Airports
        GUI_byAirline   = BooleanVar(False)  # Search by Airlines
        GUI_byTicket    = BooleanVar(False)  # Search by Ticket type
        GUI_byPrice     = BooleanVar(False)  # Search by Price Range
        
        # Functions
        ###########
        def executeSearch():
            print("executeSearch: Starting...")
            # Checks search parameters, then carries out search.
            # Setting up parameters to be populated.
            fromDateObj   = None
            toDateObj     = None
            airportDepObj = None
            airportArrObj = None
            airlineObj    = None
            ticketObj     = None
            priceMinFloat = None
            priceMaxFloat = None
            self.results  = []
            recordList.delete(0,END)
            # If something's passed through as a None, ignore searching for it.
            ######################################
            # Do Search Setup/Variable Assignment.
            print("executeSearch: Gathering Variables...")
            # Check Date/Time checkbox.
            if(GUI_byDatetime.get() == True):
                # Use Ben's date-picker method.
                self.dateFromDateObj = dateFrom.get()
                self.dateToDateObj   = dateTo.get()
                
                fromDateObj = self.dateFromDateObj
                toDateObj   = self.dateToDateObj
            
            # Check airport checkbox.
            if(GUI_byAirport.get() == True):
                if(self.airportsDep_index >= 0):
                    # Search for a departure airport.
                    airportDepObj = self.airports[self.airportsDep_index]
                    
                if(self.airportsArr_index >= 0):
                    # Search for an arrival airport.
                    airportArrObj = self.airports[self.airportsArr_index]
            
            # Check airline checkbox.
            if(GUI_byAirline.get() == True):
                # Search by airline.
                airlineObj = self.airlines[self.airline_index]
            
            # Check ticket checkbox.
            if(GUI_byTicket.get() == True):
                # Search by ticket type
                ticketObj = self.tickets[self.ticketType_index]
            
            # Check price range checkbox.
            if(GUI_byPrice.get() == True):
                # Search by price range.
                priceMinFloat = self.priceFromFloat
                priceMaxFloat = self.priceToFloat
                
            print(fromDateObj)
            print(toDateObj)
            print(airportDepObj)
            print(airportArrObj)
            print(airlineObj)
            print(ticketObj)
            print(priceMinFloat)
            print(priceMaxFloat)
            
            # Begin search criteria.
            ########################
            def addToFlightResults(flight,type="parameter"):
                # Helper function since I don't want to
                # write something like this multiple times.
                if(flight not in self.results):
                    # Matching entry doesn't exist in list.
                    print("Match for "+type+" on "+str(flight))
                    self.results.append(flight)
                    recordList.insert(END,str(flight))
                else:
                    # Already exists in list. All good.
                    print("Additional Match for "+type+" on "+str(flight))
            
            print("executeSearch: Searching...")
            for f in self.flights:
                if(GUI_byDatetime.get() == True):
                    #print("executeSearch: Searching by Date/Time range...")
                    f_dep_date = f.depDatetime.date()
                    f_arr_date = f.arrDatetime.date()
                    
                    if(fromDateObj < f_dep_date < toDateObj
                       or fromDateObj < f_arr_date < toDateObj):
                        addToFlightResults(f,"date")
                
                if(GUI_byAirport.get() == True):
                    #print("executeSearch: Searching by Airports...")
                    f_dep_airport = f.airportDep
                    f_arr_airport = f.airportArr
                    
                    if(f_dep_airport == airportDepObj):
                        addToFlightResults(f,"departing airport")
                    
                    if(f_arr_airport == airportArrObj):
                        addToFlightResults(f,"arriving airport")
                
                if(GUI_byAirline.get() == True):
                    #print("executeSearch: Searching by Airlines...")
                    f_airline = f.airline
                    if(f_airline == airlineObj):
                        addToFlightResults(f,"airline")
                
                if(GUI_byTicket.get() == True):
                    #print("executeSearch: Searching by Ticket type...")
                    f_ticket = f.ticket
                    if(f_ticket == ticketObj):
                        addToFlightResults(f,"ticket")
                
                if(GUI_byPrice.get() == True):
                    #print("executeSearch: Searching by Price range...")
                    f_price = f.price
                    #print(priceMinFloat)
                    #print(f_price)
                    #print(priceMaxFloat)
                    #print(priceMinFloat < f_price < priceMaxFloat)
                    if(priceMinFloat < f_price < priceMaxFloat):
                        addToFlightResults(f,"price")
            
            print("executeSearch: Finishing...")
        
        def menuCallback(event):
            # A regular ol' drop-down menu callback function.
            # Ostensibly for my own reference.
            print(event)
        
        def menuCallback_AirportDep(event):
            # Menu callback for Departure Airport picking.
            print(event)
            print(airportsList.index(event)-1)
            self.airportsDep_index = airportsList.index(event)-1
            
        def menuCallback_AirportArr(event):
            # Menu callback for Arrival Airport picking.
            print(event)
            print(airportsList.index(event)-1)
            self.airportsArr_index = airportsList.index(event)-1
            
        def menuCallback_Airline(event):
            # Menu callback for Airline picking.
            print(event)
            print(self.airlines.index(event))
            self.airline_index = self.airlines.index(event)
            
        def menuCallback_Ticket(event):
            # Menu callback for Ticket picking.
            print(event)
            print(self.tickets.index(event))
            self.ticketType_index = self.tickets.index(event)
            
        def entryCallback_minPrice(event):
            try:
                p = GUI_priceFrom.get()
                print(p)
                print(checkObject(p))
                self.priceFromFloat = p
                print(self.priceFromFloat)
                print(checkObject(self.priceFromFloat))
            except:
                priceFromEntry.delete(0,END)
                priceFromEntry.insert(INSERT,self.priceFromFloat)
            
            '''
            try:
                p = float(GUI_priceFrom.get())
                self.priceFromFloat = format(p,".2f")
                priceFromEntry.delete(0,END)
                priceFromEntry.insert(INSERT,p)
            except TypeError:
                print("That is not a valid type!")
                priceFromEntry.delete(0,END)
                priceFromEntry.insert(INSERT,format(priceFromFloat,".2f"))
            except ValueError:
                priceFromEntry.delete(0,END)
                priceFromEntry.insert(INSERT,format(priceFromFloat,".2f"))
                print("Text does not go there!")
            '''
        
        def entryCallback_maxPrice(event):
            try:
                p = GUI_priceTo.get()
                print(p)
                print(checkObject(p))
                self.priceToFloat = p
                print(self.priceToFloat)
                print(checkObject(self.priceToFloat))
            except:
                priceToEntry.delete(0,END)
                priceToEntry.insert(INSERT,self.priceToFloat)
            
            '''
            try:
                p = float(GUI_priceTo.get())
                self.priceToFloat = format(p,".2f")
                priceToEntry.delete(0,END)
                priceToEntry.insert(INSERT,p)
            except TypeError:
                print("Uh oh! That's not a valid type!")
                priceToEntry.delete(0,END)
                priceToEntry.insert(INSERT,format(priceToFloat,".2f"))
            except ValueError:
                print("Text does not go there!")
                priceToEntry.delete(0,END)
                priceToEntry.insert(INSERT,format(priceToFloat,".2f"))
            '''
        
        def openFlightWindow(flight=None):
            flightWin = Toplevel(self)
            window    = FlightWindow(flightWin,flight)
            window.master.transient(self.master)
            window.master.resizable(width=False,height=False)
        
        # searchFrame widgets/Frames
        ############################
        # This is going to be the tricky part!
        # Search Criteria Setup
        labelSearchBy   = Label(searchFrame,text="By...")
        labelCriteria   = Label(searchFrame,text="Criteria")
        byDateTime      = Checkbutton(searchFrame,variable=GUI_byDatetime)
        byAirport       = Checkbutton(searchFrame,variable=GUI_byAirport)
        byAirline       = Checkbutton(searchFrame,variable=GUI_byAirline)
        byTicket        = Checkbutton(searchFrame,variable=GUI_byTicket)
        byPrice         = Checkbutton(searchFrame,variable=GUI_byPrice)
        searchButton    = Button(searchFrame,text="Search",command=lambda: executeSearch())
        
        labelSearchBy.grid(row=0,column=0)          # Label Row.
        labelCriteria.grid(row=0,column=1)          # Label Row.
        byDateTime.grid(row=1,column=0,sticky=E+W)  # Date/Time Search Row.
        byAirport.grid(row=2,column=0,sticky=E+W)   # Airport Search Row.
        byAirline.grid(row=3,column=0,sticky=E+W)   # Airline Search Row.
        byTicket.grid(row=4,column=0,sticky=E+W)    # Ticket Search Row.
        byPrice.grid(row=5,column=0,sticky=E+W)     # Price Search Row.
        searchButton.grid(row=6,column=0,columnspan=2,sticky=E+W)
        
        # Search Criteria Frames
        dtSearchFrame   = LabelFrame(searchFrame,text="By Date/Time")
        dtSearchFrame.grid(row=1,column=1,sticky=E+W)
        apSearchFrame   = LabelFrame(searchFrame,text="By Airports")
        apSearchFrame.grid(row=2,column=1,sticky=E+W)
        alSearchFrame   = LabelFrame(searchFrame,text="By Airlines")
        alSearchFrame.grid(row=3,column=1,sticky=E+W)
        tiSearchFrame   = LabelFrame(searchFrame,text="By Tickets")
        tiSearchFrame.grid(row=4,column=1,sticky=E+W)
        prSearchFrame   = LabelFrame(searchFrame,text="By Price Range")
        prSearchFrame.grid(row=5,column=1,sticky=E+W)
        
        # Date/Time Search: dtSearchFrame
        #################################
        '''
        # This approach is risky. Not every computer's guaranteed to have Anaconda3 sitting pretty on it.
        import sys
        anaconda_dir = "C:\\Program Files\\Anaconda3\\Lib\\site-packages"
        sys.path.append(anaconda_dir)
        
        # So instead I copy/pasted the modules straight from Anaconda into the project directory.
        '''
        from benCode.datewidgets import Datebox
        # Cool thing is, folders with .py scripts in them can count as modules, of sorts.
        # But, since there's no "main.py" in that directory, you can just import the script
        # whole cloth and it'll handle all its bits and bobs as you'd expect. Cool eh?
        
        labelDateFrom   = Label(dtSearchFrame,text="Date From: ")
        labelDateTo     = Label(dtSearchFrame,text="Date To: ")
        
        dateFrom        = Datebox(dtSearchFrame,dt.date(2017,1,1),)
        dateTo          = Datebox(dtSearchFrame,dt.date.today(),)
        self.dateFromDateObj = dateFrom.get()
        self.dateToDateObj   = dateTo.get()
        
        labelDateFrom.grid(row=0,column=0,sticky=W)
        labelDateTo.grid(row=1,column=0,sticky=W)
        dateFrom.grid(row=0,column=1)
        dateTo.grid(row=1,column=1)
        
        ## MY OLD WAY ##
        # Staying here 'cause its just old code.
        # Not intended to be called.
        def lucaDatePicker():
            # Much clunkier, but much more locked down.
            # Could use this as part of a flight creator, actually!
            
            # Date/Time Search Boxes
            GUI_yearFrom    = StringVar()   # Year of flights to search from   (2018-2021)
            GUI_monthFrom   = StringVar()   # Month of flights to search from  (Blank + 01-12)
            GUI_dayFrom     = StringVar()   # Day of flights to search from    (Blank + 01-31)
            GUI_hourFrom    = StringVar()   # Hour of Flights to search from   (Blank + 00-23)
            GUI_minuteFrom  = StringVar()   # Minute of Flights to search from (Blank + 00-55 in increments of 5)
            
            GUI_yearTo      = StringVar()   # Year of flights to search to     (2018-2021)
            GUI_monthTo     = StringVar()   # Month of flights to search to    (Blank + 01-12)
            GUI_dayTo       = StringVar()   # Day of flights to search to      (Blank + 01-31)
            GUI_hourTo      = StringVar()   # Hour of flights to search to     (Blank + 00-23)
            GUI_minuteTo    = StringVar()   # Minute of flights to search to   (Blank + 00-55 in increments of 5)
            # No bloody way I'm doing minute by minute tracking of flights. Five minute intervals are fine.
            
            # Since the Date/Time search boxes are static (unless the structure of
            # time itself changes drastically overnight) I'll set up their variables here.
            yearList    = [2018,2019,2020,2021,2022]
            monthList   = [1,2,3,4,5,6,7,8,9,10,11,12]
            dayList     = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
            hourList    = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
            minuteList  = [0,5,10,15,20,25,30,35,40,45,50,55]
            
            GUI_yearFrom.set(yearList[0])
            GUI_monthFrom.set(monthList[0])
            GUI_dayFrom.set(dayList[0])
            GUI_hourFrom.set(hourList[0])
            GUI_minuteFrom.set(minuteList[0])
            
            GUI_yearTo.set(yearList[-1])
            GUI_monthTo.set(monthList[0])
            GUI_dayTo.set(dayList[0])
            GUI_hourTo.set(hourList[0])
            GUI_minuteTo.set(minuteList[0])
            
            # Widgets
            labelYear       = Label(dtSearchFrame,text="Year")
            labelMonth      = Label(dtSearchFrame,text="Month")
            labelDay        = Label(dtSearchFrame,text="Day")
            labelHour       = Label(dtSearchFrame,text="Hour")
            labelMinute     = Label(dtSearchFrame,text="Minute")
            
            labelFrom       = Label(dtSearchFrame,text="From: ")
            labelTo         = Label(dtSearchFrame,text="To: ")
            
            yearFrom        = OptionMenu(dtSearchFrame,GUI_yearFrom,*yearList)
            monthFrom       = OptionMenu(dtSearchFrame,GUI_monthFrom,*monthList)
            dayFrom         = OptionMenu(dtSearchFrame,GUI_dayFrom,*dayList)
            hourFrom        = OptionMenu(dtSearchFrame,GUI_hourFrom,*hourList)
            minuteFrom      = OptionMenu(dtSearchFrame,GUI_minuteFrom,*minuteList)
            
            # Reference for how I set these damn things up earlier. Crap on a cracker these are weird...
            # emailDrop   = OptionMenu(emailTypeFrame,GUI_emailType,*emailTypes,command=menuCallback).pack(side=TOP)

            yearTo          = OptionMenu(dtSearchFrame,GUI_yearTo,*yearList)
            monthTo         = OptionMenu(dtSearchFrame,GUI_monthTo,*monthList)
            dayTo           = OptionMenu(dtSearchFrame,GUI_dayTo,*dayList)
            hourTo          = OptionMenu(dtSearchFrame,GUI_hourTo,*hourList)
            minuteTo        = OptionMenu(dtSearchFrame,GUI_minuteTo,*minuteList)
            
            # Gridding the bits for Date/Time search.
            labelYear.grid(row=0,column=1)
            labelMonth.grid(row=0,column=2)
            labelDay.grid(row=0,column=3)
            labelHour.grid(row=0,column=4)
            labelMinute.grid(row=0,column=5)
            
            labelFrom.grid(row=1,column=0,sticky=W)
            labelTo.grid(row=2,column=0,sticky=W)
            
            yearFrom.grid(row=1,column=1)
            monthFrom.grid(row=1,column=2)
            dayFrom.grid(row=1,column=3)
            hourFrom.grid(row=1,column=4)
            minuteFrom.grid(row=1,column=5)
            
            yearTo.grid(row=2,column=1)
            monthTo.grid(row=2,column=2)
            dayTo.grid(row=2,column=3)
            hourTo.grid(row=2,column=4)
            minuteTo.grid(row=2,column=5)
        
        # Airport Search: apSearchFrame
        ###############################
        airportsList    = ["None/Any Airport (***)"]
        airportsList.extend(self.airports)
        
        GUI_airportsDep.set(airportsList[0])
        GUI_airportsArr.set(airportsList[0])
        
        labelDep    = Label(apSearchFrame,text="Departing From: ")
        labelArr    = Label(apSearchFrame,text="Arriving To: ")
        airportsDep = OptionMenu(apSearchFrame,GUI_airportsDep,*airportsList,command=menuCallback_AirportDep)
        airportsArr = OptionMenu(apSearchFrame,GUI_airportsArr,*airportsList,command=menuCallback_AirportArr)
        
        labelDep.grid(row=0,column=0,sticky=W)
        labelArr.grid(row=1,column=0,sticky=W)
        airportsDep.grid(row=0,column=1,sticky=W)
        airportsArr.grid(row=1,column=1,sticky=W)
        
        # Airline Search: alSearchFrame
        ###############################
        GUI_airline.set(self.airlines[0])
        
        airlineLabel    = Label(alSearchFrame,text="Airline: ")
        airline         = OptionMenu(alSearchFrame,GUI_airline,*self.airlines,command=menuCallback_Airline)
        
        airlineLabel.grid(row=0,column=0,sticky=W)
        airline.grid(row=0,column=1,sticky=W)
        
        # Ticket Search: tiSearchFrame
        ##############################
        GUI_ticketType.set(self.tickets[0])
        
        ticketLabel = Label(tiSearchFrame,text="Type: ")
        ticketType  = OptionMenu(tiSearchFrame,GUI_ticketType,*self.tickets,command=menuCallback_Ticket)
        
        ticketLabel.grid(row=0,column=0,sticky=W)
        ticketType.grid(row=0,column=1,sticky=W)
        
        # Price Search: prSearchFrame
        #############################
        priceFromFloat  = 0.00
        priceToFloat    = 0.00
        GUI_priceFrom.set(format(priceFromFloat,".2f"))
        GUI_priceTo.set(format(priceToFloat,".2f"))
        
        priceFromLabel  = Label(prSearchFrame,text="Minimum: ")
        priceToLabel    = Label(prSearchFrame,text="Maximum: ")
        priceFromEntry  = Entry(prSearchFrame,textvariable=GUI_priceFrom)
        priceToEntry    = Entry(prSearchFrame,textvariable=GUI_priceTo)
        priceFromEntry.bind("<FocusOut>",entryCallback_minPrice)
        priceToEntry.bind("<FocusOut>",entryCallback_maxPrice)
        
        priceFromLabel.grid(row=0,column=0,sticky=W)
        priceToLabel.grid(row=1,column=0,sticky=W)
        priceFromEntry.grid(row=0,column=1,sticky=W)
        priceToEntry.grid(row=1,column=1,sticky=W)
        
        # recordFrame and recButtonFrame
        # widgets and frames
        ################################
        # This is the easy part by comparison to the above.
        # I have tried and true patterns for it.
        recordScroll = Scrollbar(recordFrame,jump=1)
        recordList   = Listbox(recordFrame,height=21,width=50,listvariable=GUI_recordList,
                               selectmode="SINGLE",activestyle="dotbox",yscrollcommand=recordScroll.set)
        recordScroll.config(command=recordList.yview)
        
        recordFirst = Button(recordFrame,text="First",command=lambda: getRecord(self.results,(0,0),recordList))
        recordPrev  = Button(recordFrame,text="Previous",command=lambda: getRecord(self.results,getCurSel(recordList),recordList,offset=-1))
        recordOpen  = Button(recordFrame,text="Open",command=lambda: openFlightWindow(getRecord(self.results,getCurSel(recordList),recordList,offset=0)))
        recordNext  = Button(recordFrame,text="Next",command=lambda: getRecord(self.results,getCurSel(recordList),recordList,offset=1))
        recordLast  = Button(recordFrame,text="Last",command=lambda: getRecord(self.results,(recordList.size()-1,0),recordList))
        
        recordList.bind("<Double-Button-1>",lambda x: openFlightWindow(getRecord(self.results,getCurSel(recordList),recordList,offset=0)))
        
        recordList.grid(row=0,column=0,columnspan=5)
        recordScroll.grid(row=0,column=5,sticky=N+S)
        
        recordFirst.grid(row=1,column=0,sticky=E+W)
        recordPrev.grid(row=1,column=1,sticky=E+W)
        recordOpen.grid(row=1,column=2,sticky=E+W)
        recordNext.grid(row=1,column=3,sticky=E+W)
        recordLast.grid(row=1,column=4,sticky=E+W)

class FlightWindow(Window):
    def __init__(self,master=None,flight=None):
        Window.__init__(self,master)
        
        self.flight_obj = flight
        self.showFlight()
        
    def showFlight(self):
        # The Essentials
        ################
        outerPad = 4
        innerPad = 2
        
        self.master.title("Flying Travel Agency - Flight Details")
        self.pack(fill="both",expand=1,padx=outerPad,pady=outerPad)
        
        centerFrame = LabelFrame(self,text="Flight Result")
        centerFrame.pack(padx=outerPad,pady=outerPad)
        
        if(isinstance(self.flight_obj,Flight)):
            # Object passed into this window is a flight.
            # Therefore, unpack the variable.
            GUI_flightObj   = StringVar()
            GUI_airportDep  = StringVar()
            GUI_airportArr  = StringVar()
            GUI_airline     = StringVar()
            GUI_flightCode  = StringVar()
            GUI_depDatetime = StringVar()
            GUI_arrDatetime = StringVar()
            GUI_ticket      = StringVar()
            GUI_price       = StringVar()
            
            GUI_flightObj.set(str(self.flight_obj))
            GUI_airportDep.set(str(self.flight_obj.airportDep))
            GUI_airportArr.set(str(self.flight_obj.airportArr))
            GUI_airline.set(str(self.flight_obj.airline))
            GUI_flightCode.set(str(self.flight_obj.flightCode))
            GUI_depDatetime.set(str(self.flight_obj.depDatetime))
            GUI_arrDatetime.set(str(self.flight_obj.arrDatetime))
            GUI_ticket.set(str(self.flight_obj.ticket))
            GUI_price.set("$"+format(self.flight_obj.price,".2f"))
            
            flightObjLabel  = Label(centerFrame,textvariable=GUI_flightObj)
            airportDep      = Label(centerFrame,text="Departing From:")
            airportDep_GUI  = Label(centerFrame,textvariable=GUI_airportDep)
            airportArr      = Label(centerFrame,text="Arriving To:")
            airportArr_GUI  = Label(centerFrame,textvariable=GUI_airportArr)
            airline         = Label(centerFrame,text="Airline:")
            airline_GUI     = Label(centerFrame,textvariable=GUI_airline)
            flightCode      = Label(centerFrame,text="Flight Code:")
            flightCode_GUI  = Label(centerFrame,textvariable=GUI_flightCode)
            depDatetime     = Label(centerFrame,text="Departure Date/Time:")
            depDatetime_GUI = Label(centerFrame,textvariable=GUI_depDatetime)
            arrDatetime     = Label(centerFrame,text="Arrival Date/Time:")
            arrDatetime_GUI = Label(centerFrame,textvariable=GUI_arrDatetime)
            ticket          = Label(centerFrame,text="Ticket Type:")
            ticket_GUI      = Label(centerFrame,textvariable=GUI_ticket)
            price           = Label(centerFrame,text="Price:")
            price_GUI       = Label(centerFrame,textvariable=GUI_price)
            
            flightObjLabel.grid(row=0,column=0,columnspan=4,    padx=innerPad,pady=innerPad,sticky=N+W+E)
            airportDep.grid(row=1,column=0,                     padx=innerPad,pady=innerPad,sticky=N+W)
            airportDep_GUI.grid(row=1,column=1,                 padx=innerPad,pady=innerPad,sticky=N+W)
            airportArr.grid(row=2,column=0,                     padx=innerPad,pady=innerPad,sticky=N+W)
            airportArr_GUI.grid(row=2,column=1,                 padx=innerPad,pady=innerPad,sticky=N+W)
            airline.grid(row=3,column=0,                        padx=innerPad,pady=innerPad,sticky=N+W)
            airline_GUI.grid(row=3,column=1,                    padx=innerPad,pady=innerPad,sticky=N+W)
            flightCode.grid(row=4,column=0,                     padx=innerPad,pady=innerPad,sticky=N+W)
            flightCode_GUI.grid(row=4,column=1,                 padx=innerPad,pady=innerPad,sticky=N+W)
            depDatetime.grid(row=1,column=2,                    padx=innerPad,pady=innerPad,sticky=N+W)
            depDatetime_GUI.grid(row=1,column=3,                padx=innerPad,pady=innerPad,sticky=N+W)
            arrDatetime.grid(row=2,column=2,                    padx=innerPad,pady=innerPad,sticky=N+W)
            arrDatetime_GUI.grid(row=2,column=3,                padx=innerPad,pady=innerPad,sticky=N+W)
            ticket.grid(row=3,column=2,                         padx=innerPad,pady=innerPad,sticky=N+W)
            ticket_GUI.grid(row=3,column=3,                     padx=innerPad,pady=innerPad,sticky=N+W)
            price.grid(row=4,column=2,                          padx=innerPad,pady=innerPad,sticky=N+W)
            price_GUI.grid(row=4,column=3,                      padx=innerPad,pady=innerPad,sticky=N+W)
            
        else:
            # Object passed isn't a flight.
            # (So the list of flights is empty or somehow the wrong sort of object got in)
            warningLabel = Label(centerFrame,text="No Flight loaded! Please close this window and try again.")
            warningLabel.pack(padx=innerPad,pady=innerPad)
            