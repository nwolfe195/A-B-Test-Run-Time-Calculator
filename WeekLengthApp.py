from tkinter import *
from tkinter import messagebox
import scipy.stats as st
import math


class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Calculate A/B Test Run Time in Weeks')
        # Create widgets/grid
        self.create_widgets()

    def create_widgets(self):
        # Current Conversion Rate, ccr
        self.ccr_value = StringVar()
        self.ccr_label = Label(self.master, text='Current Conversion Rate')
        self.ccr_label.grid(row=0, column=0, sticky=W)
        self.ccr_entry = Entry(self.master, textvariable=self.ccr_value, width=6)
        self.ccr_entry.grid(row=0, column=1, sticky=E)
        self.ccr_symbol = Label(self.master, text='%')
        self.ccr_symbol.grid(row=0, column=2, sticky=W)
        # Expected Change, ec
        self.ec_value = StringVar()
        self.ec_label = Label(self.master, text='Expected Change')
        self.ec_label.grid(row=0, column=3, sticky=W)
        self.ec_entry = Entry(self.master, textvariable=self.ec_value, width=6)
        self.ec_entry.grid(row=0, column=4, sticky=E)
        self.ec_symbol = Label(self.master, text='%')
        self.ec_symbol.grid(row=0, column=5, sticky=W)
        # Weekly Visitors, wv
        self.wv_value = StringVar()
        self.wv_label = Label(self.master, text='Weekly Visitors')
        self.wv_label.grid(row=1, column=0, sticky=W)
        self.wv_entry = Entry(self.master, textvariable=self.wv_value, width=6)
        self.wv_entry.grid(row=1, column=1, sticky=E)
        # Control Ratio and Variant Ratio, cr and vr
        self.cr_value = StringVar()
        self.ratio_label = Label(self.master, text='Control:Variant Ratio')
        self.ratio_label.grid(row=1, column=3, sticky=W)
        self.cr_entry = Entry(self.master, textvariable=self.cr_value, width=6)
        self.cr_entry.grid(row=1, column=4)
        self.ratio_symbol = Label(self.master, text=':')
        self.ratio_symbol.grid(row=1, column=5)
        self.vr_value = StringVar()
        self.vr_entry = Entry(self.master, textvariable=self.vr_value, width=6)
        self.vr_entry.grid(row=1, column=6)
        # Confidence Level, cl
        self.cl_value = StringVar()
        self.cl_label = Label(self.master, text='Confidence Level')
        self.cl_label.grid(row=2, column=0, sticky=W)
        self.cl_entry = Entry(self.master, textvariable=self.cl_value, width=6)
        self.cl_entry.insert(0,95)
        self.cl_entry.grid(row=2, column=1, sticky=E)
        self.cl_symbol = Label(self.master, text='%')
        self.cl_symbol.grid(row=2, column=2, sticky=W)
        # Power Level, pl
        self.pl_value = StringVar()
        self.pl_label = Label(self.master, text='Power Level')
        self.pl_label.grid(row=2, column=3, sticky=W)
        self.pl_entry = Entry(self.master, textvariable=self.pl_value, width=6)
        self.pl_entry.insert(0, 80)
        self.pl_entry.grid(row=2, column=4)
        self.pl_symbol = Label(self.master, text='%')
        self.pl_symbol.grid(row=2, column=5, sticky=W)
        # Tail Count, tc
        self.tc_value = IntVar(value=2)
        self.onetail_radio = Radiobutton(self.master, text='One-tailed', variable=self.tc_value, value=1)
        self.onetail_radio.grid(row=3, column=0)
        self.twotail_radio = Radiobutton(self.master, text='Two-tailed', variable=self.tc_value, value=2)
        self.twotail_radio.grid(row=3, column=1)
        # Clear Values, cv
        self.cv_button = Button(self.master, text='Clear Values', command=self.clear_input)
        self.cv_button.grid(row=4, column=0)
        # Run Calculation, rc
        self.rc_button = Button(self.master, text='Calculate', command=self.calculate_run_time)
        self.rc_button.grid(row=4, column=1)


    # Calculate Run Time
    def calculate_run_time(self):
        try:
            # Verify and alter input values
            self.primary_success_metric_input = self.input_verification('Current Conversion Rate',self.ccr_value.get(),0,100)
            self.primary_success_metric = self.primary_success_metric_input/100
            self.expected_change_input = self.input_verification('Expected Change',self.ec_value.get(),-10000,10000)
            self.expected_change = self.expected_change_input/100
            self.weekly_visitors = self.input_verification('Weekly Visitors',self.wv_value.get(),0,100000000)
            self.tail = self.input_verification('Tail Count',self.tc_value.get(),1,2)
            self.alpha_input = self.input_verification('Confidence Level',self.cl_value.get(),0,100)
            self.alpha = abs(st.norm.ppf((1-self.alpha_input/100)/self.tail))
            self.beta_input = self.input_verification('Power Level',self.pl_value.get(),0,100)
            self.beta = abs(st.norm.ppf(1-(self.beta_input/100)))
            self.control_ratio = self.input_verification('Control Ratio',self.cr_value.get(),0,100000000)
            self.variant_ratio = self.input_verification('Variant Ratio',self.vr_value.get(),0,100000000)
            self.ratio = self.variant_ratio/self.control_ratio
            # Calculate original population size
            self.test_success_metric = self.primary_success_metric*(1+self.expected_change)
            self.variance_conversion_rate = self.primary_success_metric*(1-self.primary_success_metric) \
            + self.test_success_metric*(1-self.test_success_metric)
            self.n = self.variance_conversion_rate/(self.primary_success_metric-self.test_success_metric)**2 \
            *(self.alpha+self.beta)**2
            # Modify population size to account for uneven group sizes
            self.n_prime = (2*self.n*(1+self.ratio)**2)/(4*self.ratio)
            self.n_original = math.ceil(self.n_prime/(1+self.ratio))
            self.n_treatment = math.ceil((self.ratio*self.n_prime)/(1+self.ratio))
            self.n_total = self.n_original+self.n_treatment
            # Calculate run time in weeks
            self.weeks = round(self.n_total/self.weekly_visitors, 1)
            # Results labels
            self.total_label = Label(self.master, text='Total Population Required')
            self.total_label.grid(row=4, column=3, sticky=W)
            self.total_value = Label(self.master, text=self.n_total)
            self.total_value.grid(row=4, column=4, sticky=W)
            self.default_label = Label(self.master, text='Default Population Required')
            self.default_label.grid(row=5, column=3, sticky=W)
            self.default_value = Label(self.master, text=self.n_original)
            self.default_value.grid(row=5, column=4, sticky=W)
            self.treatment_label = Label(self.master, text='Treatment Population Required')
            self.treatment_label.grid(row=6, column=3, sticky=W)
            self.treatment_value = Label(self.master, text=self.n_treatment)
            self.treatment_value.grid(row=6, column=4, sticky=W)
            self.weeks_label = Label(self.master, text='Runtime (weeks)')
            self.weeks_label.grid(row=7, column=3, sticky=W)
            self.weeks_value = Label(self.master, text=self.weeks)
            self.weeks_value.grid(row=7, column=4, sticky=W)

        except Exception as e:
            print(e)
            pass

    # Verify that input is numeric and within specific bounds
    def input_verification(self,name,value,lower,upper):
        try:
            float_value = float(value)
            if float_value > upper:
                messagebox.showerror('Bound Error','%s must be less than or equal to %d'%(name,upper))
                pass
            if float_value < lower:
                messagebox.showerror('Bound Error','%s must be greater than or equal to %d'%(name,lower))
                pass
            return(float_value)
        except ValueError:
            messagebox.showerror('Type Error','%s must be numeric'%name)

    # Clear all text fields
    def clear_input(self):
        self.ccr_entry.delete(0, END)
        self.ec_entry.delete(0, END)
        self.wv_entry.delete(0, END)
        self.cr_entry.delete(0, END)
        self.vr_entry.delete(0, END)
        self.cl_entry.delete(0, END)
        self.pl_entry.delete(0, END)


root = Tk()
app = Application(master=root)
app.mainloop()
