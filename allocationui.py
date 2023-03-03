import tkinter as tk
from tkinter import ttk
#import customtkinter as ctk
from tkinter import filedialog
import matplotlib
import pandas as pd

matplotlib.use("TkAgg") #backend of matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
#import urllib
#import json
#import pandas as pd
#import numpy as np
import os
import subprocess
import sys
import threading
from io import StringIO
from pandastable import *



LARGE_FONT = ("Verdana",12)
NORM_FONT = ("Verdana",10)
SMALL_FONT = ("Verdana",8)

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text = msg, font= NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()

def run_R_script(script_path):
    #subprocess.Popen(["Rscript", script_path], stdout=subprocess.PIPE, stderr= subprocess.PIPE, shell=True)
    process = subprocess.Popen(["Rscript", script_path], stdout=subprocess.PIPE, stderr= subprocess.PIPE)
    output, error = process.communicate()
    #print(output.decode('utf-8'))
    #if error:
        #print(error.decode('utf-8'))
    #outputwindow = tk.Tk()
    #outputwindow.wm_title("Output")
    #label = ttk.Label(outputwindow)
    return output.decode('utf-8')

def display_output(script_path):
    outputwindow = tk.Toplevel()
    outputwindow.title("Output")
    output = run_R_script(script_path)
    output_label = ttk.Label(outputwindow,text=output)
    output_label.pack()

#def display_modeloutput(epsilon):
    #import Biobjective477 as bo
    #outputwindow = tk.Toplevel()
    #outputwindow.title("Output of Allocation Model")
    #output = bo.epsilon_constraint_allocation(epsilon)
    #output_label = ttk.Label(outputwindow, text = output)
    #output_label.pack()

class AllocationApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Pro-active Inventory Allocation Decision Support System")

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0,weight=1)


        #Bu şekilde yukarı kısma menü için bir şeyler eklenilebilir.
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label = "Save settings",command = lambda: popupmsg("Not supported yet."))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu = filemenu)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label = "Edit Data",command = lambda: popupmsg("Not supported yet."))
        editmenu.add_separator()
        editmenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="Edit", menu = editmenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, Insights, DataUpdate, Charts, IAM, DataPreparation, Zones,
                  Forecast, Product): #This enables to travel between windows. Any added window class should be here.
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Login Page", font=LARGE_FONT)
        label.pack(pady=10, padx= 10)
        label1 = tk.Label(self, text="Please enter information below to log in.")
        label1.pack()

        username = tk.StringVar()
        password = tk.StringVar()

        username_label = tk.Label(self, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(self, textvariable=username)
        username_entry.pack()

        password_label = tk.Label(self, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(self, textvariable=password, show="*")
        password_entry.pack()

        tk.Label(self, text="").pack()

        button = ttk.Button(self, text="Login")
        button.pack()

        #Login kısmını aktif yapıcak DB ve error mesajları kısmı eklemesi.

        button1 = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()

        buttonapp = ttk.Button(self, text="See Service Available",
                            command=lambda: controller.show_frame(PageThree))
        buttonapp.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text= "First Page", font=LARGE_FONT)
        label.pack(pady=10, padx= 10)

        button2 = ttk.Button(self, text="Back to Homepage",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()

        button4 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button4.pack()

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text= "Second Page", font=LARGE_FONT)
        label.pack(pady=10, padx= 10)

        button2 = ttk.Button(self, text="Back to Homepage",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()

        button3 = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button3.pack()

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text= "Provided Services", font=LARGE_FONT)
        label.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        button4 = ttk.Button(self, text="Update Data",
                            command=lambda: controller.show_frame(DataUpdate))
        button4.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        button5 = ttk.Button(self, text="Run Forecast Methods",
                             command=lambda: controller.show_frame(Forecast))
        button5.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button6 = ttk.Button(self, text="Update and Show Zones",
                             command=lambda: controller.show_frame(Zones))
        button6.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button7 = ttk.Button(self, text="Search Product",
                             command=lambda: controller.show_frame(Product))
        button7.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button8 = ttk.Button(self, text="Update and Show Insights",
                             command=lambda: controller.show_frame(Insights))
        button8.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button9 = ttk.Button(self, text="Integer Allocation Model",
                             command=lambda: controller.show_frame(IAM))
        button9.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button10 = ttk.Button(self, text="Log out",
                             command=lambda: controller.show_frame(StartPage))
        button10.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class DataUpdate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text= "Data Update", font=LARGE_FONT)
        label.pack(pady=10, padx= 10)

        def browseFiles():
            filename = filedialog.askopenfilename(initialdir="/", title="Select a File",filetypes=(("Text files","*.txt*"),("all files","*.*")))

            # Change label contents
            label_file_explorer.configure(text="File Opened: " + filename)

        label_file_explorer = tk.Label(self,
                                    text="File Explorer using Tkinter",
                                    width=100, height=4,
                                    fg="blue")

        button_explore = tk.Button(self, text="Browse Files", command=browseFiles)
        button_explore.pack()

        homepage = ttk.Button(self, text="Back to Provided Services",
                            command=lambda: controller.show_frame(PageThree))
        homepage.pack()

class Forecast(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text= "Forecasting Methods", font=LARGE_FONT)
        label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        zone1 = ttk.Button(self, text="Apply Forecast Methods for Zone 1",
                              command=lambda: controller.show_frame(PageThree))
        zone1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        zone2 = ttk.Button(self, text="Apply Forecast Methods for Zone 2",
                              command= lambda:self.run_forecast())
        zone2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        zone3 = ttk.Button(self, text="Apply Forecast Methods for Zone 3",
                              command=lambda: controller.show_frame(PageThree))
        zone3.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        zone4 = ttk.Button(self, text="Apply Forecast Methods for Zone 4",
                              command=lambda: controller.show_frame(PageThree))
        zone4.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        zone5 = ttk.Button(self, text="Apply Forecast Methods for Zone 5",
                              command=lambda: controller.show_frame(PageThree))
        zone5.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        tocsv = ttk.Button(self, text="Download Forecast Results as CVS",
                              command=lambda: controller.show_frame(PageThree))
        tocsv.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        services = ttk.Button(self, text="Back to Provided Services",
                            command=lambda: controller.show_frame(PageThree))
        services.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def run_forecast(self):
        running_window = RunningWindowForecast(self)
        running_window.grab_set()

        model_thread = threading.Thread(target=self.runforecast_thread)
        model_thread.start()

        self.check_model_thread(model_thread, running_window)

    def runforecast_thread(self):
        import forecast_zone2 as fc2
        #path_to_gurobipy = "C:/Users/PC/PycharmProjects/pythonProject23/venv/Lib/site-packages/gurobipy"
        #os.environ["PYTHONPATH"] = path_to_gurobipy
        result = fc2.forecast_zone2()
        return result

    def check_model_thread(self,model_thread, running_window):
        if model_thread.is_alive():
            self.after(100, lambda: self.check_model_thread(model_thread, running_window)) #checking if the model is ended or still running every 100ms.
        else:
            #Model thread has finished, so close the "running" pop-up window and display the solution.
            running_window.destroy()
            solution_output = self.runforecast_thread()
            solution_window = SolutionWindowForecast(self, solution_output)
            solution_window.grab_set()

class RunningWindowForecast(tk.Toplevel): #Pop-up window that displays the statement that model is running.
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Currently Running")
        self.label = tk.Label(self, text="The program is currently running. Please wait.")
        self.label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class SolutionWindowForecast(tk.Toplevel): #burdaki çıkan ekrandan kaydedilebiliyor ama csv değil pickle diye bişi?
    def __init__(self, parent, result):
        super().__init__(parent)
        self.title("Outputs of Forecasting Methods")
        self.label = tk.Label(self, text="The program has finished running.")
        self.label.grid(row=0, column=0, sticky="nsew")

        self.table = Table(self, dataframe=result, showtoolbar=True, showstatusbar=True)
        self.table.grid(row=1, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.table.show(self)

class Zones(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text= "Update and Show Zones", font=LARGE_FONT)
        label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        updatezones = ttk.Button(self, text="Update Zones",
                                  command=lambda:self.run_script())
        updatezones.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #visualizezones = ttk.Button(self, text="Visualize Zones",
                                 #command=lambda: controller.show_frame(DataPreparation))
        #visualizezones.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        services = ttk.Button(self, text="Back to Provided Services",
                              command=lambda: controller.show_frame(PageThree))
        services.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def run_script(self):
        running_window = RunningWindow(self)
        running_window.grab_set()

        model_thread = threading.Thread(target=self.runmodel_thread)
        model_thread.start()

        self.check_model_thread(model_thread, running_window)

    def runmodel_thread(self):
        path_to_gurobipy = "C:/Users/PC/PycharmProjects/pythonProject23/venv/Lib/site-packages/gurobipy" #showing the path to the gurobipy in order to see the path that used in ClusterModel.py
        os.environ["PYTHONPATH"] = path_to_gurobipy #setting the environment.
        subprocess.run(["python", "ClusterModel.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #running the code.

    def check_model_thread(self,model_thread, running_window):
        if model_thread.is_alive():
            self.after(100, lambda: self.check_model_thread(model_thread, running_window)) #checking if the model is ended or still running every 100ms.
        else:
            # Model thread has finished, so close the "running" pop-up window and display the solution
            running_window.destroy()
            solution_window = SolutionWindow(self)
            solution_window.grab_set()

class Product(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text= "Search Product", font=LARGE_FONT)
        label.pack(pady=10, padx= 10)

        self.selected_option = tk.StringVar()
        options = ["23-B938438475J", "22-A938268475AG", "16-H128948475K", "76-S938948675K", "63-S9389826385M", "11-S9394J036K", "926-S99374567K"]
        combobox = ttk.Combobox(self, textvariable=self.selected_option, values=options)
        combobox.pack()

        label = ttk.Label(self, textvariable=self.selected_option)
        label.pack()

        skuid = ttk.Button(self, text="Choose Product ID",
                              command=lambda: controller.show_frame(PageThree))
        skuid.pack()

        #buradaki forecast data, start of week sales vs searched product için mi? Öyleyse product id seçildikten
        #sonraki page'de olacak o kısımlar. Şu noktada eksik.

        services = ttk.Button(self, text="Back to Provided Services",
                            command=lambda: controller.show_frame(PageThree))
        services.pack()

class Insights(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text= "Data Analysis Insights", font=LARGE_FONT)
        label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #def R_prepareforML():
            #subprocess.call(["Rscript", "22_Oplog.R"], shell= True)
            #popup = tk.Tk()
            #popup.wm_title("Data Preparation")
            #label = ttk.Label(popup, text="Data Preparation Completed.", font= NORM_FONT)
            #label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            #b1 = ttk.Button(popup, text="Okay", command = popup.destroy)
            #b1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #def R_datamanipulation():
            #subprocess.call(['Rscript', "11_Oplog.R"], shell= True)
            #popup = tk.Tk()
            #popup.wm_title("Data Adjustment")
            #label = ttk.Label(popup, text="Data adjusted successfully!", font=NORM_FONT)
            #label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            #B1 = ttk.Button(popup, text="Prepare data for forecasting", command=R_prepareforML())
            #B1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            #B2 = ttk.Button(popup, text="Okay", command=popup.destroy)
            #B2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            #popup.mainloop()
        #adjustandprepare = ttk.Button(self, text="Adjust and Prepare Data for Forecast",
                            #command=lambda: controller.show_frame(DataPreparation))
        #adjustandprepare.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        chartbutton = ttk.Button(self, text="Show Zone Based Analysis Charts",
                            command=lambda: controller.show_frame(Charts))
        chartbutton.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        weekofsalesbutton = ttk.Button(self, text="Show Chart of Start Week of Sales",
                            command=lambda: controller.show_frame(Start))
        weekofsalesbutton.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        nowsoldbutton = ttk.Button(self, text="Show Chart of Number of Weeks Sold",
                            command=lambda: controller.show_frame(NoWSold))
        nowsoldbutton.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        productclass = ttk.Button(self, text="Show Product Classification Chart",
                            command=lambda: controller.show_frame(ProdClass))
        productclass.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #manipulatedata = ttk.Button(self, text="Adjust Address and Sales Excel Files",
                            #command=R_datamanipulation)
        #manipulatedata.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        homepage = ttk.Button(self, text="Back to Provided Services",
                              command=lambda: controller.show_frame(PageThree))
        homepage.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class Charts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text= "Zone Based Analysis Charts", font=LARGE_FONT)
        label.pack(pady=10, padx= 10)

        insights = ttk.Button(self, text="Back to Data Analysis Insights",
                              command=lambda: controller.show_frame(Insights))
        insights.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111) #one by one and plot number one
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,4,6,8,10])
        a.set_title("Zone 1")

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True) #grid de olabilir.

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

class DataPreparation(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text= "Data Preparation for Forecast", font=LARGE_FONT)
        label.pack(pady=10, padx= 10)

        homepage = ttk.Button(self, text="Back to Provided Services",
                            command=lambda: controller.show_frame(PageThree))
        homepage.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        insights = ttk.Button(self, text="Back to Data Insights",
                              command=lambda: controller.show_frame(Insights))
        insights.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        runRcode= ttk.Button(self, text="Run R code",
                              command=lambda: display_output("C:/Users/PC/PycharmProjects/pythonProject25/11_Oplog.R"))
        runRcode.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class IAM(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text= "Integer Allocation Model", font=LARGE_FONT)
        label.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        runmodel = ttk.Button(self, text="Run Integer Allocation Model", command=lambda:self.run_model())
        runmodel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        services = ttk.Button(self, text="Back to Provided Services",
                              command=lambda: controller.show_frame(PageThree))
        services.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def run_model(self):
        running_window = RunningWindowIAM(self)
        running_window.grab_set()

        model_thread = threading.Thread(target=self.runmodel_thread)
        model_thread.start()

        self.check_model_thread(model_thread, running_window)

    def runmodel_thread(self):
        import AllocationModel as iam
        path_to_gurobipy = "C:/Users/PC/PycharmProjects/pythonProject23/venv/Lib/site-packages/gurobipy"
        os.environ["PYTHONPATH"] = path_to_gurobipy
        result = iam.AllocationModel()
        return result

    def check_model_thread(self,model_thread, running_window):
        if model_thread.is_alive():
            self.after(100, lambda: self.check_model_thread(model_thread, running_window)) #checking if the model is ended or still running every 100ms.
        else:
            #Model thread has finished, so close the "running" pop-up window and display the solution.
            running_window.destroy()
            solution_output = self.runmodel_thread()
            solution_window = SolutionWindowIAM(self, solution_output)
            solution_window.grab_set()

class RunningWindowIAM(tk.Toplevel): #Pop-up window that displays the statement that model is running.
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Currently Running")
        self.label = tk.Label(self, text="The program is currently running. Please wait.")
        self.label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class SolutionWindowIAM(tk.Toplevel): #burdaki çıkan ekrandan kaydedilebiliyor ama csv değil pickle diye bişi?
    def __init__(self, parent, result):
        super().__init__(parent)
        self.title("Outputs of Integer Programming Model for Allocation")
        self.label = tk.Label(self, text="The program has finished running.")
        self.label.grid(row=0, column=0, sticky="nsew")

        self.table = Table(self, dataframe=result, showtoolbar=True, showstatusbar=True)
        self.table.grid(row=1, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.table.show(self)



app = AllocationApp()
#app.geometry("1280x720")
app.geometry("1000x500")
app.mainloop()
