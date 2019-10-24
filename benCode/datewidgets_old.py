import calendar as cal
import tkinter as tk
from tkinter import ttk
from datetime import date, time, datetime
from dateutil.relativedelta import relativedelta

class Datebox(tk.Frame):
    '''A custom widget for selecting dates in TKinter, which
    can be any valid calendar date between 1990 and 2030.
    Defined with optional parameters master (for where
    the widget is placed, initial (the date the widget initially
    shows, defaulting to today if not specified or None),
    and func (if defined and not none, should be a function
    to be called when the date is modified).'''
    def __init__(self, master=None,initial=None,func=None):
        super().__init__(master)
        self.state = 'normal'
        self.config(borderwidth=1,relief='sunken')
        self.func = None
        if initial == None:
            self.date = date.today()
        else:
            self.date = initial
        self.dVal, self.mVal, self.yVal = tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.dateReset()

        self.dBox = tk.Entry(self, textvariable=self.dVal, width=2, borderwidth=0)
        self.mBox = tk.Entry(self, textvariable=self.mVal, width=2, borderwidth=0)
        self.yBox = tk.Entry(self, textvariable=self.yVal, width=4, borderwidth=0)

        self.dBox.bind("<FocusIn>",self.boxClick)
        self.mBox.bind("<FocusIn>",self.boxClick)
        self.yBox.bind("<FocusIn>",self.boxClick)

        self.dBox.bind("<FocusOut>",self.validate)
        self.mBox.bind("<FocusOut>",self.validate)
        self.yBox.bind("<FocusOut>",self.validate)

        dSep = tk.Label(self, text='/', borderwidth=0, bg='white')
        mSep = tk.Label(self, text='/', borderwidth=0, bg='white')

        self.button = tk.Button(self, text='▐▓▌',width=2,height=1,command=self.datepick)

        self.dBox.grid(row=0,column=0,sticky='nesw')
        dSep.grid(row=0,column=1,sticky='nesw')
        self.mBox.grid(row=0,column=2,sticky='nesw')
        mSep.grid(row=0,column=3,sticky='nesw')
        self.yBox.grid(row=0,column=4,sticky='nesw')
        self.button.grid(row=0,column=5,sticky='nesw')
        self.func = func

    def boxClick(self,event):
        event.widget.selection_clear()
        event.widget.selection_range(0,'end')

    def dateReset(self):
        self.dVal.set(self.date.strftime('%d'))
        self.mVal.set(self.date.strftime('%m'))
        self.yVal.set(self.date.strftime('%Y'))
        if self.func != None:
            self.func()
        
    def validate(self,*args):
        date = self.get()
        if (date == None) or (date.year<1990) or (date.year>2030): #if you want to change the hardcoded date range, change these values
            self.dateReset()
            return False
        else:
            self.date = date
            self.dateReset()
            return True

    def datepick(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty()+self.winfo_height()
        test = mthMenu(x,y,self.date,self)
        self.wait_window(test)
        self.dateReset()

    def insert(self, data):
        '''Function to set the date of the datebox. Requires one parameter,
        data, which must be a date object'''
        if type(data) is date:
            self.date = data
            self.dateReset()
        else:
            return

    def getString(self):
        '''Function that, called on the datebox, returns the current value
        of the datebox conteints as a string in the format DD/MM/YYYY'''
        data = self.dVal.get() + '/' + self.mVal.get() + '/' + self.yVal.get()
        return data

    def get(self):
        '''Function that, called on the datebox, returns the current value
        as a date object'''
        try:
            y = int(self.yVal.get())
            m = int(self.mVal.get())
            d = int(self.dVal.get())
            return date(y, m, d)
        except ValueError:
            return None

    def enable(self,state='normal'):
        '''Changes all widgets in the datebox to enabled.'''
        def changestate(widget):
            if widget.winfo_children:
                for w in widget.winfo_children():
                    w.config(state=state)
                    changestate(w)
        changestate(self)

    def disable(self):
        '''Changes all widgets in the datebox to disabled'''
        self.enable('disabled')

    def bindToChildren(self, trigger, command):
        for w in self.children.values():
            w.bind(trigger, command)
