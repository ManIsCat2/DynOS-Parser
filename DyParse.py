import tkinter as tk
from tkinter import filedialog
import os
import DynosMain

file_path=''

root = tk.Tk()
root.title("DyParse v1.0")
w,h=560,300
root.geometry("%dx%d"%(w,h))
root.maxsize(w, h)
root.minsize(w, h)
root.resizable(False, False)
icon_image = tk.PhotoImage(file='gui/ico.png')
root.iconphoto(False, icon_image)

opt_tex = tk.BooleanVar()
opt_actor = tk.BooleanVar()
opt_actor.set(True)
opt_writetex = tk.BooleanVar()

my_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
my_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

def MenuOpenFile():
    global file_path
    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=(
            ('DynOS Binary', '*.bin *.tex'),
            ('All files', '*.*')
        )
    )
    if file_path:
        label.config(text="%s" % os.path.basename(file_path))
    else:
        label.config(text="No file selected")

def DynosRun():
    global file_path
    global opt_actor
    global opt_tex
    actor = opt_actor.get()
    texture = opt_tex.get()
    extract = actor or texture
    if actor and texture:
        texture=False
    DynosMain.main(file=file_path,
        actor=actor,
        texture=texture, 
        extract=extract)

button = tk.Button(my_frame, text="Open file", command=MenuOpenFile)
button.pack(padx=10, pady=10,ipadx=5,ipady=5, anchor="nw",side=tk.LEFT)

label = tk.Label(my_frame, text="No file selected")
label.pack(pady=15, anchor="ne",side=tk.LEFT)

checkbox = tk.Checkbutton(my_frame, text="Decompile bin", variable=opt_actor)
checkbox2 = tk.Checkbutton(my_frame, text="Decompile tex", variable=opt_tex)
#checkbox3 = tk.Checkbutton(my_frame, text="Write tex (needs png)", variable=opt_writetex)
checkbox.pack(pady=1, anchor="e", padx=40)
checkbox2.pack(pady=1, anchor="e", padx=40)
#checkbox3.pack(pady=1, anchor="e", padx=3)

run = tk.Button(root, text="Run DyParse", command=DynosRun)
run.pack(pady=10,ipadx=50,ipady=5)

root.mainloop()