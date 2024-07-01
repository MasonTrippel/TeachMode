import tkinter as tk
import logJointValues as ljv
import move
import time
import threading
from tkinter import messagebox, simpledialog, filedialog
import os
from PIL import ImageTk, Image
#start recording
def start():
    
    ljv.begin(entries['x'].get(), entries['y'].get(), entries['z'].get(), entries['rx'].get(), entries['ry'].get(), entries['rz'].get())
    
#stop recording
def stop():
    ljv.stop()

#using threading to allow for the start and stop functions to run concurrently
def start_thread():
    start_thread = threading.Thread(target=start, daemon=True)
    start_thread.start()

    # Create a StringVar
    time_text = tk.StringVar()
    time_text.set("Data Collection Starting In 10 Seconds")

    # Create the label with the StringVar
    time_label = tk.Label(root, textvariable=time_text)
    time_label.grid(row=middle_row+2, column=1,padx=(150,20))
    root.update()

    for i in range(9, -1, -1):
        time.sleep(1)
        # Update the StringVar
        time_text.set("Data Collection Starting In " + str(i) + " Seconds")
        root.update()

    time.sleep(1)
    time_label.destroy()
    root.update()

def stop_thread():
    stop_thread = threading.Thread(target=stop)
    stop_thread.start()
    
#move robot through the taught positions
def move_through_positions(loopCount = "1", filepath="robot_positions.txt", speed = 0.05):
    if not threading.active_count() > 1:
        if loopCount == "":
            messagebox.showinfo("Warning","Please enter a loop count.")
            return
        if int(loopCount) > 200:
            messagebox.showinfo("Warning", "Loop count cannot exceed 200.")
            return
        elif filepath == "robot_positions.txt":   
            move.move(loop_count=int(loopCount), speed=speed)
            return
        else:
            move.move(int(loopCount), filepath)
            return
    else:   
        print("Please stop the data collection before moving through positions.")
        return
#dont allow non-integer values in the loop count input
def validate_input(*args):
    value = loop_count_value.get()
    if not value.isdigit():
        value = value[:-1]
        loop_count_value.set(value)
def runCustomPositions(loop_count):
    filepath = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("text files","*.txt"),("all files","*.*")))
    move_through_positions(loop_count, filepath)

def save_positions():
    user_input = simpledialog.askstring("Input File Name", "Please enter a name for the position file:")
    ljv.save_positions(user_input + ".txt")


root = tk.Tk()
root.title("Teach Mode Tool")  # Set the window title
root.geometry("700x300")  # Set the window size
configuration_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eagle_composites_logo.ico")
root.iconbitmap(configuration_file_path)  # Set the window icon
configuration_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eagle_composites_logo.jpg")
img = Image.open(configuration_file_path)
photo = ImageTk.PhotoImage(img)
root.wm_iconphoto(False, photo)  # Set the window icon
# Add a title label
tk.Label(root, text="Free Axes", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, sticky='w')

labels = ["x", "y", "z", "rx", "ry", "rz"]
entries = {}
options = ['0', '1']

for i, label in enumerate(labels):
    tk.Label(root, text=label, font=("Helvetica",12)).grid(row=i+1, column=0)  # Adjust the row index to account for the title label
    entries[label] = tk.IntVar()  # Use IntVar for Checkbutton
    tk.Checkbutton(root, variable=entries[label]).grid(row=i+1, column=1,sticky='w')  # Create a Checkbutton

middle_row = len(labels) // 2
# Add "Loop Count" label and number input
loop_count_value = tk.StringVar()
loop_count_value.trace('w', validate_input)
tk.Label(root, text="Loop Count").grid(row=middle_row+2, column=2,padx=(0,20))
loop_count = tk.Entry(root, textvariable=loop_count_value)
loop_count.grid(row=middle_row+3, column=2)

speed_value = tk.StringVar()
speed_value.set("0.05")
speed_value.trace('w', validate_input)
tk.Label(root, text="Speed (m/s)").grid(row=middle_row+4, column=2,padx=(0,20))
speed = tk.Entry(root, textvariable=speed_value)
speed.grid(row=middle_row+5, column=2)

tk.Label(root, text="Teach Positions",font=("Helvetica", 14, "bold")).grid(row=middle_row -1, column=1,padx=(150,0))
tk.Button(root, text="Start", command=start_thread, height=2, width=10).grid(row=middle_row, column=1, padx=(150, 20))
tk.Button(root, text="Stop", command=stop_thread, height=2, width=10).grid(row=middle_row + 1, column=1, padx=(150, 20))
tk.Button(root, text="Save Positions", command=save_positions, height=2, width=10).grid(row=middle_row + 2, column=1, padx=(150, 20))


tk.Label(root, text="Move Robot Through Positions",font=("Helvetica", 14, "bold")).grid(row=middle_row - 1,sticky='w', column=2,padx=(50,0))
tk.Button(root, text="Start Move", command=lambda: move_through_positions(loopCount=loop_count.get(), speed=speed.get()),height=2, width=10).grid(row=middle_row, column=2, padx=(0,20))
tk.Button(root, text="Start Move with File", command=lambda: runCustomPositions(loop_count.get(),speed=speed.get()),height=2, width=20).grid(row=middle_row+1, column=2, padx=(0,20))

messagebox.showinfo("Warning","Before Starting the Recording please place the robot in automatic mode and then go the the \"Move\" Tab on the pendant and use the \"Allign\" feature. Then place the robot back into Remote mode.")
root.mainloop()

