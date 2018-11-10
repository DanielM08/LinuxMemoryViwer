import os
import subprocess
import dialog_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
import numpy as np

# Thanks to https://stackoverflow.com/questions/12332975/installing-python-module-within-code
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    try:
        import Tkinter as tk
        import ttk
    except ImportError:
        print('Tkinter not installed!')

try:
    import pandas as pd
except ImportError:
    try:
        import pip
        subprocess.call([sys.executable, "-m", "pip", "install", "pandas"])
    except ImportError:
        dialog_error('Import PIP')


def memory_values():
    meminfo = dict((i.split()[0].rstrip(':'),[int(i.split()[1])]) for i in open('/proc/meminfo').readlines())
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
            pid.append(int(lstAux1[0]))
            min_flt.append(int(lstAux1[1]))
            maj_flt.append(int(lstAux1[2]))
    proc_flt = pd.DataFrame().from_dict({'pid':pid,'min_flt':min_flt, 'maj_flt':maj_flt})
    return proc_flt

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

    def create_widgets(self):
        self.options = ttk.Notebook(self)
        
        self.page_faults_frame = ttk.Frame()
        self.options.add(self.page_faults_frame, text='Page Faults')

        self.pid_label = tk.Label(self.page_faults_frame,text='Active Process PID')
        self.pid_label.grid(column=1, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.listbox_pid = tk.Listbox(self.page_faults_frame,height=25)
        self.listbox_pid.grid(column=1, row=2, rowspan=12, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.maj_flt_label = tk.Label(self.page_faults_frame,text=' Major Page Faults ')
        self.maj_flt_label.grid(column=3, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.min_flt_label = tk.Label(self.page_faults_frame,text=' Minor Page Faults ')
        self.min_flt_label.grid(column=2, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        self.update_btn = tk.Button(self.page_faults_frame,text='Udate Active Process PID list',command=self.update_pids)
        self.update_btn.grid(column=3, row=13, sticky=(tk.N, tk.W, tk.E, tk.S))


        self.mem_vals_frame = tk.Frame()
        self.options.add(self.mem_vals_frame, text='Memory Values')


        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.min_flt_frame = tk.Label(self.page_faults_frame)
        self.min_flt_frame.grid(column=2, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.maj_flt_frame = tk.Label(self.page_faults_frame)
        self.maj_flt_frame.grid(column=3, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        self.master.bind('<Control-c>', self.exit)
        self.master.bind('<Control-q>', self.exit)
        self.master.bind('<Control-w>', self.exit)
        self.master.bind('<Alt-F4>', self.exit)
        self.master.bind('<Escape>', self.exit)

        self.insert2listbox()
        self.draw_figure()

    def insert2listbox(self):
        for row in self.df['pid']:
            self.listbox_pid.insert(tk.END,row)
        self.listbox_pid.bind('<<ListboxSelect>>', self.onselect)

    def update_pids(self):
        self.listbox_pid.delete(0,tk.END)
        for row in self.df['pid']:
            self.listbox_pid.insert(tk.END,row)

    def draw_figure(self,loc=(20, 20)):
        mem_vals_df = memory_values()
        mem_vals_df['MemUsed'] = int(mem_vals_df['MemTotal']) - int(mem_vals_df['MemFree'])
        mem_vals_df = mem_vals_df.loc[:,['MemUsed','MemFree']].transpose()
        # mem_vals_df = page_faults()

        figure = plt.figure(figsize=(3,5), dpi=100)
        # ax = mem_vals_df.plot(y=0,kind='pie',fig=figure)
        # ax.plot()
        plt.pie(mem_vals_df)

        canvas = FigureCanvasTkAgg(figure,master=self.mem_vals_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        
        toolbar = NavigationToolbar2TkAgg(canvas, self.mem_vals_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        


    def onselect(self,evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.min_flt_frame.config(text=self.df['min_flt'].iloc[index])
        self.maj_flt_frame.config(text=self.df['maj_flt'].iloc[index])

    def exit(self,*args):
        self.master.quit()
        self.master.destroy()

def main():
    root = tk.Tk()
    app = Canvas(master=root,title='Linux Memory Viwer')
    app.mainloop()

if __name__ == "__main__":
    main()


