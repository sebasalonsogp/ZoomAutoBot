import tkinter as tk
import customtkinter as ctk

def zoombot():
    print("test")

#Settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#Frame
gui = ctk.CTk()
gui.geometry("720x480")
gui.title("Zoom Auto-Join Script")

#UI Elements

keybind_frame = ctk.CTkFrame(gui)
keybind_frame.pack(side='left')

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
cameralabel= ctk.CTkLabel(keybind_frame, text="Camera Keybind")
cameralabel.pack(padx=5,pady=10)
camerakb = ctk.CTkEntry(master=keybind_frame,placeholder_text="Enter the camera key", validate="key",validatecommand=one_char)
camerakb.pack(padx=10,pady=10)


leavelabel = ctk.CTkLabel(keybind_frame,text="Leave Keybind")
leavelabel.pack(padx=5,pady=5)
leavekb = ctk.CTkEntry(master=keybind_frame,placeholder_text="Enter the leave key",validate="key",validatecommand=one_char)
leavekb.pack(padx=10,pady=10)


meetings_frame = ctk.CTkFrame(gui)
meetings_frame.pack(side='right')

num_meetings = 0
def increase():
    global num_meetings
    num_meetings = num_meetings+1
    meeting_num_display.configure(text=num_meetings)

def decrease():
    global num_meetings
    if num_meetings > 0:
        num_meetings = num_meetings-1
        meeting_num_display.configure(text=num_meetings)

meeting_num_display = ctk.CTkLabel(meetings_frame,text=num_meetings)
meeting_num_display.pack(padx=10,pady=10)

meeting_num_increase = ctk.CTkButton(master=meetings_frame,text="+",command=increase,width=10,height=10)
meeting_num_increase.pack(padx=5,pady=5)

meeting_num_decrease =ctk.CTkButton(master=meetings_frame,text="-",command=decrease,width=10,height=10)
meeting_num_decrease.pack(padx=5,pady=5)

test = meeting_num_display.cget("text")
print(test)
for i in range(int(meeting_num_display.cget("text"))):
    print(i)




run = ctk.CTkButton(master=gui,text="Run",command=zoombot, text_color="white", fg_color="dark green", hover_color="green")
run.pack(side='bottom',padx=10,pady=10)


#Run gui
gui.mainloop()