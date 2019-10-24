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

# Define database window and data functions.
############################################
class DatabaseWindow(Window):
    def __init__(self,master=None,listName=""):
        # Listname is just some additional text data. You'll see what its for.
        Window.__init__(self,master)
        self.master = master

        # Do the database/list name check before proceeding.
        if(checkDB(listName) == True):
            # Database check returned True.
            print("List '"+str(listName)+"' in database found! Opening...")
            # Start the Data window stuff.
            self.databaseWindow(getattr(db,listName),listName)
            self.editView = None
        else:
            # Database check returned False. Delete self to save memory.
            print("List in database not found. Aborting window creation and deleting self.")
            del self

    def databaseWindow(self,li,lis=""):
        # Show off the database.
        # Define textual stuff ahead of time.
        titleText = "Flying Travel Agency - Database"
        dataText = "Database Viewer"
        if(lis != ""):
            # titleText += " - Viewing "+lis
            dataText += " - Viewing '"+lis+"'."
        # Define a title for the window.
        self.master.title(titleText)

        # Pre-pack the 'base' of the database.
        self.pack(fill="both",expand=1)

        # Create a sub-label below the title, just in case.
        dataLabel = Label(self,text=dataText)
        dataLabel.pack(side="top",fill="none")

        # Create a frame to put the data view in
        # and pack it as being 'above', therefore below the label.
        lFrame = LabelFrame(self,text="Records in List")# List Frame

        # Create a scrolling list box of options.
        # Note that its parent object is the just-created 'lFrame'
        # and not the 'self', because self is a frame too.
        dataScroll = Scrollbar(lFrame,jump=1)
        dataList = Listbox(lFrame,height=20,width=50,selectmode="SINGLE",
                           activestyle="dotbox",yscrollcommand=dataScroll.set)
        # Bind a clcik to the data list to fire off the data viewing.
        dataList.bind("<Double-1>",lambda x: createDataView(getRecord(li,getCurSel(dataList),dataList)))
        # And configure the scroll wheel beside the data list.
        dataScroll.config(command=dataList.yview)

        # Start populating the dropdown, by iterating through the list
        # END is a tkinter constant for listboxes which puts new entries on the end.
        for i in li:
            dataList.insert(END,str(i)+" ("+checkObject(i)+")")
        #print(dataList.size())

        # Create a frame to put the buttons below the list and record view in
        bFrame = LabelFrame(self,text="Commands")# Buttons Frame

        # Create buttons for the frame, to go below the data entries. Go on the left side.
        newRec      = Button(bFrame,text="New",underline=0)
        openRec     = Button(bFrame,text="Open",underline=0,command=lambda: createDataView(getRecord(li,getCurSel(dataList),dataList)))
        editRec     = Button(bFrame,text="Edit",underline=0)
        prinRec     = Button(bFrame,text="Print",underline=0)
        delRec      = Button(bFrame,text="Delete",underline=0)

        # File navigation buttons, go on the right side.
        # These buttons create a data view for the first record, the one previous to the current selection
        # the one ahead of current selection, and one for the last record in the list.
        # None of this will fire off if the records are empty.
        firstRec    = Button(bFrame,text="First",command=lambda: createDataView(getRecord(li,(0,0),dataList)))
        prevRec     = Button(bFrame,text="Previous",command=lambda: createDataView(getRecord(li,getCurSel(dataList),dataList,offset=-1)))
        nextRec     = Button(bFrame,text="Next",command=lambda: createDataView(getRecord(li,getCurSel(dataList),dataList,offset=1)))
        endRec      = Button(bFrame,text="End",command=lambda: createDataView(getRecord(li,(dataList.size()-1,0),dataList)))

        # Pack up Data List and Buttons Widgets.
        for widget in [newRec, openRec, editRec, prinRec, delRec]:
            widget.pack(side="left",fill="x")
        for widget in [endRec, nextRec, prevRec, firstRec]:
            widget.pack(side="right",fill="x")

        # Pack the list and scrollbar for it
        # Then pack the button bar.
        dataScroll.pack(side="right",fill="y")
        dataList.pack(side="right",fill="both")
        bFrame.pack(side="bottom",fill="x")
        lFrame.pack(side="left",fill="both")

        # Start creating the Data viewing Frame
        dFrame = LabelFrame(self,text="Record View",width=320)# Data Frame
        dFrame.pack(side="right",fill="both")

        # StringVar is a special tkinter variable.
        # its weird. Either way, this is where our object's info will be written to.
        # Whenever this 'stringvar' gets changed, it'll update wherever its told to read.
        objText = StringVar()
        objText.set("No Record Loaded.")
        objInfo = Label(dFrame,anchor=NW,width=50,wraplength=350,justify=LEFT,textvariable=objText)
        objInfo.pack(side="right",fill="both",expand=True)

        # Also I wanted to add a scrollbar to the label, but Labels don't do scrolling...
        '''
        #objScroll = Scrollbar(dFrame,jump=1)
        #objScroll.pack(side="right",fill="y")
        #objScroll.
        '''

        def createDataView(obj):
            # Get an object type, then create a data view for it.
            # This works after GetRecord() does its thing and returns the 'obj'.
            # Blank the text in the data object text box.
            objText.set("No Record Loaded.")
            newText = str("")

            def checkAndAddToAttributes():
                # 'a' is the set of attributes to check for and update based on
                # a data object's type from checkObject(obj) below (obj is already specified).
                ty = checkObject(obj)
                ob = db.getAllowedObjs()
                at = db.getAttributes()
                try:
                    ai = ob.index(ty)
                    #print("Attr Index: "+str(ai))
                    newAttr = at[ai]
                    #print("New Attr: "+str(newAttr))
                    return newAttr
                except ValueError:
                    # If for some reason grabbing attributes fails, we have a fallback...
                    return [""]

            # Try the try/except method of getting attributes from an object.
            # First, hard-coding all the most important stuff in.
            attributes = db.getDefaultAttributes()
            # Then adding all the shiny new attributes we got based on the object class.
            attributes.extend(checkAndAddToAttributes())

            # Then go through all the attributes and try/except in a loop.
            for attr in attributes:
                try:
                    # Cycle through the names of attributes.
                    # Get the values of the attributes which exist.
                    attrName = attr
                    attrText = getattr(obj,attr)
                    newText += str(attrName)+": "+str(attrText)+"\n"
                except AttributeError:
                    # If an attribute doesn't exist, continue at it.
                    continue

            # Change the object text to what's been found.
            objText.set(newText)

        # Pre-load the first record in the database into the view.
        createDataView(getRecord(li,(0,0),dataList))