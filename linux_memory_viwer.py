import os
import sys
import subprocess
import threading
import time

# Checking versions and installation of main packages used here
try:
    import numpy as np
except ImportError:
    print('Install NumPy! Please see README.md for futher informations')
    sys.exit()
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg
except ImportError:
    try:
        from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
    except ImportError:
        print('Install MatPlotLib Python! Please see README.md for futher informations')
        sys.exit()
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    try:
        import Tkinter as tk
        import ttk
    except ImportError:
        print('Tkinter or ttk not installed! Please see README.md for futher informations')
        sys.exit()

# Thanks to https://stackoverflow.com/questions/12332975/installing-python-module-within-code
try:
    import pandas as pd
except ImportError:
    print('Install Pandas! Please see README.md for futher informations')
    sys.exit()

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
               treeview_sort_column(tv, col, not reverse))

def memory_values():
    '''
    Return a DataFrame containing informations values from RAM, Cache and Swap memories.
    '''
    meminfo = dict((i.split()[0].rstrip(':'),[int(i.split()[1])]) for i in open('/proc/meminfo').readlines())
    return pd.DataFrame().from_dict(meminfo)

def page_faults():
    '''
    Return a DataFrame containing informatios due to page faults system.
    '''
    try:
        pagesF = subprocess.check_output("ps h -e -o pid,min_flt,maj_flt", shell = True).split('\n')
    except:
        pagesF = str(subprocess.check_output("ps h -e -o pid,min_flt,maj_flt", shell = True))[2:-1].split('\\n')

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
    proc_flt = proc_flt[(proc_flt['min_flt']!=0) | (proc_flt['maj_flt']!=0)]
    return proc_flt

class Canvas(ttk.Frame, object):
    '''
    A GUI class for this application
    '''

    ## Variables
    score_label={}
    score_value_label={}
    df=page_faults()
    figure=None
    cavas=None
    is_thread=False

    def __init__(self, master=None, title='Canvas',df=page_faults()):
        '''
        Constructor
        '''
        super(Canvas, self).__init__(master, padding="12 12 12 12")
        self.master.protocol("WM_DELETE_WINDOW", self.exit) # Set new exit function on close window
        self.master.title(title)
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.master.columnconfigure(0, weight=3)
        self.master.rowconfigure(0, weight=3)
        self.figure = plt.figure(figsize=(3,5), dpi=100)
        self.is_thread=True
        self.pack()
        self.create_widgets()

        self.draw_thread=threading.Thread(target=self.draw_figure)
        self.draw_thread.start()

        # self.pids_thread=threading.Thread(target=self.update_pids)
        # self.pids_thread.start()

        self.pids_thread=threading.Thread(target=self.fill_tree)
        self.pids_thread.start()



    def create_widgets(self):
        '''
        Create widgets necessaries
        '''

        ## Tab responsible for widget
        self.options = ttk.Notebook(self)
        
        ## Page Faults Tab panel with tree view
        self.page_faults_frame_tv = ttk.Frame()
        self.options.add(self.page_faults_frame_tv, text='Page Faults TV')

        self.pf_tree = ttk.Treeview(self.page_faults_frame_tv, columns=('pid', 'maj_flt', 'min_flt'))
        self.pf_tree.heading('pid',text='Active Process PID')
        self.pf_tree.heading('maj_flt',text='Major Page Faults')
        self.pf_tree.heading('min_flt',text='Minor Page Faults')
        self.pf_tree.column('pid',anchor=tk.CENTER)
        self.pf_tree.column('maj_flt',anchor=tk.CENTER)
        self.pf_tree.column('min_flt',anchor=tk.CENTER)
        self.pf_tree['show']='headings'
        self.pf_tree.grid(column=1,row=1,rowspan=22,sticky=(tk.N,tk.W,tk.E,tk.S))

        ## Page Faults Tab panel
        # self.page_faults_frame = ttk.Frame()
        # self.options.add(self.page_faults_frame, text='Page Faults')

        # ## Items on Page Faults Tab panel
        # self.pid_label = tk.Label(self.page_faults_frame,text='Active Process PID')
        # self.pid_label.grid(column=1, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        # self.listbox_pid = tk.Listbox(self.page_faults_frame,height=25)
        # self.listbox_scroll = tk.Scrollbar(self.listbox_pid,orient=tk.VERTICAL)
        # self.listbox_pid.grid(column=1, row=2, rowspan=12, sticky=(tk.N, tk.W, tk.E, tk.S))
        # self.listbox_pid.config(yscrollcommand=self.listbox_scroll.set)
        # self.listbox_scroll.config(command=self.listbox_pid.yview)
        # self.maj_flt_label = tk.Label(self.page_faults_frame,text=' Major Page Faults ')
        # self.maj_flt_label.grid(column=3, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        # self.min_flt_label = tk.Label(self.page_faults_frame,text=' Minor Page Faults ')
        # self.min_flt_label.grid(column=2, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        ## There is no need for such a thing
        # self.update_btn = tk.Button(self.page_faults_frame,text='Udate Active Process PID list',command=self.update_pids)
        # self.update_btn.grid(column=3, row=13, sticky=(tk.N, tk.W, tk.E, tk.S))

        ## Memory page/panel
        self.mem_vals_frame = tk.Frame()
        self.options.add(self.mem_vals_frame, text='Memory Values')

        ## There's no need for this button once a thread is setted for this job
        # self.update_figure_btn = tk.Button(self.mem_vals_frame,text='Udate',command=self.draw_figure)
        # self.update_figure_btn.grid(column=1, row=13, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.canvas = FigureCanvasTkAgg(self.figure,master=self.mem_vals_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.mem_vals_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        ## There is no need for such a thing
        # self.min_flt_frame = tk.Label(self.page_faults_frame)
        # self.min_flt_frame.grid(column=2, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))
        # self.maj_flt_frame = tk.Label(self.page_faults_frame)
        # self.maj_flt_frame.grid(column=3, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        self.master.bind('<Control-c>', self.exit)
        self.master.bind('<Control-q>', self.exit)
        self.master.bind('<Control-w>', self.exit)
        self.master.bind('<Alt-F4>', self.exit)
        self.master.bind('<Escape>', self.exit)

        ## There is no need for such a thing
        # self.insert2listbox()

    def fill_tree(self):
        while(self.is_thread):
            self.df = self.df.append(page_faults(),ignore_index=True)
            self.df.drop_duplicates('pid',inplace=True,keep='last')
            self.childs=self.pf_tree.get_children()
            self.df.index=self.df.index.map(str)
            self.df.sort_values('pid',inplace=True)
            self.children={}
            for child in self.childs:
                self.children[self.pf_tree.item(child)['values'][0]]=child
            for index,row in self.df.iterrows():
                if row['pid'] not in self.children.keys():
                    self.pf_tree.insert('','end',values=(int(row['pid']),row['min_flt'],row['maj_flt']))
                else:
                    self.pf_tree.item(self.children[int(row['pid'])],values=(int(row['pid']),row['min_flt'],row['maj_flt']))
            self.pf_tree.config(height=min(25,self.df.shape[0]))
            time.sleep(0.5)


    ## Doesn't need this anymore
    # def insert2listbox(self):
    #     for row in self.df['pid']:
    #         self.listbox_pid.insert(tk.END,row)
    #     self.listbox_pid.bind('<<ListboxSelect>>', self.onselect)

    def update_pids(self):
        print(self.listbox_pid)
        while(self.is_thread):
            self.df = page_faults()
            self.listbox_pid.delete(0,tk.END)
            # self.listbox_pid.update_idletasks()
            for row in self.df['pid']:
                self.listbox_pid.insert(tk.END,row)
            # self.listbox_pid.update_idletasks()
            
            time.sleep(1)

    def calculate_values(self):
        mem_vals_df = memory_values()
        # print(mem_vals_df.transpose())
        mem_vals_df['MemUsed'] = int(mem_vals_df['MemTotal']) - int(mem_vals_df['MemFree'])
        mem_vals_df['SwapUsed'] = int(mem_vals_df['SwapTotal']) - int(mem_vals_df['SwapFree'])
        df_aux = {'Memory':{},'Swap':{},'Cache':{}}
        for col in mem_vals_df.columns:
            for key in df_aux.keys():
                if key[:3] in col:
                    df_aux[key][col] = mem_vals_df[col][0]
        for key in df_aux.keys():
            df_aux[key] = pd.DataFrame().from_dict(df_aux[key],orient='index',columns=['value']).reset_index()
        return pd.concat(df_aux)

    def draw_figure(self,loc=(20, 20)):
        while(self.is_thread):
            self.figure.clear()
            df_aux = self.calculate_values()
            plt.bar(df_aux['index'],df_aux['value'])
            plt.xticks(rotation=90)
            plt.subplots_adjust(left=0.2,bottom=0.22)
            self.canvas.draw()

            time.sleep(0.5)
        


    def onselect(self,evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.min_flt_frame.config(text=self.df['min_flt'].iloc[index])
        self.maj_flt_frame.config(text=self.df['maj_flt'].iloc[index])

    def exit(self,*args):
        try:
            self.is_thread=False
            self.master.quit()
            self.master.destroy()
        except:
            sys.exit()

def main():
    root = tk.Tk()
    app = Canvas(master=root,title='Linux Memory Viwer')
    app.mainloop()

if __name__ == "__main__":
    main()


