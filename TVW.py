from tkinter import Tk, Frame, Label, Text, Entry, Listbox, Button, Scrollbar
from tkinter import StringVar, IntVar, END, N, S, E, W, X, Y, BOTH 
from tkinter import INSERT
import tkinter.ttk as ttk
import time
import threading
from ReadDict import readData
from ReadDict import writeData
from CompareInfo import updateData
import pdb
import math



showLocation = "Show Names.txt"
showInfoLocation = "info.txt"
# how often should the auto update run in seconds (3600 = 1 hour)
update_timer = 3600
# how often should the progress bar update in seconds
progress_interval = .1



class timer():
    start_time = 0
    end_time = 0

    def start(self):
        self.start_time=time.time()
    #

    def end(self):
        self.end_time=time.time()
        taken = self.end_time - self.start_time
        print('Timer took ','{:6.3f}'.format(taken),'s' )
##
        


class test(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        
        self.label = Label(self, text='Hello')
        self.label.grid(row=0, column=0)

        self.details=Details(self)
        self.details.grid(row=5, column=0)

        
class Details(Frame):
    def __init__(self, master):
    ## Variables ##
        Frame.__init__(self, master)
        self.master = master
        self.title = StringVar()
            # status shows as: Running, Returning Series, ''
        self.status = StringVar()
        self.prev_ep_name = StringVar()
        self.prev_ep = StringVar()
        self.next_ep = StringVar()
        self.next_ep_name = StringVar()
        self.next_air = StringVar()
        self.prev_air = StringVar()

        # Widgets
            #create
        self.title_label = Label(self, textvariable=self.title, font = "Courier 16 bold")
        self.status_label = Label(self, textvariable=self.status)

        self.next_title=Label(self, text="Next Episode")
        self.next_ep_frame = Frame(self, highlightbackground="#B0B0B0", highlightcolor="#B0B0B0", highlightthickness=1, width=150, height=100, bd= 0)
        self.next_ep_name_label = Label(self.next_ep_frame, textvariable=self.next_ep_name)
        self.next_ep_label = Label(self.next_ep_frame, textvariable=self.next_ep)

        self.prev_title=Label(self, text="Previous Episode")
        self.prev_ep_frame = Frame(self, highlightbackground="#B0B0B0", highlightcolor="#B0B0B0", highlightthickness=1, width=150, height=100, bd= 0)
        self.prev_ep_name_label = Label(self.prev_ep_frame, textvariable=self.prev_ep_name)
        self.prev_ep_label = Label(self.prev_ep_frame, textvariable=self.prev_ep)

        self.next_air_label = Label(self.next_ep_frame, textvariable=self.next_air)
        self.prev_air_label = Label(self.prev_ep_frame, textvariable=self.prev_air)

        self.out_of_date_label = Label(self, text="Out of Date Episodes")
        self.out_of_date = Frame(self, highlightbackground="#B0B0B0", highlightthickness=1)

        # Configure
#        self.next_ep_frame.grid_propagate(False)
#        self.prev_ep_frame.grid_propagate(False)
        # Layout

        self.title_label.grid(row=0, column=0, columnspan=2, sticky=E+W)
        self.status_label.grid(row=1, column=0, columnspan=2, sticky=E+W)

        self.prev_title.grid(row=2, column=0, sticky=E+W)
        self.prev_ep_frame.grid(row=3, column=0, sticky=E+W)
        self.prev_ep_name_label.grid(row=0,column=0,sticky=E+W)
        self.prev_ep_label.grid(row=1,column=0,sticky=E+W)
        self.prev_air_label.grid(row=2, column=0, sticky=S+E+W)

        self.next_title.grid(row=2, column=1, sticky=E+W, ipady=5, ipadx=5)
        self.next_ep_frame.grid(row=3, column=1, sticky=S+E+W)
        self.next_ep_name_label.grid(row=0,column=0,sticky=E+W)
        self.next_ep_label.grid(row=1,column=0,sticky=E+W)
        self.next_air_label.grid(row=2, column=0, sticky=S+E+W)
        
        self.out_of_date_label.grid(row=7, column=0, columnspan=2, sticky=E+W)
        self.out_of_date.grid(row=8, column=0, columnspan=2, sticky=S+E+W)

        self.title.set('No Show Slected')
    #

    def updateDetails(self):
        #######  Show Data ##
        # Title
        # Airs On
        # Status
        # Prev-Name
        # Prev-Date
        # Prev-Season
        # Prev-Episode
        # Next-Name
        # Next-Date
        # Next-Season
        # Next-Episode
        # Out-of-Date
        #####################

        #######  Show Labels ##
        # self.status
        # self.next_ep
        # self.next_ep_name
        # self.prev_ep
        # self.prev_ep_name
        # self.next_air
        ###########

        #clear Data from last eps
        self.out_of_date.destroy()
        self.out_of_date = Frame(self, highlightbackground="#B0B0B0", highlightthickness=1)
        self.out_of_date.grid(row=8, column=0, columnspan=2, sticky=S+E+W)

        # Get data from master
        showData = self.master.showData
        cur_show = self.master.cur_show

        # set status color #
            #maybe implement icons to display next to name?#
        
        self.status.set(showData[cur_show]['Status'])
        self.title.set(showData[cur_show]['Title'])

        self.next_ep_name.set(showData[cur_show]['Next-Name'])
        self.next_ep.set('S'+showData[cur_show]['Next-Season']+"E"+showData[cur_show]['Next-Episode'])
        self.next_air.set(showData[cur_show]['Next-Date'])
                
        self.prev_ep_name.set(showData[cur_show]['Prev-Name'])
        self.prev_ep.set('S'+showData[cur_show]['Prev-Season']+"E"+showData[cur_show]['Prev-Episode'])
        self.prev_air.set(showData[cur_show]['Prev-Date'])

        ood_buttons ={}
        count=0;
        gr=0;
        gc=0;
        for eps in self.master.showData[self.master.cur_show]['Out-of-Date']:

            # pass each button's text to a function
            action = lambda x = eps: self.master.removeOOD(x)
            # create the buttons and assign to episode:button-object dict pair
            ood_buttons[eps] = Button(self.out_of_date, text=eps, command=action)
            if count<2:
                gr=0
            else:
                gr=math.floor(count/2)

            if (count % 2) == 0:
                gc=0
            else:
                gc=1
            ood_buttons[eps].grid(row=gr,column=gc)
            count+=1
        #
    #
#








class TVW(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master)
        ## Variables ##
        self.grid()
        self.master = master
        master.title("TVW")
        self.showList = readData(showLocation)
        if self.showList=='':self.showList=[]
        self.showData = readData(showInfoLocation)
        if self.showData=='':self.showData={}
        self.auto_updater = True
        self.run_thread = True
        self.cur_show = ''

        self.auto_progress_text = StringVar()
        self.update_progress_text = StringVar()

        self.auto_update()
        self.forceUpdate()

        ## Specialty Progress Bar ##
            # I somewhat understand this, but pulled offline to make it work
        self.style = ttk.Style(master)
            # add label in the layout
        self.style.layout('text.Horizontal.TProgressbar', 
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}), 
              ('Horizontal.Progressbar.label', {'sticky': ''})])
            # set initial text
            #got arround using this to change the label of all status bars, while wanting to change each individually
            #oh well, it works
        self.style.configure('text.Horizontal.TProgressbar', text='')

        ##  Widgets  ##
            #Details
        self.details=Details(self)
            #Out Of Date Buttons, to be set per show
        self.ood_buttons=[]

        self.list_frame = Frame(self)
            #list Box#
        self.list_scrollbar = Scrollbar(self.list_frame, orient="vertical")
        self.show_lb = Listbox(self.list_frame, width=30, height=15, yscrollcommand=self.list_scrollbar.set)
        self.show_lb.bind('<<ListboxSelect>>', self.showSelect)
        self.list_scrollbar.config(command=self.show_lb.yview)
            #Add to List#
        self.add_entry = Entry(self.list_frame, text="Enter Show Name")
        self.add_button = Button(self.list_frame, text="+", command=self.newShow)
        self.delete_show = Button(self.list_frame, text="Delete This Show", command=self.deleteShow)
            #updates#
        self.update_frame = Frame(self, bg='#D0D0D0')
        self.update_align = Frame(self.update_frame, bg='#D0D0D0')
        self.update_button = Button(self.update_align, text='Refresh', command=self.forceUpdate)
        self.auto_progress = ttk.Progressbar(self.update_align, style='text.Horizontal.TProgressbar', variable=self.auto_progress_text, length=100, mode='determinate')
        self.update_progress = ttk.Progressbar(self.update_align, style='text.Horizontal.TProgressbar', variable=self.update_progress_text, length=100, mode='determinate')
        

        ## LAYOUT  ##
            #details#
        self.details.grid(row=0, column=1, sticky=N+E+W, padx=5, pady=5)
            #show list#
        self.list_frame.grid(row=0, column=0, rowspan=2)
        self.show_lb.grid(row=0, column=0, sticky=W)
        self.list_scrollbar.grid(row=0, column=1, sticky=N+S)
        self.add_entry.grid(row=1, column=0, sticky = E+W, pady=2)
        self.add_button.grid(row=1, column=1, sticky = W)
        self.delete_show.grid(row=2, column=0, columnspan=2, sticky=E+W)
            #update#
        self.update_frame.grid(row=1, column=1, sticky=S+E+W)
        self.update_align.pack(anchor=E)
        self.update_button.grid(row=0,column=1, sticky=E)
        self.auto_progress.grid(row=0,column=0, sticky=E)
            # have this appear only when running update
        #self.update_progress.grid(row=1,column=1, sticky=E)
        

    ### Aditional Functions ###
    # get show selection from Listbox
    def showSelect(self, evt):
        select = self.show_lb.curselection()
        show = self.showList[int(select[0])]
        self.cur_show=show
        self.details.updateDetails()

            
    # remove an out of date episode. Be up to date.    
    def removeOOD(self, ep):
        print("remove", ep)
        self.showData[self.cur_show]['Out-of-Date'].remove(ep)
        self.fillListBox()
        self.details.updateDetails()
        writeData(showInfoLocation, self.showData)
   
        
    # Add new name to list of shows, update showLocation file, Run scrubbing script for new show, rerun FillListBox
    def newShow(self):
        #show_name = simpledialog.askstring("Name of new show","Please input Show Name")
        show_name = self.add_entry.get()
        if show_name!='':
            self.update([show_name])
                

    # progress bar in lower right.  always repeats.  When it completes, run update function
    def auto_update(self):
        def thread_auto_update():
            try:
                while self.run_thread:
                    x=0
                    while (x<=update_timer and self.auto_updater):
                        x+=progress_interval
                        time.sleep(progress_interval)
                        self.auto_progress.step(100/(update_timer/progress_interval))
                        self.style.configure('text.Horizontal.TProgressbar', text='{:.0f} Seconds'.format(update_timer-x))
                    if self.run_thread!=False:
                        self.update(self.showList)
                        self.auto_updater=True
                    else:
                        print('Ending Thread')
            except:
                    print("Error in thread.  Likely program ended while it was running")
        threading.Thread(target=thread_auto_update).start()

    # ends the current thread on auto_update, immediately forcing an update.  Will reassign and restart in auto_update
    def forceUpdate(self):
        self.auto_updater = False;

    def killUpdate(self):
        self.auto_updater = False;
        self.run_thread = False;

        
    # run all steps to update data.  Scrub info from web, update list/new show times, ect
    def update(self, show_list):
        # Setup Variables
        self.add_button['state']='disabled'
        self.update_button['state']='disabled'
        self.update_progress.grid(row=0,column=0, sticky=W)
        progress=(100/(1+len(show_list)))
        self.update_progress["value"]=progress
        self.style.configure('text.Horizontal.TProgressbar', text="Updating")
        temp_show_data={}

        
        #run Update on List of Shows
        for show in show_list:
            # check if program has closed
            if self.run_thread != True:break

            #Get data for Each Show, check if 404 or missing in list
            self.style.configure('text.Horizontal.TProgressbar', text=show)
            
            showInfo = updateData([show])

            if showInfo == "404":
                print("Server Error on '",show,"', getting 404")
            else:
                temp_show_data[show] = showInfo[show]
                if show not in self.showList:
                    self.showList.append(show)
                    writeData(showLocation, self.showList)
            self.update_progress.step(progress)

        #Writing data and updating List
        #self.style.configure('text.Horizontal.TProgressbar', text='Updating List')
        self.showData = temp_show_data
        writeData(showInfoLocation, self.showData)
        self.fillListBox()
        self.update_progress.step(progress)

        #Update is complete, user can edit things again
        self.add_button['state']='normal'
        self.update_button['state']='normal'
        self.update_progress.grid_forget()

        
    # fill in the list box elements, along with Out of Date Episode Count
    def fillListBox(self):
	####  while updating list, check for out of date episodes, and include number for size next to name ####
        self.show_lb.delete(0,'end')
        showCount=1
        state='none'
        for show in self.showList:
            clip = ''
            clip+= show
            try:
                ood = len(self.showData[show]['Out-of-Date'])
                if ood>0:
                    clip+= ' ('+str(ood)+')'
                    state='ood'
            except:
                print('Error Getting Out-of-Date on '+show)
            self.show_lb.insert(showCount,clip)
            if state!='none':
                self.show_lb.itemconfig(showCount-1, foreground="red")
            showCount+=1
            state='none'

    #delete show from all logs.  Remove from show names and from info
    def deleteShow(self):
        try:
            self.showList.remove(self.cur_show)
            del self.showData[self.cur_show]
            writeData(showLocation, self.showList)
            writeData(showInfoLocation, self.showData)
        except:
            print("No Show Specified.  Cannot delete.")

        self.fillListBox()


###########  Figure out why thread will not end if update is running  ############
##
def on_closing():
    my_gui.killUpdate()
    time.sleep(1) #give a literal second to let the thread close 
    root.destroy()

#########  Begin Program  ###########

root = Tk()
root.resizable(False, False)
my_gui = TVW(root)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
