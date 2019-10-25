from tkinter import *
# To get pop-up messages you gotta be a bit wonky. Oh well.
import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog

from email.message import EmailMessage  # For creating the message to send
import email.errors                     # For debugging the message
import smtplib                          # For sending the message
import datetime as dt                   # Date functions/time/etc.

from cl_createPeople import staffList, custsList, peopleList
from cl_createPeople import Person

# Simple window class to work off of.
class Window(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master

class CommunicationsWindow(Window):
    def __init__(self,master=None):
        Window.__init__(self,master)
        # Key/Value lists for staff and customer selection
        self.contactNames   = ["Staff","Customers","All People"]
        self.contactLists   = [staffList,custsList,peopleList]
        self.currentList    = self.contactLists[0]  # Currently selected/used list of contacts to go through.
        self.chosenContacts = []                    # Expandable/dimishable list of contacts for a given message.
        
        # Email centric vars
        self.emailMessage   = EmailMessage()        # Email Message to send
        self.emailMessage["Date"]    = dt.datetime.now()
        self.emailMessage["Subject"] = ""           # Preemptively set this.
        self.attachments    = []                    # List of filename strings
        
        # SMS-centric vars (tbd)
        # IM-centric vars (tbd)
        
        # Fire main window.
        self.commWin()
        
    def commWin(self):
        # Essentials and Basics
        #######################
        outPad = 4
        inPad  = 2
        
        self.master.title("Luca's Communications Module")
        self.pack(fill="y",expand=1,padx=outPad,pady=outPad)
        
        # GUI Vars
        ##########
        # Contacts GUI vars
        GUI_currentList = StringVar()   # Which contact list we're looking at.
        GUI_currentList.set(self.currentList)
        GUI_listName    = StringVar()   # The user-friendly name of the contact list we're looking at.
        GUI_listName.set(self.contactNames[0])
        
        # Email GUI vars
        GUI_emailFrom   = StringVar()   # Message sending from.
        GUI_emailTo     = StringVar()   # Message sending to.
        GUI_emailSubject= StringVar()   # Message subject.
        GUI_emailAttach = StringVar()   # Message Attachments List
        GUI_emailText   = StringVar()   # Main message body.
        
        # SMS GUI vars
        GUI_numbersTo   = StringVar()
        
        # IM GUI vars
        GUI_handlesTo   = StringVar()
        
        # Functions
        ###########
        def callback(event):
            # Super-simple callback function for whatever.
            print(event)
        
        def contactGroups_callback(event):
            # Callback function for selecting which group of contacts
            contactList.selection_clear(0,END)
            g = contactGroups.get()
            i = contactGroups.current()
            print(g+", #"+str(i))
            
            self.currentList = self.contactLists[i]
            GUI_currentList.set(self.currentList)
            GUI_listName.set(self.contactNames[i])
            print("Now reading people from {}".format(g))
            updateRecipients()
        
        def updateRecipients(event=None):
            # Update who is in/out of a particular message.
            self.chosenContacts = []
            
            people = contactList.curselection()
            
            for p in people:
                self.chosenContacts.append(self.currentList[p])
            
            emails  = [] # List of email addresses
            phones  = [] # List of mobile numbers
            handles = [] # List of Yammer handles/usernames
            
            for cc in self.chosenContacts:
                # Update Email send List
                emails.append(cc.email+";")
                # Update SMS send list
                phones.append(cc.mobile)
                # Update IM send list.
                handles.append(cc.handle)
                
            print("Email Addresses: {}".format(emails))
            print("Phone Numbers: {}".format(phones))
            print("Yammer Handles: {}".format(handles))
            
            GUI_emailTo.set(emails)
            del self.emailMessage["To"]
            self.emailMessage["To"] = emails
            
            GUI_numbersTo.set(phones)
            GUI_handlesTo.set(handles)
            
            email_showHeaders()
            
        def contactList_selectAll():
            # Select all available contacts on the list of contacts.
            contactList.selection_set(0,END)
            updateRecipients()
        
        def contactList_selectNone():
            # Deselect all available contacts on the list of contacts.
            contactList.selection_clear(0,END)
            updateRecipients()
            
        def email_changeSubject():
            # Updates the email's Subject
            try:
                del self.emailMessage["Subject"]
                self.emailMessage["Subject"] = GUI_emailSubject.get()
            except email.errors.HeaderParseError:
                print("Header is Invalid! (HeaderParseError)")
            except IndexError:
                print("Header is Invalid! (IndexError)")
            finally:
                email_showHeaders()
            
        def email_changeFrom():
            # Updates the email's Sender/From
            try: 
                del self.emailMessage["From"]
                self.emailMessage["From"] = GUI_emailFrom.get()
            except email.errors.HeaderParseError:
                print("Header is Invalid! (HeaderParseError)")
            except IndexError:
                print("Header is Invalid! (IndexError)")
            finally:
                email_showHeaders()
        
        def email_updateContent():
            # Update the contents of the email.
            pass
            
        def email_attachFile():
            # Attaches a file to the email message.
            filepath = filedialog.askopenfilename(initialdir="/",title="Select Attachment...")
            #print(filepath)
            
            self.attachments.append(filepath)
            GUI_emailAttach.set(self.attachments)
            
            del self.emailMessage["Content-Disposition"]
            self.emailMessage.add_header("Content-Disposition","attachment",filename=filepath)
            self.emailMessage.iter_attachments()
            
            email_showHeaders()
            pass
        
        def email_clearAttach():
            # Removes a selected attachment from the email message.
            if(self.emailMessage.is_attachment()):
                print("You have attachments. Remove selected!")
                try:
                    sel = emailAttachList.curselection() # Get current selection.
                    ind = sel[0]                 # Selection index from Menu.
                    att = self.attachments[ind]  # Attachment Object before its deleted.
                    
                    # Remove entry from GUI list
                    emailAttachList.delete(ind)
                    # Remove entry from actual list
                    try: 
                        self.attachments.remove(att)
                    except ValueError:
                        print("Aw shit. Removing the attachment from the email didn't line up.")
                    # Remove entry from Email
                    
                    for part in self.emailMessage.get_all("Content-Disposition"):
                        #try:
                        print(part)
                        #except:
                        #print("Bugger.")
                    
                except IndexError:
                    # No attachment selected.
                    pass
            else:
                print("You don't have any attachments to remove.")
            email_showHeaders()
        
        def email_sendMessage():
            # Opens up Outlook via Powershell to transpose your message there.
            pass
        
        def email_showHeaders():
            # Debug function because working with email headers is a nightmare.
            # Also update the date/time on the message, because why not?
            del self.emailMessage["Date"]
            self.emailMessage["Date"] = dt.datetime.now()
            
            print(self.emailMessage.items())
            #print(self.emailMessage.keys())
            #print(self.emailMessage.values())
        
        # Widgets
        #########
        ## Frame Setup
        ##############
        commLabel   = Label(self,text="This is the communications module.\nIt uses dummy data of people (staff and customers) from the Flying Travel Agency (Project 1) to create a list of contacts which can be messaged one way or another. This is a demonstration/exploration of the communications capabilities of Python.",wraplength=600,justify=LEFT)
        
        emailImg    = PhotoImage(file=r"../img/icon_perDetails.png")
        imImg       = PhotoImage(file=r"../img/icon_Products.png")
        smsImg      = PhotoImage(file=r"../img/icon_perContacts.png")
        
        tabsFrame   = LabelFrame(self,text="Your Communications")
        tabs        = ttk.Notebook(tabsFrame)
        imTab       = Frame(tabsFrame)
        emailTab    = Frame(tabsFrame)
        smsTab      = Frame(tabsFrame)
        
        tabs.add(emailTab,text="Send Emails",image=emailImg,compound=LEFT)
        tabs.add(smsTab,text="Send SMS",image=smsImg,compound=LEFT)
        tabs.add(imTab,text="Send Instant Message",image=imImg,compound=LEFT)
        tabs.emailImg   = emailImg
        tabs.smsImg     = smsImg
        tabs.imImg      = imImg
        
        commLabel.grid(row=0,column=0,columnspan=2,     padx=inPad,pady=inPad)
        tabs.grid(row=0,column=0,                       padx=inPad,pady=inPad,sticky=N+S)
        
        contactFrame = LabelFrame(self,text="Your Contacts")
        contactFrame.grid(row=1,column=0,               padx=inPad,pady=inPad,sticky=N+S)
        tabsFrame.grid(row=1,column=1,                  padx=inPad,pady=inPad,sticky=N+S)
        
        ## Stuff that goes in 'contactFrame'
        ####################################
        # Drop-down for what group of contacts you want to communicate with.
        contactGroups = ttk.Combobox(contactFrame,values=self.contactNames)
        contactGroups.current(0)
        contactGroups.bind("<<ComboboxSelected>>",contactGroups_callback)
        
        contactScroll = Scrollbar(contactFrame,jump=1)
        contactList   = Listbox(contactFrame,height=27,width=32,listvariable=GUI_currentList,exportselection=False,
                                selectmode=MULTIPLE,activestyle="dotbox",yscrollcommand=contactScroll.set)
        contactScroll.config(command=contactList.yview)
        contactAll  = Button(contactFrame,text="Select All",command=contactList_selectAll)
        contactNone = Button(contactFrame,text="Select None",command=contactList_selectNone)
        contactList.bind("<<ListboxSelect>>",lambda e: updateRecipients(e))
        
        contactGroups.grid(row=0,column=0,columnspan=3, padx=inPad,pady=inPad)
        contactScroll.grid(row=1,column=2,              padx=inPad,pady=inPad,sticky=N+S)
        contactList.grid(row=1,column=0,columnspan=2,   padx=inPad,pady=inPad,sticky=E)
        contactAll.grid(row=2,column=0,                 padx=inPad,pady=inPad,sticky=E+W)
        contactNone.grid(row=2,column=1,                padx=inPad,pady=inPad,sticky=E+W)
        
        ## Stuff that goes in 'emailTab'
        ################################
        # From Field
        GUI_emailFrom.trace_add("write",lambda x,y,z: email_changeFrom())
        emailFromLabel      = Label(emailTab,text="From:")
        emailFrom           = Entry(emailTab,width=56,textvariable=GUI_emailFrom)
        
        # To Field
        emailToLabel        = Label(emailTab,text="To:")
        emailTo             = Entry(emailTab,width=56,textvariable=GUI_emailTo,state="readonly")
        # The emailTo field is populated dynamically as people are selected and de-selected from the list of contacts.
        
        # Subject Field
        GUI_emailSubject.trace_add("write",lambda x,y,z: email_changeSubject())
        emailSubjectLabel   = Label(emailTab,text="Subject:")
        emailSubject        = Entry(emailTab,width=56,textvariable=GUI_emailSubject)
        
        # Attachments
        # Temporarily disabled because attachments are a goddamn nightmare - and for some reason there's
        # no easy tutorial on adding/removing attachments from an email.message.EmailMessage!
        emailAttachScroll   = Scrollbar(emailTab,jump=1)
        emailAttachList     = Listbox(emailTab,height=4,width=56,listvariable=GUI_emailAttach,
                                  selectmode=SINGLE,activestyle="dotbox",yscrollcommand=emailAttachScroll.set,state=DISABLED)
        emailAttachScroll.config(command=emailAttachList.yview)
        emailAttachButt     = Button(emailTab,text="Attach File...",command=email_attachFile,state=DISABLED)
        emailAttachClear    = Button(emailTab,text="Clear Attachment",command=email_clearAttach,state=DISABLED)
        
        # Main Email Body
        emailTextLabel      = Label(emailTab,text="Message:")
        emailScroll         = Scrollbar(emailTab,jump=1)
        emailText           = Text(emailTab,height=16,width=62,wrap=WORD,yscrollcommand=emailScroll.set)
        emailScroll.config(command=emailText.yview)
        
        # Sending Buttons
        emailSend           = Button(emailTab,text="Send Email(s)")
        
        # Gridding
        emailFromLabel.grid(row=0,column=0,             padx=inPad,pady=inPad,sticky=W)
        emailFrom.grid(row=0,column=1,                  padx=inPad,pady=inPad)
        emailToLabel.grid(row=1,column=0,               padx=inPad,pady=inPad,sticky=W)
        emailTo.grid(row=1,column=1,                    padx=inPad,pady=inPad)
        emailSubjectLabel.grid(row=2,column=0,          padx=inPad,pady=inPad,sticky=W)
        emailSubject.grid(row=2,column=1,               padx=inPad,pady=inPad)
        
        emailAttachButt.grid(row=3,column=0,            padx=inPad,pady=inPad,sticky=W+E)
        emailAttachClear.grid(row=4,column=0,           padx=inPad,pady=inPad,sticky=W+E)
        emailAttachList.grid(row=3,rowspan=2,column=1,  padx=inPad,pady=inPad)
        emailAttachScroll.grid(row=3,rowspan=2,column=2,padx=inPad,pady=inPad,sticky=N+S)
        
        emailTextLabel.grid(row=5,column=0,columnspan=2,padx=inPad,pady=inPad,sticky=W)
        emailText.grid(row=6,column=0,columnspan=2,     padx=inPad,pady=inPad)
        emailScroll.grid(row=6,column=2,                padx=inPad,pady=inPad,sticky=N+S)
        
        emailSend.grid(row=7,column=0,columnspan=3,     padx=inPad,pady=inPad,sticky=W+E)
        
        ## Stuff that goes in 'imTab'
        #############################
        imComingSoon    = Label(imTab,text="Coming as soon as we figure out if Yammer has an API which is compatible with Python scripts, thus enabling the program to send messages through there!",wraplength=320,justify=LEFT)
        imComingSoon.grid(row=0,column=0,                padx=inPad,pady=inPad)
        
        ## Stuff that goes in 'smsTab'
        ##############################
        smsComingSoon   = Label(smsTab,text="Coming as soon as we figure out if ANZ has its own SMS-sending infrastructure (they sure don't grow on trees!) and if so, how to use it with Python!",wraplength=320,justify=LEFT)
        smsComingSoon.grid(row=0,column=0,               padx=inPad,pady=inPad)

root = Tk()
app = CommunicationsWindow(root)
root.resizable(width=False, height=False)
#root.geometry("640x400")
root.mainloop()
