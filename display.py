import os
import tkinter as tk
import zoomer

from tkinter import filedialog


BTN_H = 2
BTN_W = 20

COLOR = {
    'success': '#A3DE83',
    'danger': '#f04d43',
    'mint': '#5BBD93',
    'mango': '#FB9927',
}

FONT = ('arial', 8, 'bold')

FILES = {'Input': '', 'Output': ''}

class Display(tk.Frame):

    @classmethod
    def main(cls):
        root = tk.Tk()
        root.title("Zoomer")
        root.resizable(width=False, height=False)
        root.geometry('330x250')

        frame = cls(root)
        frame.grid()
        root.mainloop()


    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.f_in_label = tk.Label(self, text="Roster: EMPTY", font=FONT)
        self.f_out_label = tk.Label(self, text="Results: EMPTY", font=FONT)

        self.f_in_btn = tk.Button(self, text="Student Roster", font=FONT, height=BTN_H, width=BTN_W, 
            fg="white", bg=COLOR['danger'], activebackground=COLOR['danger'], activeforeground='white', 
            command=lambda: addFile("Input", self.f_in_label, self.f_in_btn, self.f_out_btn))
        self.f_out_btn = tk.Button(self, text="Attendance Results", font=FONT, height=BTN_H, width=BTN_W, 
            fg="white", bg=COLOR['danger'], activebackground=COLOR['danger'], activeforeground='white',
            command=lambda: addFile("Output", self.f_out_label, self.f_in_btn, self.f_out_btn))

        self.student_btn = tk.Button(self, text="Take Attendance", font=FONT, height=BTN_H, width=BTN_W, 
            fg="white", bg=COLOR['mint'], activebackground=COLOR['success'], activeforeground='white', 
            command=lambda: attendance("Student", self.f_in_label, self.f_out_label, self.output_label))
        self.leaders_btn = tk.Button(self, text="Admit Group Leaders", font=FONT, height=BTN_H, width=BTN_W, 
            fg="white", bg=COLOR['mint'], activebackground=COLOR['success'], activeforeground='white', 
            command=lambda: attendance("Leader", self.f_in_label, self.f_out_label, self.output_label))

        self.output_label = tk.Label(self, text="", font=FONT)
        
        self.f_in_label.grid(row=1, column=0, padx=10, pady=(15,10))
        self.f_out_label.grid(row=1, column=1, pady=(15,10))

        self.f_in_btn.grid(row=2, column=0, padx=10, pady=5)
        self.f_out_btn.grid(row=2, column=1, pady=5)
        
        self.student_btn.grid(row=3, column=0, pady=5)
        self.leaders_btn.grid(row=3, column=1, pady=5)

        self.output_label.grid(row=4, column=0, pady=15, columnspan=2)

        self.student_btn.bind('<Enter>', self.student_hover)
        self.leaders_btn.bind('<Enter>', self.leaders_hover)

        self.student_btn.bind('<Leave>', self.student_leave)
        self.leaders_btn.bind('<Leave>', self.leaders_leave)


    def student_hover(self, e):
        self.student_btn['bg'] = COLOR['mango']
    def leaders_hover(self, e):
        self.leaders_btn['bg'] = COLOR['mango']

    def student_leave(self, e):
        self.student_btn['bg'] = COLOR['mint']
    def leaders_leave(self, e):
        self.leaders_btn['bg'] = COLOR['mint']


def addFile(file, label, in_btn, out_btn):
    file_name = filedialog.askopenfilename(initialdir='/', title="Select A File", filetypes=(("csv files", '*.csv'),))
    
    if os.path.isfile(file_name):
        FILES[file] = file_name
        f = file_name.split('/')
        
        if file == "Input":
            label.config(text="Roster: " + f[-1])
            in_btn['bg'] = COLOR['success']
        else:
            label.config(text="Results: " + f[-1])
            out_btn['bg'] = COLOR['success']

    if FILES['Input'] != '' and FILES['Output'] != '':
        zoomer.setup_df(FILES['Input'], FILES['Output'])


def attendance(student_type, f_in_label, f_out_label, output_label):
    if FILES['Input'] != '' and FILES['Output'] != '':
        run = zoomer.attendance(FILES['Input'], FILES['Output'], student_type)
        if run is None:
            output_label.config(text="Please make sure to: \nminimize all unused windows \nkeep the Zoom app visible on the desktop")

           
if __name__ == '__main__':
    Display.main()