import setup
import numpy as np
#import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb


class Table(tk.Frame):
    def __init__(self,master,df,length,func):
        tk.Frame.__init__(self,master)
        self.df = df
        self.func = func
        self.length = length
        self.df = self.df.sort_values(by=self.df.columns[0])
        self.init_window()

    def init_window(self):
        self.cframe = tk.Frame(self)
        self.cols = {}
        self.ltitle = {}
        self.lboxes = {}
        self.value = None
        self.scroll = tk.Scrollbar(self.cframe)
        self.scroll.grid(row=1,column=self.df.shape[1],sticky='nes')
        for i,col in enumerate(self.df.items()):
            self.cols[i] = tk.StringVar(value=list(col[1]))
            self.ltitle[i] = tk.Label(self.cframe,text=col[0],anchor='w',
                                      relief='groove',justify='left')
            self.ltitle[i].grid(row=0,column=i,sticky='new')
            self.ltitle[i].name = col[0]
            self.ltitle[i].bind("<Button-1>",self.sort)
            self.lboxes[i] = tk.Listbox(self.cframe,listvariable=self.cols[i],
                                        exportselection=0,height=self.length,borderwidth=0,
                                        yscrollcommand=self.scroll.set)
            self.lboxes[i].bind("<<ListboxSelect>>",self.boxSelect)
            self.lboxes[i].bind("<Double-1>",self.open)
            self.lboxes[i].bind("<MouseWheel>",self.mwheel)
            self.lboxes[i].grid(row=1,column=i,sticky='new')
        self.ltitle[0].config(text=("▼ " + self.ltitle[0].name),bg='lightgrey')
        self.sortby = self.ltitle[0]
        self.sortasc = True
        self.scroll.config(command=self.vscroll)
        self.cframe.grid(column=0,row=0,padx=10,pady=5)
        self.cframe.rowconfigure(1,weight=1)

    def vscroll(self, *args):
        for i in self.lboxes:
            self.lboxes[i].yview(*args)

    def mwheel(self,event):
        for i in self.lboxes:
            self.lboxes[i].yview("scroll",int(-event.delta/120),"units")
        return "break"

    def clear(self,*args):
        for i in self.lboxes:
            self.lboxes[i].selection_clear(0,'end')

    def reset(self):
        self.clear()
        self.sortasc = False
        self.ltitle[0].event_generate("<Button-1>")
        self.value = None

    def boxSelect(self,event):
        self.value = event.widget.curselection()[0]
        self.clear()
        for i in self.lboxes:
            self.lboxes[i].selection_set(self.value)

    def open(self,event):
        self.func(self.df.index[self.value])
        self.clear()
        self.value = None

    def remove(self,ID):
        self.df.drop(ID,inplace=True)
        self.refresh()

    def update(self,ID,line):
        self.df.loc[ID] = line
        self.refresh()

    def refresh(self):
        for i,col in enumerate(self.df.items()):
            self.cols[i].set(list(col[1]))

    def sort(self,event):
        if event.widget != self.sortby:
            self.sortby.config(text=self.sortby.name,bg='SystemButtonFace')
        if event.widget == self.sortby and self.sortasc is True:
            self.sortasc = False
            a = "▲ "
        else:
            self.sortasc = True
            a = "▼ "
        self.df = self.df.sort_values(by=event.widget.name,ascending=self.sortasc)
        self.refresh()
        event.widget.config(text=(a + event.widget.name),bg='lightgrey')
        self.sortby = event.widget
        

if __name__ == '__main__':
    import database as db
    db.makeDBs()
    root = tk.Tk()
    app = Table(root,setup.ALLDBS['Program'].df,5)
    app.pack()
    app.mainloop()
        
