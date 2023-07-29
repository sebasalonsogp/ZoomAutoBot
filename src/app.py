from tkinter import *
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import re
import threading

#Settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#Frame
gui = ctk.CTk()

app_width = 720 #app size
app_height = 480

screen_width = gui.winfo_screenwidth() 
screen_height = gui.winfo_screenheight() 

x = (screen_width/2) -(app_width/2) #x centered
y = (screen_height/2) - (app_height/2) #y centered

gui.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}') #app size - centered
gui.title("Zoom Auto-Join App")

#grid configuration
gui.grid_columnconfigure(0,weight=1)
gui.grid_columnconfigure(1,weight=1)
gui.grid_rowconfigure(0,weight=1)
gui.grid_rowconfigure(1,weight=1)
gui.grid_rowconfigure(2,weight=1)


#Subframes
    #keybinds frame
keybind_frame = ctk.CTkFrame(gui,height=430,width=360,fg_color="gray10")
keybind_frame.grid(column=0,row=0,rowspan=3,sticky="nsew",padx=5,pady=5)

    #meetings frame
meetings_frame = ctk.CTkFrame(gui,height=100,width=360,fg_color="gray10")
meetings_frame.grid(row=0,column=1,sticky="nsew",padx=5,pady=5)

        #meetings frame grid config
meetings_frame.grid_columnconfigure(0,weight=1)
meetings_frame.grid_columnconfigure(1,weight=1)
meetings_frame.grid_columnconfigure(2,weight=1)
meetings_frame.grid_columnconfigure(3,weight=1)
meetings_frame.grid_columnconfigure(4,weight=1)
meetings_frame.grid_rowconfigure(0,weight=1)
meetings_frame.grid_rowconfigure(1,weight=1)


    #meetings list frame
meetings_list_frame = ctk.CTkScrollableFrame(gui,height=330,width=360,fg_color="gray25")
meetings_list_frame.grid(row=2,column=1,sticky="nsew",padx=5,pady=5)

    #run_button frame
run_button_frame= ctk.CTkFrame(gui,height=50,width=720,fg_color="gray10")
run_button_frame.grid(row=3,columnspan=2,sticky="nsew",padx=5,pady=5)


#Widgets

#keybinds_frame widgets 
def is_digit(P):    #only digits
    return P.isdigit() or ""

is_digit=(gui.register(is_digit),'%P')

#Only one character in the entry box
def one_char(P):
    if P == "Enter the camera key" or P == "Enter the leave key":
        return True
    P = str(P)
    if P == "":
        return True
    elif len(P) == 1:
        return True
    else:
        return False

one_char=(gui.register(one_char),'%P')

#Leave Keybind
leavelabel = ctk.CTkLabel(keybind_frame,text="Leave Keybind")
leavelabel.pack(padx=5,pady=5)
leavekb = ctk.CTkEntry(master=keybind_frame,placeholder_text="Enter the leave key",validate="key",validatecommand=one_char)
leavekb.pack(padx=10,pady=10)

#Camera Keybind
cameralabel= ctk.CTkLabel(keybind_frame, text="Camera Keybind")
camerakb = ctk.CTkEntry(master=keybind_frame,placeholder_text="Enter the camera key", validate="key",validatecommand=one_char)

#camera delay
camdelaylabel = ctk.CTkLabel(keybind_frame,text="Delay (seconds)")
cameradelay = ctk.CTkEntry(keybind_frame,validate="key",validatecommand=is_digit)

def on_click():
    if camera_checkbox.get()==1:
        cameralabel.pack(padx=5,pady=10)
        camerakb.pack(padx=10,pady=10)
        camdelaylabel.pack(padx=10,pady=10)
        cameradelay.pack(padx=10,pady=10)
    elif camera_checkbox.get()==0:
        cameralabel.pack_forget()
        camerakb.pack_forget()
        camdelaylabel.pack_forget()
        cameradelay.pack_forget()

camera_checkbox = ctk.CTkCheckBox(keybind_frame,text="Auto Turn On Camera",command=on_click)
camera_checkbox.pack(padx=10,pady=10)

#meetings_frame widgets
#validation methods
def validate_time_input(P):
    time_pattern = r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'  
    return bool(re.match(time_pattern,P))

def inputting_time(P): #only allow users to input nums and ':'
    return re.match(r'^[\d:]*$',P) is not None and len(P)<=5

validate_input_time = gui.register(inputting_time)
validate_time = gui.register(validate_time_input)

#commands
meetings_list = [] #type : list of dictionaries
num_meetings=0


def extract_zoom_id(link):
    pattern = r"/j/(\d+)\?pwd"
    match = re.search(pattern, link)
    if match:
        return match.group(1)
    else:
        CTkMessagebox(gui,title="Warning",message="Could not extract a meeting ID from the link. Ensure the link is correct/working",icon="warning")
        return "Check Link Validity"

def add_meeting():
    import re
    global meetings_list,num_meetings

    link = meeting_link.get()
    start_time = meeting_start_time.get()
    end_time = meeting_end_time.get()

    if not validate_time_input(start_time) or not validate_time_input(end_time):
        CTkMessagebox(gui,icon="cancel",title="Invalid Input",message="Time must be inputted in 24-hr HH:MM format.")
        return
    
    if link == "":
        CTkMessagebox(gui,icon="cancel",title="Invalid Input",message="You must input a link!")
        return
    
    #add actual meeting data to list
    new_meeting = {"link": link, "start_time": start_time, "end_time": end_time }
    meetings_list.append(new_meeting)

    #add meeting to the GUI

    #extract the zoom meeting ID for display
    

    zoom_id = extract_zoom_id(link)

    link_entry = ctk.CTkLabel(meetings_list_frame,text=zoom_id,bg_color="gray10",justify='center',width=175)
    link_entry.grid(row=num_meetings+3,column=0,ipadx=50,pady=2)

    start_entry = link_entry = ctk.CTkLabel(meetings_list_frame,text=start_time,bg_color="gray10",justify='center',width=75)
    start_entry.grid(row=num_meetings+3,column=1,pady=2)

    end_entry = link_entry = ctk.CTkLabel(meetings_list_frame,text=end_time,bg_color="gray10",justify='center',width=75)
    end_entry.grid(row=num_meetings+3,column=2,pady=2)
    
    remove_button = ctk.CTkButton(meetings_list_frame,text="X",command=lambda: remove_meeting(link,start_time,end_time),width=5,fg_color="red2",hover_color="red3")
    remove_button.grid(row=num_meetings+3,column=3,pady=2)

    meeting_link.delete(0, 'end')
    meeting_start_time.delete(0, 'end')
    meeting_end_time.delete(0, 'end')

    #print("added", meetings_list)
    num_meetings += 1

#meetings_frame_list remove button frame
def remove_meeting(link, start, end):
    global meetings_list, num_meetings

    # Find the index of the meeting to be removed based on link, start, and end time
    index_to_remove = None
    for i, meeting in enumerate(meetings_list):
        if meeting["link"] == link and meeting["start_time"] == start and meeting["end_time"] == end:
            index_to_remove = i
            break

    if index_to_remove is not None:
        # Remove the meeting data from the list
        del meetings_list[index_to_remove]

        # Remove the labels and delete button from the GUI
        row_index = index_to_remove + 3
        link_labels = meetings_list_frame.grid_slaves(row=row_index, column=0)
        start_labels = meetings_list_frame.grid_slaves(row=row_index, column=1)
        end_labels = meetings_list_frame.grid_slaves(row=row_index, column=2)
        remove_buttons = meetings_list_frame.grid_slaves(row=row_index, column=3)

        for label in link_labels + start_labels + end_labels:
            label.grid_forget()

        for button in remove_buttons:
            button.grid_forget()

        # Update the row indices of the labels and buttons after removal
        for i in range(row_index + 1, num_meetings + 3):
            link_labels = meetings_list_frame.grid_slaves(row=i, column=0)
            start_labels = meetings_list_frame.grid_slaves(row=i, column=1)
            end_labels = meetings_list_frame.grid_slaves(row=i, column=2)
            remove_buttons = meetings_list_frame.grid_slaves(row=i, column=3)

            for label in link_labels:
                label.grid(row=i - 1, column=0, pady=2)

            for label in start_labels:
                label.grid(row=i - 1, column=1, pady=2)

            for label in end_labels:
                label.grid(row=i - 1, column=2, pady=2)

            for button in remove_buttons:
                button.grid(row=i - 1, column=3, pady=2)

        #print("removed", meetings_list)
        num_meetings -= 1




#create custom treeview headers
header = [(0, "Meeting ID"),(1,"Start"), (2, "End")]
for x,label in header:
    entry = ctk.CTkEntry(meetings_list_frame, justify='center')
    entry.insert(0, label)
    entry.configure(state='readonly')
    if label.lower() == 'meeting id':
        entry.configure(width=175,fg_color="RoyalBlue1",border_color="black")
        entry.grid(row=0, column=x, ipadx=50, pady=5,padx=2.5)
    else:
        entry.configure(width=75,fg_color="RoyalBlue1",border_color="black")
        entry.grid(row=0, column=x,pady=5,padx=2.5)

#meeting_link
meeting_link_label=ctk.CTkLabel(meetings_frame,text="Meeting Link:",anchor="e")
meeting_link_label.grid(row=0,column=0,padx=5,pady=5,sticky="e")
meeting_link = ctk.CTkEntry(meetings_frame,width=400)
meeting_link.grid(row=0,column=1,columnspan=5,padx=5,pady=5)

#meeting start time
meeting_start_time_label = ctk.CTkLabel(meetings_frame,text="Start Time:")
meeting_start_time_label.grid(row=1,column=0,padx=5,pady=5)
meeting_start_time = ctk.CTkEntry(meetings_frame,validate="key",validatecommand=(validate_input_time,"%P"),placeholder_text="00:00-23:59",width=50)
meeting_start_time.grid(row=1,column=1,padx=10,pady=10)

#meeting_end time
meeting_end_time_label = ctk.CTkLabel(meetings_frame,text="End Time:")
meeting_end_time_label.grid(row=1,column=2,padx=5,pady=5)
meeting_end_time = ctk.CTkEntry(meetings_frame,validatecommand=(validate_input_time,"%P"),validate="key",placeholder_text="00:00-23:59",width=50)
meeting_end_time.grid(row=1,column=3,padx=5,pady=5)

#add meeting button
add_meeting_button = ctk.CTkButton(meetings_frame,text="Add Meeting",command=add_meeting)
add_meeting_button.grid(row=1,column=4,padx=5,pady=5)

def extract_ID(link):
    pattern = r"/j/(\d+)\?pwd"
    match = re.search(pattern, link)
    if match:
        return match.group(1)
    else:
        return link


stop_script = threading.Event() #event handler
process = None #global process popup

#scheduler
def run_onclick():
    import sched, time
    global meetings_list, stop_script

    gui.protocol("WM_DELETE_WINDOW", lambda: None) #ensure main window cannot close while script is running

    stop_script.clear() #ensure it is set to false for every run

    scheduler = sched.scheduler(time.time,time.sleep)

    ##aquiring inputs for script
    script_leavekb = leavekb.get()
    script_camkb = camerakb.get()
    script_delay = lambda: 0 if not cameradelay.get() == "" else cameradelay.get()
    script_camcheckbool = camera_checkbox.get()

    #ensure neccesary keybinds are inputted
    if script_leavekb == "" or script_leavekb is None or (script_camcheckbool == 1 and (script_camkb == "" or script_camkb is None)):
        CTkMessagebox(gui,title="Missing Keybind",message="You must have all neccesary keybinds inputted!",icon="warning")
        return
    if meetings_list is None or meetings_list == []: #ensure there are meetings
        CTkMessagebox(gui,title="Missing Schedule",message="You must have at least one meeting",icon="warning")
        return

    #sort meeting and ensure its chronolical
    sort_check_start = sorted(meetings_list, key=lambda x: x["start_time"])
    sort_check_end = sorted(meetings_list, key=lambda x: x["end_time"])

    if sort_check_start != sort_check_end:
        CTkMessagebox(gui,title="Invalid Schedule", message="Your schedule must not have overlapping times!", icon="warning")
        return
    
    sorted_sched = sort_check_start
    #print("\nSorted Schedule", sorted_sched)

    #start schedule thread
    schedule_thread = threading.Thread(target=run_schedule,args=(scheduler, script_camkb, script_delay, script_leavekb, script_camcheckbool,sorted_sched))
    schedule_thread.start()


def end_script():#end script with button
    global process, stop_script
    import time
    stop_script.set() #tell script to stop running
    if process:
        #print("Closing window")
        process.destroy() #close window when stop is clicked
    time.sleep(2)
    gui.protocol("WM_DELETE_WINDOW", gui.quit)

def close_popup(): # Close popup after script runs successfully
    global process
    if process:
        process.destroy()
    CTkMessagebox(gui, title="Success!", message="Script is done running. Schedule complete", icon="check")
    gui.protocol("WM_DELETE_WINDOW", gui.quit)

#script
def join(link, script_camkb, script_delay, script_camcheckbool,in_meeting):
    import webbrowser, time
    from pynput.keyboard import Controller,Key
    
    in_meeting.configure(text="In meeting", text_color="green2")
    #print("joining...")
 
    keyboard = Controller()
    webbrowser.open(link)
    if script_camcheckbool == 1:
        time.sleep(script_delay) 
        with keyboard.pressed(Key.alt):
            keyboard.press(script_camkb)

def leave(script_leavekb,in_meeting):
    import time
    from pynput.keyboard import Controller,Key
    in_meeting.configure(text="Not in meeting", text_color="red2")
    #print("leaving...")
    keyboard = Controller()
    with keyboard.pressed(Key.alt):
        keyboard.press(script_leavekb)

    time.sleep(5) #in case if there is an additional leave pop-up
    keyboard.press(Key.enter)


#thread to run the schedule.
def run_schedule(scheduler, script_camkb,script_delay,script_leavekb,script_camcheckbool,sorted_sched):
    global stop_script, process#, meetings_list
    import time
    from datetime import datetime
    #from script import join, leave

    #print("\nRunning current schedule:", sorted_sched)

    #show process running window
    process = ctk.CTkToplevel()
    process.geometry(f'{300}x{150}+{(screen_width-300)//2}+{(screen_height-150)//2}')
    process.title("Process running...")
    process.protocol("WM_DELETE_WINDOW", lambda: None)
    process.grab_set()

    stop = ctk.CTkButton(process,text="Stop",command=end_script,fg_color="red4",hover_color="red2").pack(pady=5)
    current_meeting = ctk.CTkLabel(process)
    in_meeting = ctk.CTkLabel(process,text="Not in meeting",text_color="red3")
    in_meeting.pack(pady=2)

    #next_meeting = ctk.CTkLabel(process) ##TODO? maybe allow to show next meeting and time until completion in another thread?


    #schedule each meeting
    for meeting in sorted_sched:

        if stop_script.is_set(): #check to see if stop button is clicked
            return

        #print("\nCurrently on meeting:", meeting)

        link = meeting["link"]
        start = meeting["start_time"]
        end = meeting["end_time"]
        
        current_string = "Current Meeting\n" + "ID: " + extract_ID(link) + "\nStart: " + start + "\nEnd: " + end
        current_meeting.configure(text=current_string)
        current_meeting.pack(pady=5)
        

        start_time = datetime.strptime(start, "%H:%M")
        end_time = datetime.strptime(end, "%H:%M")
        now = datetime.now().replace(year=1900, month=1, day=1)

        delay_start = (start_time - now).total_seconds() #start time
        delay_end = (end_time - now).total_seconds() #leave time
        
        #print("Time until start\n",delay_start)
        
        scheduler.enterabs(time.time()+delay_start, 1, join, argument=(link, script_camkb, script_delay, script_camcheckbool,in_meeting))
        scheduler.enterabs(time.time()+delay_end, 1, leave, argument=(script_leavekb,in_meeting))
        scheduler.run() ##TODO maybe change to use after() and recursive function to pop() from list rather than not use inside the forloop
        
    
    
    close_popup() 
    
    


#run button
run = ctk.CTkButton(master=run_button_frame,text="Run",command=run_onclick, text_color="white", fg_color="dark green", hover_color="green")
run.pack(side='bottom',padx=10,pady=10)

#info popup
CTkMessagebox(font=("Arial", 18),title="Important Information",message="1. Zoom must be open and logged in as neccesary.\n\n2. You must manually set your keybinds and they must have 'ALT' as the prefix (e.g. ALT+[Key])\n\n3. Time must be in 24-hr HH:MM format.\n4. Ensure your meeting times are not overlapping and that they all fall within one 24-hr day.")

#Run gui
gui.mainloop()
