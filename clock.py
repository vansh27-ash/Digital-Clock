''' C l o c k : - S t o p w a t c h , T i m e r , C a l e n d a r '''

import tkinter as tk 
from tkinter.ttk import Notebook
from calendar import TextCalendar
from datetime import datetime
from threading import Thread
from time import sleep, asctime
from tkinter.messagebox import showinfo, askyesno

'''---------------------------------------------------------ALL IMPORTS DONE--------------------------------------------'''

mainwin = tk.Tk()       # our main window
mainwin.title('C L O C K')

icon = tk.PhotoImage(file = 'clock.png') # select any image and pass file path here
mainwin.iconphoto(1,icon)     # if throwing error then no icon can be preferred 

mainwin.geometry('900x650+50+10'), mainwin.resizable(0, 0)
win = Notebook(mainwin) # window for multiple windows


def gettime(second):   # this in common with 2
    '''Returns time in hrs : min : sec format for time taken in seconds'''
    hrs, minu, sec = second//3600, (second %
                                    3600)//60, ((second % 3600) % 60) % 60
    return f'{str(hrs).zfill(2)} : {str(minu).zfill(2)} : {str(sec).zfill(2)}'


'''----------------------------------------------------- MAKE DIFFERENT WINDOWS ----------------------------------------'''

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> C L O C K <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#


def moveon():
    '''Continues showing time till program runs'''
    try:    # as exception occurs when appliction is closed i.e when mainwin is destroyed it also occurs in other windows too
        while True:
            label_for_time.config(
                text=f'{datetime.now().hour} : {datetime.now().minute} : {datetime.now().second}')
            if datetime.now().hour == 0 and datetime.now().minute == 0 and datetime.now().second == 0: #12 bjte hi
                lftd = asctime().split()
                label_for_DateandDay.config(text=f'{lftd[2]} {lftd[1]} {lftd[4]} {dict_day[lftd[0]]}')
            sleep(0.99)
    except RuntimeError:
        pass


clock_tab = tk.LabelFrame(win, text='            DATE AND TIME             ', font=(
    'Courier new', 30, ('underline','italic')), bg='black', fg='cyan')
frame_for_time = tk.LabelFrame(clock_tab)
label_for_time = tk.Label(frame_for_time, text=f'{datetime.now().hour} : {datetime.now().minute} : {datetime.now().second}',
                          font=('Courier new', 30, 'underline'), fg='cyan', bg='black', width=30, height=4)
label_for_time.pack()
frame_for_time.place(x=60, y=50)
lftd = asctime().split()  # list for time data
frame_for_DateandDay = tk.LabelFrame(clock_tab)
dict_day = {'Mon':'Monday','Tue':'Tuesday','Wed':'Wednesday','Thu':'Thursday','Fri':'Friday','Sat':'Saturday','Sun':'Sunday'}
label_for_DateandDay = tk.Label(frame_for_DateandDay, text=f'{lftd[2]} {lftd[1]} {lftd[4]} {dict_day[lftd[0]]}',
         font=('Courier new', 30, 'underline'), fg='cyan', bg='black', width=30, height=4)
label_for_DateandDay.pack()
frame_for_DateandDay.place(x=60, y=300)
Thread(target=moveon).start()
clock_tab.pack(fill='both', expand=1)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> C A L E N D A R <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#


def changeleft():
    '''See previous month'''
    global month, year
    month -= 1
    if month == 0:
        year -= 1
        month = 12
    text_for_calendar = my_calendar.formatmonth(year, month, w=5, l=2)
    cal_mess.config(text=text_for_calendar)


def changeright():
    '''See next month'''
    global month, year
    month += 1
    if month == 13:
        year += 1
        month = 1
    text_for_calendar = my_calendar.formatmonth(year, month, w=5, l=2)
    cal_mess.config(text=text_for_calendar)


calendar_tab = tk.Frame(win)
calendar_tab.pack(fill='both', expand=1)
time_now = datetime.now()
my_calendar = TextCalendar()
year = time_now.year
month = time_now.month
text_for_calendar = my_calendar.formatmonth(year, month, w=5, l=2)

cal_mess = tk.Message(calendar_tab, text=text_for_calendar, font=(
    'Courier new', 20, 'bold'), bg='black', fg='cyan')
cal_mess.pack(fill='both', expand=1)

tk.Button(cal_mess, text='<', font=('arial', 20, 'bold'), bg='black',
          fg='cyan', command=changeleft).place(x=80, y=50)

tk.Button(cal_mess, text='>', font=('arial', 20, 'bold'), bg='black',
          fg='cyan', command=changeright).place(x=800, y=50)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> T I M E R <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#


def change_to_new_time():
    '''Confirm to change time of already running timer'''
    ans = askyesno('ARE YOU SURE ?', 'Would you like to change the time ?')
    if ans:
        globals()['stop_timer'] = 1
        settime()


def start(timer_time):
    '''Start Countdown'''
    # to avoid thraeds can be used once error
    if stop_timer:
        b1.config(command=not_passed_time)
    else:
        b1.config(command=time_already_running)

    def clr():
        time_up_label.config(text='')
    try:
        for time_left in range(timer_time, 0, -1):
            timer_label.config(text=gettime(time_left)), sleep(0.99)
            if globals()['stop_timer']:
                break
        else:
            globals()['stop_timer'] = 1
            timer_label.config(text='00 : 00 : 00')
            time_up_label.config(text='TIME UP')
            b2.config(command=settime)
            timer_tab.after(10000, clr)
            mainwin.bell()  # to produce sound
    except RuntimeError:
        pass


def settime():
    '''Set time for timer'''
    global sec_to_take, min_to_take, hrs_to_take

    def submit():
        global timer_time
        globals()['stop_timer'] = 0
        timer_time = hrs_to_take*3600+min_to_take*60+sec_to_take
        thread_for_timer = Thread(target=start, args=([timer_time]))
        timer_label.config(text=gettime(timer_time))
        b1.config(command=thread_for_timer.start)
        b2.config(command=change_to_new_time)
        frame.destroy()

    def secl():
        global sec_to_take
        sec_to_take -= 1
        if sec_to_take == -1:
            sec_to_take = 59
        sec_label.config(text=sec_to_take)

    def secr():
        global sec_to_take
        sec_to_take += 1
        if sec_to_take == 60:
            sec_to_take = 0
        sec_label.config(text=sec_to_take)

    def minl():
        global min_to_take
        min_to_take -= 1
        if min_to_take == -1:
            min_to_take = 59
        min_label.config(text=min_to_take)

    def minr():
        global min_to_take
        min_to_take += 1
        if min_to_take == 60:
            min_to_take = 0
        min_label.config(text=min_to_take)

    def hrsl():
        global hrs_to_take
        hrs_to_take -= 1
        if hrs_to_take == -1:
            hrs_to_take = 0
        hrs_label.config(text=hrs_to_take)

    def hrsr():
        global hrs_to_take
        hrs_to_take += 1
        hrs_label.config(text=hrs_to_take)

    hrs_to_take, min_to_take, sec_to_take = 0, 0, 0
    frame = tk.Toplevel(mainwin)
    frame.title('SET TIME HERE'), frame.resizable(0, 0)
    frame.geometry('350x200+50+20'), frame.config(background='black')
    hrs_frame = tk.LabelFrame(frame, text='HRS', font=(
        'Courier new', 15, 'italic'), bg='black', fg='cyan')
    hrs_frame.pack(padx=30, side='left')
    min_frame = tk.LabelFrame(frame, text='MIN', font=(
        'Courier new', 15, 'italic'), bg='black', fg='cyan')
    min_frame.pack(side='left')
    sec_frame = tk.LabelFrame(frame, text='SEC', font=(
        'Courier new', 15, 'italic'), bg='black', fg='cyan')
    sec_frame.pack(padx=30, side='left')
    tk.Button(sec_frame, text='\u2191', font=('Courier new', 15, 'italic'), bg='black',
              fg='cyan', command=secr).pack(padx=5, pady=2)
    tk.Button(min_frame, text='\u2191', font=('Courier new', 15, 'italic'), bg='black',
              fg='cyan', command=minr).pack(padx=5, pady=2)
    tk.Button(hrs_frame, text='\u2191', font=('Courier new', 15, 'italic'), bg='black',
              fg='cyan', command=hrsr).pack(padx=5, pady=2)
    sec_label = tk.Label(sec_frame, text='0', font=(
        'Courier new', 20, 'italic'), bg='black', fg='cyan')
    min_label = tk.Label(min_frame, text='0', font=(
        'Courier new', 20, 'italic'), bg='black', fg='cyan')
    hrs_label = tk.Label(hrs_frame, text='0', font=(
        'Courier new', 20, 'italic'), bg='black', fg='cyan')
    sec_label.pack(padx=5, pady=2)
    min_label.pack(padx=5, pady=2)
    hrs_label.pack(padx=5, pady=2)
    tk.Button(sec_frame, text='\u2193', font=('Courier new', 15, 'italic'), bg='black',
              fg='cyan', command=secl).pack(padx=5, pady=2)
    tk.Button(min_frame, text='\u2193', font=('Courier new', 15, 'italic'), bg='black',
              fg='cyan', command=minl).pack(padx=5, pady=2)
    tk.Button(hrs_frame, text='\u2193', font=('Courier new', 15, 'italic'), bg='black',
              fg='cyan', command=hrsl).pack(padx=5, pady=2)
    tk.Button(frame, text='DONE', font=('Courier new', 15, 'italic'),
              bg='black', fg='cyan', command=submit).pack(side='left')
    frame.mainloop()


def not_passed_time():
    '''Shows the message when time not given and start button is pressed'''
    showinfo('INFO', 'YOU HAVEN\'T PASSED TIME YET')


def time_already_running():
    '''Shows the message when pressing start when timer is already running'''
    showinfo('INFO', 'YOU HAVE ALREADY PASSED TIME')


stop_timer = 0

timer_tab = tk.LabelFrame(win, text='Bell sound will be heard in order to inform >> TIME UP',
                          font=('Courier new', 20, ('underline','italic')), bg='black', fg='cyan')
time_show_timer = tk.LabelFrame(timer_tab, text='TIME LEFT', font=(
    'Courier new', 20, ('italic','underline')), fg='cyan', bg='black')
time_show_timer.place(x=150, y=50)

timer_label = tk.Label(time_show_timer, text='00 : 00 : 00', font=(
    'Courier new', 25, 'italic'), fg='cyan', bg='black', height=5, width=30)
timer_label.pack(fill='both', expand=1)

time_up_label = tk.Label(timer_tab, text='', font=(
    'Courier new', 50, 'italic'), fg='cyan', bg='black')
time_up_label.place(x=250, y=300)


b1 = tk.Button(timer_tab, text='START', font=('Courier new', 20,
                                              'italic'), fg='cyan', bg='black', command=not_passed_time)
b1.place(x=120, y=450)

b2 = tk.Button(timer_tab, text='SET TIME', font=('Courier new', 20, 'italic'),
               fg='cyan', bg='black', command=settime)
b2.place(x=580, y=450)
timer_tab.pack(fill='both', expand=1)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> S T O P W A T C H <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#


def startthread():
    '''Start the thread which starts stopwatch here itself'''
    Thread(target=starts).start()


def starts():
    '''Start the stopwatch'''
    global j
    j, sec = 0, 0  # here I kept j so that in gui we have a button to stop it by making j=1
    try:
        while not j:
            time = gettime(sec)
            stop_label.config(text=time)
            sec += 1
            sleep(0.99)
        last_record.config(text='LAST RECORDED :- '+time)
        stop_label.config(text='00: 00 : 00')
    except RuntimeError:
        pass


def stop():
    '''Stop the Stopwatch'''
    global j
    j = 1


stopwatch_tab = tk.LabelFrame(win, text='Start>>start and Stop>>stop [ON STOPPING AUTOMATICALLY RESETS]',
                              font=('Courier new', 18, ('underline','italic')), bg='black', fg='cyan')
time_show_stop = tk.LabelFrame(stopwatch_tab)
time_show_stop.place(x=180, y=50)

stop_label = tk.Label(time_show_stop, text='00 : 00 : 00', font=(
    'Courier new', 30, 'italic'), fg='cyan', bg='black', width=20, height=4)
stop_label.pack()

last_record = tk.Label(stopwatch_tab, text='LAST RECORDED :- 00 : 00 : 00',
                       font=('Courier new', 25, 'italic'), fg='cyan', bg='black')
last_record.place(x=200, y=300)

tk.Button(stopwatch_tab, text='START', font=('Courier new', 20, 'italic'),
          fg='cyan', bg='black', command=startthread).place(x=120, y=450)
tk.Button(stopwatch_tab, text='STOP', font=('Courier new', 20, 'italic'),
          fg='cyan', bg='black', command=stop).place(x=620, y=450)
stopwatch_tab.pack(fill='both', expand=1)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#

'''----------------------------------------------- ADDING THE WINDOWS TO WIN ---------------------------------------------'''

win.add(clock_tab, text='                              Clock                                      ')
win.add(calendar_tab,text='                           Calendar                                   ')
win.add(timer_tab, text='                               Timer                                     ')
win.add(stopwatch_tab,text='                          Stopwatch                                  ')
win.pack(expand=1, fill='both')
mainwin.mainloop()

''''''''''''''''''''''''''''''''''''''''''''''''' T H E ** E N D'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
