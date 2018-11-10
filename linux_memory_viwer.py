import os
import subprocess
import dialog_error

# Thanks to https://stackoverflow.com/questions/12332975/installing-python-module-within-code
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

try:
    import pandas as pd
except ImportError:
    try:
        import pip
    except ImportError:
        dialog_error('Import PIP')


def memory_values():
    meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    return pd.DataFrame().from_dict(meminfo)

def page_faults():
    pagesF = subprocess.check_output("ps h -e -o pid,min_flt,maj_flt", shell = True).split('\n')

    pid = []
    min_flt = []
    maj_flt = []
    for i in range(0, len(pagesF)):
        lstAux1 = pagesF[i].split(' ')
        lstAux1 = [item for item in lstAux1 if item != '']
        if(lstAux1):
            pid.append(lstAux1[0])
            min_flt.append(lstAux1[1])
            maj_flt.append(lstAux1[2])
    proc_flt = pd.DataFrame().from_dict({'pid':pid,'min_flt':min_flt, 'maj_flt':maj_flt})
    return proc_flt

# print(page_faults(pageFaults))


class Canvas(ttk.Frame, object):
    score_label={}
    score_value_label={}
    df=page_faults()

    def __init__(self, master=None, title='Canvas',df=page_faults()):
        super(Canvas, self).__init__(master, padding="12 12 12 12")
        self.master.title(title)
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.master.columnconfigure(0, weight=3)
        self.master.rowconfigure(0, weight=3)
        self.pack()
        self.create_widgets()
        self.insert2listbox()

    def create_widgets(self):
        self.options = ttk.Notebook(self)
        
        self.page_faults_frame = ttk.Frame()
        self.options.add(self.page_faults_frame, text='Page Faults')

        self.listbox_pid = tk.Listbox(self.page_faults_frame)
        self.listbox_pid.grid(column=1, row=1, rowspan=12, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.maj_flt_label = tk.Label(self.page_faults_frame,text='Major Page Faults')
        self.maj_flt_label.grid(column=3, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.min_flt_label = tk.Label(self.page_faults_frame,text='Minor Page Faults')
        self.min_flt_label.grid(column=2, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        self.mem_vals_frame = ttk.Frame()
        self.options.add(self.mem_vals_frame, text='Memory Values')
        
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.min_flt_frame = tk.Label(self.page_faults_frame)
        self.min_flt_frame.grid(column=2, row=3, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.maj_flt_frame = tk.Label(self.page_faults_frame)
        self.maj_flt_frame.grid(column=3, row=3, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        self.master.bind('<Control-c>', self.exit)
        self.master.bind('<Control-q>', self.exit)
        self.master.bind('<Control-w>', self.exit)
        self.master.bind('<Alt-F4>', self.exit)
        self.master.bind('<Escape>', self.exit)

    def insert2listbox(self):
        for row in self.df['pid']:
            self.listbox_pid.insert(tk.END,row)
        self.listbox_pid.bind('<<ListboxSelect>>', self.onselect)

    def onselect(self,evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.min_flt_frame.config(text=self.df['min_flt'].loc[index])
        self.maj_flt_frame.config(text=self.df['maj_flt'].loc[index])

    def exit(self,*args):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = Canvas(master=root,title='Linux Memory Viwer')
    app.mainloop()

    # ttk.Entry(mainframe, width=7, textvariable=feet).grid(column=2, row=1, sticky=(W, E)).focus()
    # root.bind('<Return>', calculate) # on enter key pressed

    # root.mainloop()

if __name__ == "__main__":
    main()


