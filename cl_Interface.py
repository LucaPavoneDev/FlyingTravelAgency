# Oh boy. This is gonna be _fun_!
# Might as well throw the whole lot of tkinter in.
from tkinter import *
# To get pop-up messages you gotta be a bit wonky. Oh well.
import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox
#from pillow import Image, ImageTK

# Finally, the specifics for each of my modules as needed:
from cl_Data import database as db
import datetime as dt

#dbCon = sqlite3.connect("./travelAgency.db")
#dbCur = dbCon.cursor()

# Get the roots and window containers figured out ahead of time.

# Define basic window class.
############################
class Window(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master

from gui.gui_IntroWin import IntroWindow

# Making it go. Go for it, man!
###############################
# Set window size.
# Run the thing.
root = Tk()
app = IntroWindow(root)
root.resizable(width=False, height=False)
root.geometry("640x400")
root.mainloop()

#dbCon.commit()
#dbCon.close()