from tkinter import *
from tkinter import messagebox
import scipy.stats as st
import math


class Window:
    def __init__(self, master):
        self.master = master
        master.title('Calculate A/B Test Run Time in Weeks')

        psm = StringVar()
        Label(master, text='Current Conversion Rate').grid(row=0, column=0, sticky=W)
        Entry(root, textvariable=psm, width=6).grid(row=0, column=1, sticky=E)
        Label(master, text='%').grid(row=0, column=2, sticky=W)

        ec = StringVar()
        Label(master, text='Expected Change').grid(row=0, column=3, sticky=W)
        Entry(root, textvariable=ec, width=6).grid(row=0, column=4, sticky=E)
        Label(master, text='%').grid(row=0, column=5, sticky=W)

        wv = StringVar()
        Label(master, text='Weekly Visitors').grid(row=1, column=0, sticky=W)
        Entry(root, textvariable=wv, width=6).grid(row=1, column=1, sticky=E)

        cr = StringVar()
        vr = StringVar()
        Label(master, text='Control:Variant Ratio').grid(row=1, column=3, sticky=W)
        Entry(root, textvariable=cr, width=6).grid(row=1, column=4)
        Label(master, text=':').grid(row=1, column=5)
        Entry(root, textvariable=vr, width=6).grid(row=1, column=6)

        cl = StringVar()
        Label(master, text='Confidence Level').grid(row=2, column=0, sticky=W)
        cl_entry = Entry(root, textvariable=cl, width=6)
        cl_entry.insert(0, 95)
        cl_entry.grid(row=2, column=1, sticky=E)
        Label(master, text='%').grid(row=2, column=2, sticky=W)

        p = StringVar()
        Label(master, text='Power').grid(row=2, column=3, sticky=W)
        p_entry = Entry(root, textvariable=p, width=6)
        p_entry.insert(0, 80)
        p_entry.grid(row=2, column=4)
        Label(master, text='%').grid(row=2, column=5, sticky=W)

        t = IntVar(value=2)
        ot = Radiobutton(master, text='One-tailed', variable=t, value=1).grid(row=3, column=0)
        tt = Radiobutton(master, text='Two-tailed', variable=t, value=2).grid(row=3, column=1)

        variables = [psm,ec,wv,cr,vr,cl,p,t]
        b = Button(master, text='Calculate', command=lambda : self.Calculate(variables,master)).grid(row=4, column=0)

    def Calculate(self,variables,master):
        primary_success_metric = float(variables[0].get())/100
        expected_change = float(variables[1].get())/100
        weekly_visitors = float(variables[2].get())
        tail = float(variables[7].get())
        alpha = abs(st.norm.ppf((1-float(variables[5].get())/100)/tail))
        beta = abs(st.norm.ppf(1-(float(variables[6].get())/100)))
        ratio = float(variables[4].get())/float(variables[3].get())

        test_success_metric = primary_success_metric*(1+expected_change)
        variance_conversion_rate = primary_success_metric*(1-primary_success_metric) \
        + test_success_metric*(1-test_success_metric)
        n = variance_conversion_rate/(primary_success_metric-test_success_metric)**2*(alpha+beta)**2

        n_prime = (n*(1+ratio)**2)/(4*ratio)
        n_original = math.ceil(n_prime/(1+ratio))
        n_treatment = math.ceil((ratio*n_prime)/(1+ratio))
        n_total = n_original+n_treatment

        Label(master, text='Total Population Required').grid(row=4, column=3, sticky=W)
        Label(master, text=n_total).grid(row=4, column=4, sticky=W)
        Label(master, text='Default Population Required').grid(row=5, column=3, sticky=W)
        Label(master, text=n_original).grid(row=5, column=4, sticky=W)
        Label(master, text='Treatment Population Required').grid(row=6, column=3, sticky=W)
        Label(master, text=n_treatment).grid(row=6, column=4, sticky=W)

        weeks = round(n_total/weekly_visitors,1)
        Label(master, text='Runtime (weeks)').grid(row=7, column=3, sticky=W)
        Label(master, text=weeks).grid(row=7, column=4, sticky=W)


root = Tk()
root.geometry()
my_gui = Window(root)
root.mainloop()
