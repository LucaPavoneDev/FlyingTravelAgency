from tkinter import *
# To get pop-up messages you gotta be a bit wonky. Oh well.
import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox

from cl_Interface import Window
from cl_Data import database as db
from gui.gui_Helpers import *

# Class for searching through tables for records with.
######################################################
class SearchWindow(Window):
    def __init__(self,master=None):
        Window.__init__(self,master)
        self.curInd    = 0                          # Current index picked for which set of DB records to go through.
                                                    # IE: Index 0 is essentially:
                                                    #("Customers", "customerList", "Customer", ["tid","pid","id","name","fname","lname","desc"] + ["contacts","address"])
                                                    # Respectively from listNames, allLists, objTypes, and the default attributes list extended by the index's additional attribs list.
        self.defaults  = db.getDefaultAttributes()  # A copy of a list of default attributes to look for in each object.
        self.listNames = db.getListNames()   # List of user-friendly Names of data-lists in DB.
        self.allLists  = db.getAllLists()    # List of program-friendly names of data-lists in DB.
                                             # Used in conjunction with db.getList("listName") function.
                                             # To specify which 'table' in the DB to check.
        self.objTypes  = db.getAllowedObjs() # List of names of allowed object classes within.
                                             # For checking against with checkObject(Object),
                                             # Which returns Class Name as String.
        self.attribs   = db.getAttributes()  # List of a list of strings of attribute names to check through an object for.
                                             # Iterated through per object to collect data.

        self.searchList= []                  # Where any search items are sent to if they match criteria.
        self.searchWindow()                  # Finally, this line runs the whole shebang.

    def searchWindow(self):
        # Window presentation variables
        outerPad = 4
        innerPad = 2

        # Change window name and prepack it.
        self.master.title("Flying Travel Agency - Search")
        self.pack(fill="both",expand=1,padx=outerPad,pady=outerPad)

        # Set up big frames for widgets.
        topFrame   = Frame(self)
        botFrame   = Frame(self)
        leftFrame  = Frame(botFrame)
        rightFrame = Frame(botFrame)

        # Big Frame packing.
        topFrame.pack(side=TOP,padx=outerPad,pady=outerPad)
        botFrame.pack(side=BOTTOM,padx=outerPad,pady=outerPad)
        leftFrame.pack(side=LEFT,padx=innerPad,pady=innerPad)
        rightFrame.pack(side=RIGHT,padx=innerPad,pady=innerPad)

        # Labelled Frames inside of the container frames
        searchFrame  = LabelFrame(topFrame,text="Search Criteria")
        resultList   = LabelFrame(leftFrame,text="Records Returned")
        resultReturn = LabelFrame(rightFrame,text="Record Data")

        # Labelled Frame Packing
        searchFrame.pack(side=TOP,padx=innerPad,pady=innerPad,fill="both")
        resultList.pack(side=RIGHT,padx=innerPad,pady=innerPad)
        resultReturn.pack(side=LEFT,padx=innerPad,pady=innerPad)

        # Setting up Controlled Variable for the Drop-down Menu and Search
        ##################################################################
        GUI_menuCurr     = StringVar() # Currently chosen item in drop-down menu
        GUI_searchString = StringVar() # Current text in search bar.
        GUI_recordData   = StringVar() # Current record data. Gets cleared/populated as need be.
        GUI_matchTally   = StringVar() # How many matches there were.
        GUI_recordTally  = StringVar() # How many records were returned.
        GUI_opt_matchWord= BooleanVar()
        GUI_opt_matchCase= BooleanVar()

        GUI_menuCurr.set(self.listNames[0])
        GUI_searchString.set("")
        GUI_recordData.set("")
        GUI_matchTally.set("0 Matches")
        GUI_recordTally.set("0 Records")
        GUI_opt_matchWord.set(False)
        GUI_opt_matchCase.set(False)

        # Define a callback function for the dropdown menu
        def menuCallback(selection):
            try:
                self.curInd = self.listNames.index(selection)
                # What this'll do is:
                print(self.curInd)
                print(self.listNames[self.curInd])
                print(self.allLists[self.curInd])
                print(self.objTypes[self.curInd])
                print(self.attribs[self.curInd])
            except ValueError:
                print("menuCallback reported ValueError: Element not found in list.")

        def searchButtonCommand(searchString=GUI_searchString.get()):
            # This function writes all the output from the Search to the record list.
            ind  = self.curInd
            name = self.listNames[ind]       # User-friendly list name.
            plist= self.allLists[ind]       # Programmer-friendly list name.
            attr = db.getDefaultAttributes() # Load default attributes.
            attr.extend(self.attribs[ind])   # Load attributes for objects within list.
            self.searchList = []             # Clear the search list of objects.

            listData.delete(0,END)           # Clear current records list.
            allMatches = 0                   # All counted data matches.
            allRecords = 0                   # All counted records.
            GUI_matchTally.set("SEARCHING...")
            GUI_recordTally.set("")

            print("SearchButtonCommand: Starting...")
            for obj in db.getList(plist):
                # To check if the record being assessed is going to be outputted.
                goesInList = False
                matches    = 0

                # Search through attributes for matching string.
                for a in attr:
                    try:
                        # Do Case Sensitivity Check
                        if(GUI_opt_matchCase.get() == 1):
                            # Lowercase all attributes, make them strings.
                            ss = str(searchString)

                            attrName = a # Get code-friendly name of attribute
                            attrText = str(getattr(obj,a)) # Get data from attribute
                        else:
                            # Lowercase all the attributes.
                            ss = str(searchString).lower()

                            attrName = a # Get code-friendly name of attribute
                            attrText = str(getattr(obj,a)).lower() # Get data from attribute

                        # Use Python's "in" word to search through attributes.
                        if(ss in attrText and goesInList == False):
                            # Show the matching attribute and its contents full.
                            goesInList = True
                            matches += 1
                            allMatches += 1
                            allRecords += 1
                            print("Match "+str(matches)+" of Record "+str(obj)+" in "+str(attrName)+", '"+str(attrText)+"'.")
                        elif(ss in attrText):
                            # Show the matching attribute only since we've already got a match.
                            matches += 1
                            allMatches += 1
                            print("Match "+str(matches)+" of Record "+str(obj)+" in "+str(attrName)+".")
                    except AttributeError:
                        # Skip that attribute since it isn't set/present in object, so continue the loop.
                        continue

                # If there's a match, it goes on on the list.
                if(goesInList == True):
                    self.searchList.append(obj)     # Add object to the list of returned objects.
                    listData.insert(END,str(obj))   # Insert an entry for that list into the GUI.
            GUI_matchTally.set(str(allMatches)+" Matches")
            GUI_recordTally.set(str(allRecords)+" Records")
            print("SearchButtonCommand: Found "+str(allMatches)+" Matches in "+str(allRecords)+" Records.")
            print("SearchButtonCommand: Finished.")

        def openSearchRecord(obj):
            # This is where presenting the record's contents matters most.
            # This is where the object is read and written into the Record Data frame.
            #print(obj)

            ind  = self.curInd
            attr = db.getDefaultAttributes() # Load default attributes.
            attr.extend(self.attribs[ind])   # Load attributes for objects within list.

            # Delete everything from Record Attribute List:
            recData.delete(0,END)
            recData.insert(END,str(obj)+" is a "+checkObject(obj)+".")

            # Scroll through object
            for attribute in attr:
                try:
                    # Cycle through names of attributes.
                    # Get values of attributes which exist.
                    # And add them to the list.
                    an = attribute
                    at = getattr(obj,an)

                    if(type(at) is dict):
                        #print("It's a dictionary!")
                        dind = 0
                        for key, value in at.items():
                            #print(key)
                            #print(value)
                            textLine = "DICT #"+str(dind)+" "+an+": "+str(key)+": "+str(value)
                            recData.insert(END,str(textLine))
                            dind += 1
                    elif(type(at) is list):
                        #print("It's a list!")
                        lind = 0
                        for value in at:
                            textLine = "LIST #"+str(lind)+" "+an+": "+str(value)
                            recData.insert(END,str(textLine))
                            lind += 1
                    else:
                        #print("It's not a dictionary or list.")
                        textLine = str(an)+": "+str(at)
                        recData.insert(END,str(textLine))

                except AttributeError:
                    # Attribute doesn't exist. Continue.
                    continue

        # Search Options/Entry Frame
        ############################
        # for Labelframe: searchFrame
        searchEntry  = Entry(searchFrame,textvariable=GUI_searchString,width=24)
        searchEntry.bind("<Return>",lambda searchString: searchButtonCommand(GUI_searchString.get()))
        searchDrop   = OptionMenu(searchFrame,GUI_menuCurr,*self.listNames,command=menuCallback)
        searchButton = Button(searchFrame,text="Search In...",command=lambda: searchButtonCommand(GUI_searchString.get()))

        matchTally   = Label(searchFrame,textvariable=GUI_matchTally,anchor="w")
        recordTally  = Label(searchFrame,textvariable=GUI_recordTally,anchor="w")

        # Search Options
        lab_matchWord    = Label(searchFrame,text="Match Whole Word:")
        lab_matchCase    = Label(searchFrame,text="Case Sensitive:")
        opt_matchWord    = Checkbutton(searchFrame,variable=GUI_opt_matchWord)
        opt_matchCase    = Checkbutton(searchFrame,variable=GUI_opt_matchCase)

        # Gridding widgets for Search Frame
        searchEntry.grid(row=0,column=0,columnspan=2,padx=innerPad,pady=innerPad,sticky="ns")
        searchButton.grid(row=0,column=2,padx=innerPad,pady=innerPad,sticky="nsew")
        searchDrop.grid(row=1,column=2,padx=innerPad,pady=innerPad,sticky="nsew")

        matchTally.grid(row=1,column=0,padx=innerPad,pady=innerPad,sticky="wns")
        recordTally.grid(row=1,column=1,padx=innerPad,pady=innerPad,sticky="wns")

        # Options Gridding
        lab_matchWord.grid(row=0,column=4,padx=innerPad,pady=innerPad)
        opt_matchWord.grid(row=0,column=5,padx=innerPad,pady=innerPad)
        lab_matchCase.grid(row=1,column=4,padx=innerPad,pady=innerPad)
        opt_matchCase.grid(row=1,column=5,padx=innerPad,pady=innerPad)

        # Record List Frame
        ###################
        # for Labelframe: resultList
        listScroll  = Scrollbar(resultList,jump=1)
        listData    = Listbox(resultList,height=20,width=50,selectmode="SINGLE",
                              activestyle="dotbox",yscrollcommand=listScroll.set)
        listScroll.config(command=listData.yview)
        listData.bind("<Double-1>",lambda x: openSearchRecord(getRecord(self.searchList,getCurSel(listData),listData)))

        listScroll.pack(side=RIGHT,fill="y")
        listData.pack(side=RIGHT)

        # Record Data Frame
        ###################
        # for Labelframe: resultReturn
        recScrollY  = Scrollbar(resultReturn,jump=1)
        recScrollX  = Scrollbar(resultReturn,jump=1,orient=HORIZONTAL)
        recData     = Listbox(resultReturn,height=19,width=80,selectmode="SINGLE",
                              activestyle="dotbox",yscrollcommand=recScrollY.set,xscrollcommand=recScrollX.set)
        recScrollY.config(command=recData.yview)
        recScrollX.config(command=recData.xview)

        recData.grid(row=0,column=0)
        recScrollY.grid(row=0,column=1,sticky=N+S)
        recScrollX.grid(row=1,column=0,sticky=E+W)
        