# error.py

# Thanks to https://stackoverflow.com/questions/12332975/installing-python-module-within-code
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

def dialog_error(message):
    error_msg = tk.Tk()
    tk.Label(error_msg, text=message).grid(column=1, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
    tk.Button(error_msg, text='OK', command=error_msg.destroy).grid(column=1, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))
    for child in error_msg.winfo_children():
        child.grid_configure(padx=15, pady=15)
    def exit(*args):
        error_msg.destroy()
    error_msg.bind('<Control-c>', exit)
    error_msg.bind('<Control-q>', exit)
    error_msg.bind('<Control-w>', exit)
    error_msg.bind('<Alt-F4>', exit)
    error_msg.bind('<Escape>', exit)
    error_msg.mainloop()
