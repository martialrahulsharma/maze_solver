# from tkinter import *
# root=Tk()
# frame=Frame(root,width=300,height=300)
# frame.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)
# canvas=Canvas(frame,bg='red',width=300,height=300,scrollregion=(0,0,500,500))
# hbar=Scrollbar(frame,orient=HORIZONTAL)
# hbar.pack(side=BOTTOM,fill=X)
# hbar.config(command=canvas.xview)
# vbar=Scrollbar(frame,orient=VERTICAL)
# vbar.pack(side=RIGHT,fill=Y)
# vbar.config(command=canvas.yview)
# canvas.config(width=300,height=300)
# canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
# canvas.pack(side=LEFT,expand=True,fill=BOTH)
#
# root.mainloop()

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
container = ttk.Frame(root)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

for i in range(50):
    ttk.Label(scrollable_frame, text="Sample scrolling label").pack()

container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()