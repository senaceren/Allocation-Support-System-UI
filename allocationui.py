import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import PIL
from PIL import Image, ImageTk

import customtkinter
import matplotlib
import customtkinter as ctk

matplotlib.use("TkAgg") #backend of matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import os
import subprocess
import sys
import threading
from io import StringIO
from pandastable import *


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

#UI'deki yazı tiplerini tanımlamak için.
LARGE_FONT = ("Georgia",24)
NORM_FONT = ("Georgia",18)
SMALL_FONT = ("Georgia",14)

# Pop-up mesaj çıkmasını sağlayan fonksiyon. Input'u direkt çıkılması istenen mesaj.
def popupmsg(msg):
    popup = ctk.CTk()
    popup.wm_title("!")
    label = ctk.CTkLabel(popup, text = msg, font= NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ctk.CTkButton(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.geometry("300x300")
    popup.mainloop()


# Bu fonksiyon input olarak R dosyalarının pathlerini alıp (data düzenlemesi vs için kullanılan), R dosyalarını çalıştırıp çıktılarını returnluyor.
def run_R_script(script_path):
    process = subprocess.Popen(["Rscript", script_path], stdout=subprocess.PIPE, stderr= subprocess.PIPE)
    output, error = process.communicate()
    return output.decode('utf-8')

# Bu da R dosyalarından elde edilen çıktıların bir window olarak user'a sunulması adına.
def display_output(script_path):
    outputwindow = tk.Toplevel()
    outputwindow.title("Output")
    output = run_R_script(script_path)
    output_label = ttk.Label(outputwindow,text=output)
    output_label.pack()

# Bu yaptığımız Allocation App'in ana frame'ini oluşturuyor.
class AllocationApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        ctk.CTk.wm_title(self, "Pro-active Inventory Allocation Decision Support System")

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0,weight=1)


        #Bu şekilde yukarı kısma menü için bir şeyler eklenilebilir, dileğe göre customized edilebilir. Yukarıdaki menubar'ı tanımlıyor.
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

        for F in (StartPage, PageThree, Insights, DataUpdate, Charts, IAM, DataPreparation, Zones,
                  Forecast): # Bu windowlar arasındaki geçişi sağlıyor. Eklenmiş herhangi bir class window buraya da eklenmeli.
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#Burası şu anlık sizin tarafınızdan headless olarak kullanılacağı için tanımlı değil.
#Sisteminize nasıl entegre edeceğinize göre login page olarak kullanılabilir ya da kaldırılabilir.

class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Login Page", font=LARGE_FONT)
        label.pack(pady=10, padx= 10)
        label1 = ctk.CTkLabel(self, text="Please enter information below to log in.")
        label1.pack()

        username = tk.StringVar()
        password = tk.StringVar()

        username_label = ctk.CTkLabel(self, text="Username:")
        username_label.pack()
        username_entry = ctk.CTkEntry(self, textvariable=username)
        username_entry.pack()

        password_label = ctk.CTkLabel(self, text="Password:")
        password_label.pack()
        password_entry = ctk.CTkEntry(self, textvariable=password, show="*")
        password_entry.pack()

        ctk.CTkLabel(self, text="").pack()

        button = ctk.CTkButton(self, text="Login")
        button.pack()

        #Login kısmını aktif yapıcak DB ve error mesajları kısmı eklemesi yapılabilir buraya eğer DB ile bağlanılıp kullanılacaksa.

        buttonapp = ctk.CTkButton(self, text="See Service Available",
                            command=lambda: controller.show_frame(PageThree))
        buttonapp.pack()

# Sağlanan servisleri gösteren ana pencere. Butonlarla belirlenen diğer servislerin pencerelerine bağlantı sağlanıyor.
class PageThree(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self,parent)

        canvas = ctk.CTkCanvas(self, borderwidth=0, highlightthickness=0, bg="white")
        frame= ctk.CTkFrame(canvas)
        frame.pack(side=ctk.TOP, fill= ctk.BOTH, expand=TRUE)
        vsb = ctk.CTkScrollbar(self, orientation=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=ctk.RIGHT, fill=ctk.Y)

        label = ctk.CTkLabel(frame, text= "Provided Services",  font=LARGE_FONT, width=120,
                               height=25,
                               fg_color=("#004679", "gray75"),
                               corner_radius=2, text_color="white")
        label.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

        add_forecast_image = ctk.CTkImage(PIL.Image.open("icons/forecast.png").resize((1000,1000), PIL.Image.Resampling.LANCZOS))
        add_cluster_image = ctk.CTkImage(PIL.Image.open("icons/cluster.png").resize((1000,1000), PIL.Image.Resampling.LANCZOS))
        add_data_image = ctk.CTkImage(PIL.Image.open("icons/data.png").resize((1000,1000), PIL.Image.Resampling.LANCZOS))
        add_model_image = ctk.CTkImage(PIL.Image.open("icons/model.png").resize((1000,1000), PIL.Image.Resampling.LANCZOS))

        button5 = ctk.CTkButton(frame, image= add_forecast_image, width=400, height=100, text="Run Forecast Methods", font= SMALL_FONT, compound="left",
                             command=lambda: controller.show_frame(Forecast))
        button5.pack(ipadx=20, ipady= 20, side= ctk.LEFT, expand=True)

        button6 = ctk.CTkButton(frame, image=add_cluster_image, text="Update and Show Zones", font= SMALL_FONT,  width=400, height=100, compound="left",
                             command=lambda: controller.show_frame(Zones))
        button6.pack(side=ctk.RIGHT, ipadx=20, ipady= 20, expand=True)

        button8 = ctk.CTkButton(frame, image=add_data_image, text="Update and Show Insights", font= SMALL_FONT, width=400, height=100, compound="left",
                             command=lambda: controller.show_frame(Insights))
        button8.pack(side=tk.TOP, ipadx=20, ipady= 20, anchor=ctk.E, expand=True)

        button9 = ctk.CTkButton(frame, image=add_model_image, text="Integer Allocation Model", font= SMALL_FONT, width=400, height=100, compound="left",
                             command=lambda: controller.show_frame(IAM))
        button9.pack(side=tk.TOP, ipadx=20, ipady= 20, anchor=ctk.E, expand=True)

        button10 = ctk.CTkButton(frame, text="Log out", font= SMALL_FONT, width=400, height=100,
                             command=lambda: controller.show_frame(StartPage))
        button10.pack(side=tk.TOP, ipadx=20, ipady= 20, anchor=ctk.CENTER, expand=True)

        frame.update_idletasks()
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.config(scrollregion=canvas.bbox("all"))


# Bu window şu noktada disabled. Kullanmak isterseniz bu tarz bir window ile csv uzantılı dosyalar sisteme ekleyebilir (ya da direkt DB'den),
# Sonrasında da buraya yüklenen dataları diğer pencelerde kullanabilirsiniz.
class DataUpdate(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self,parent)
        label = ctk.CTkLabel(self, text= "Data Update", font=LARGE_FONT)
        label.pack(pady=10, padx= 10)

        # Dosya yüklemek için olan fonksiyon. Bilgisayardan direkt dosya yüklemek için.
        def browseFiles():
            filename = filedialog.askopenfilename(initialdir="/", title="Select a File",filetypes=(("Text files","*.txt*"),("all files","*.*")))

            # Change label contents
            label_file_explorer.configure(text="File Opened: " + filename)

        label_file_explorer = tk.Label(self,
                                    text="File Explorer using Tkinter",
                                    width=100, height=4,
                                    fg="blue")

        button_explore = ctk.CTkButton(self, text="Browse Files", command=browseFiles)
        button_explore.pack()

        homepage = ctk.CTkButton(self, text="Back to Provided Services",
                            command=lambda: controller.show_frame(PageThree))
        homepage.pack()


#Forecast penceresi. Bu noktada forecastleri uygulamak için zone bazında butonlar bulunmakta.
#Gösterim için şu noktada zone2 için olan buton çalışmakta.

class Forecast(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self,parent)
        label = ctk.CTkLabel(self, text= "Forecasting Methods", font=LARGE_FONT,width=120,
                               height=25,
                               fg_color=("#004679", "gray75"),
                               corner_radius=2, text_color="white")

        label.pack(side=tk.TOP, pady=10, fill=tk.BOTH, expand=True)

        zone1 = ctk.CTkButton(self, text="Apply Forecast Methods for Zone 1",
                              command=lambda:self.run_forecast1())
        zone1.pack(side=tk.TOP, pady=10, padx= 100, fill=tk.BOTH, expand=True)

        zone2 = ctk.CTkButton(self, text="Apply Forecast Methods for Zone 2",
                              command= lambda:self.run_forecast2())
        zone2.pack(side=tk.TOP, pady=10, padx= 100,fill=tk.BOTH, expand=True)

        zone3 = ctk.CTkButton(self, text="Apply Forecast Methods for Zone 3",
                              command=lambda:self.run_forecast3())
        zone3.pack(side=tk.TOP, pady=10, padx= 100,fill=tk.BOTH, expand=True)

        zone4 = ctk.CTkButton(self, text="Apply Forecast Methods for Zone 4",
                              command=lambda:self.run_forecast4())
        zone4.pack(side=tk.TOP, pady=10,padx= 100, fill=tk.BOTH, expand=True)

        zone5 = ctk.CTkButton(self, text="Apply Forecast Methods for Zone 5",
                              command=lambda:self.run_forecast5())
        zone5.pack(side=tk.TOP, pady=10, padx= 100,fill=tk.BOTH, expand=True)

        tocsv = ctk.CTkButton(self, text="Download Forecast Results as CVS",
                              command=lambda: controller.show_frame(PageThree))
        tocsv.pack(side=tk.TOP, pady=10,padx= 100, fill=tk.BOTH, expand=True)

        services = ctk.CTkButton(self, text="Back to Provided Services",
                            command=lambda: controller.show_frame(PageThree))
        services.pack(side=tk.TOP,pady=10,padx= 100, fill=tk.BOTH, expand=True)

    #FORECASTLER İÇİN:

    #Forecast for Zone 1

    def run_forecast1(self):
        running_window1 = RunningWindowForecast1(self)
        running_window1.grab_set()

        model_thread1 = threading.Thread(target=self.runforecast_thread1)
        model_thread1.start()

        self.check_model_thread1(model_thread1, running_window1)

    def runforecast_thread1(self):
        import Intermittent as fc1
        #import ForecastUII as frq
        import MA as ma
        file1 = "Forecast/for_croston.rds"
        Zone = "Zone_1"
        file2 = "Forecast/for_ma.rds"
        result1_1 = fc1.intermittent(file1,Zone)
        #result1-2 = frq.frequent()
        result1_3 = ma.MA(file2, Zone)
        final1 = pd.concat([result1_1, result1_3])
        return final1

    # Checking if the model is ended or still running every 100ms.
    def check_model_thread1(self,model_thread1, running_window1):
        if model_thread1.is_alive():
            self.after(100, lambda: self.check_model_thread1(model_thread1, running_window1))
        else:
            #Model thread has finished, so close the "running" pop-up window and display the solution.
            running_window1.destroy()
            solution_output1 = self.runforecast_thread1()
            solution_window1 = SolutionWindowForecast1(self, solution_output1)
            solution_window1.grab_set()

    #Forecast for Zone 2

    #Forecast doyasının durumlarını kontrol eden, çalışmakta olan windowu (aşağıda tanımlı) kontrol eden fonksiyon.
    def run_forecast2(self):
        running_window2 = RunningWindowForecast2(self)
        running_window2.grab_set()

        model_thread2 = threading.Thread(target=self.runforecast_thread2)
        model_thread2.start()

        self.check_model_thread2(model_thread2, running_window2)

    #Forecast dosyasını çalışmak için olan fonskiyon. Forecast python dosyası import ediliyor. İstenirse path şeklinde aşağıdaki gibi de tanımlanabilir.
    def runforecast_thread2(self):
        import Intermittent as fc1
        #import ForecastUII as frq
        import MA as ma
        file1 = "Forecast/for_croston.rds"
        Zone = "Zone_2"
        file2 = "Forecast/for_ma.rds"
        result1_1 = fc1.intermittent(file1,Zone)
        #result1-2 = frq.frequent()
        result1_3 = ma.MA(file2, Zone)
        final2 = pd.concat([result1_1, result1_3])
        return final2

    # Checking if the model is ended or still running every 100ms.
    def check_model_thread2(self,model_thread2, running_window2):
        if model_thread2.is_alive():
            self.after(100, lambda: self.check_model_thread2(model_thread2, running_window2))
        else:
            #Model thread has finished, so close the "running" pop-up window and display the solution.
            running_window2.destroy()
            solution_output2 = self.runforecast_thread2()
            solution_window2 = SolutionWindowForecast2(self, solution_output2)
            solution_window2.grab_set()

    #Forecast for Zone 3

    #Forecast doyasının durumlarını kontrol eden, çalışmakta olan windowu (aşağıda tanımlı) kontrol eden fonksiyon.
    def run_forecast3(self):
        running_window3 = RunningWindowForecast3(self)
        running_window3.grab_set()

        model_thread3 = threading.Thread(target=self.runforecast_thread3)
        model_thread3.start()

        self.check_model_thread2(model_thread3, running_window3)

    #Forecast dosyasını çalışmak için olan fonskiyon. Forecast python dosyası import ediliyor. İstenirse path şeklinde aşağıdaki gibi de tanımlanabilir.
    def runforecast_thread3(self):
        import Intermittent as fc1
        #import ForecastUII as frq
        import MA as ma
        file1 = "Forecast/for_croston.rds"
        Zone = "Zone_3"
        file2 = "Forecast/for_ma.rds"
        result1_1 = fc1.intermittent(file1,Zone)
        #result1-2 = frq.frequent()
        result1_3 = ma.MA(file2, Zone)
        final3 = pd.concat([result1_1, result1_3])
        return final3

    # Checking if the model is ended or still running every 100ms.
    def check_model_thread3(self,model_thread3, running_window3):
        if model_thread3.is_alive():
            self.after(100, lambda: self.check_model_thread3(model_thread3, running_window3))
        else:
            #Model thread has finished, so close the "running" pop-up window and display the solution.
            running_window3.destroy()
            solution_output3 = self.runforecast_thread2()
            solution_window3 = SolutionWindowForecast2(self, solution_output3)
            solution_window3.grab_set()

    #Forecast for Zone 4

    #Forecast doyasının durumlarını kontrol eden, çalışmakta olan windowu (aşağıda tanımlı) kontrol eden fonksiyon.
    def run_forecast4(self):
        running_window4 = RunningWindowForecast4(self)
        running_window4.grab_set()

        model_thread4 = threading.Thread(target=self.runforecast_thread4)
        model_thread4.start()

        self.check_model_thread4(model_thread4, running_window4)

    #Forecast dosyasını çalışmak için olan fonskiyon. Forecast python dosyası import ediliyor. İstenirse path şeklinde aşağıdaki gibi de tanımlanabilir.
    def runforecast_thread4(self):
        import Intermittent as fc1
        #import ForecastUII as frq
        import MA as ma
        file1 = "Forecast/for_croston.rds"
        Zone = "Zone_4"
        file2 = "Forecast/for_ma.rds"
        result1_1 = fc1.intermittent(file1,Zone)
        #result1-2 = frq.frequent()
        result1_3 = ma.MA(file2, Zone)
        final4 = pd.concat([result1_1, result1_3])
        return final4

    # Checking if the model is ended or still running every 100ms.
    def check_model_thread4(self,model_thread4, running_window4):
        if model_thread4.is_alive():
            self.after(100, lambda: self.check_model_thread2(model_thread4, running_window4))
        else:
            #Model thread has finished, so close the "running" pop-up window and display the solution.
            running_window4.destroy()
            solution_output4 = self.runforecast_thread4()
            solution_window4 = SolutionWindowForecast2(self, solution_output4)
            solution_window4.grab_set()

    #Forecast for Zone 5

    #Forecast doyasının durumlarını kontrol eden, çalışmakta olan windowu (aşağıda tanımlı) kontrol eden fonksiyon.
    def run_forecast5(self):
        running_window5 = RunningWindowForecast5(self)
        running_window5.grab_set()

        model_thread5 = threading.Thread(target=self.runforecast_thread5)
        model_thread5.start()

        self.check_model_thread5(model_thread5, running_window5)

    #Forecast dosyasını çalışmak için olan fonskiyon. Forecast python dosyası import ediliyor. İstenirse path şeklinde aşağıdaki gibi de tanımlanabilir.
    def runforecast_thread5(self):
        import Intermittent as fc1
        #import ForecastUII as frq
        import MA as ma
        file1 = "Forecast/for_croston.rds"
        Zone = "Zone_5"
        file2 = "Forecast/for_ma.rds"
        result1_1 = fc1.intermittent(file1,Zone)
        #result1-2 = frq.frequent()
        result1_3 = ma.MA(file2, Zone)
        final5 = pd.concat([result1_1, result1_3])
        return final5

    # Checking if the model is ended or still running every 100ms.
    def check_model_thread5(self,model_thread5, running_window5):
        if model_thread5.is_alive():
            self.after(100, lambda: self.check_model_thread2(model_thread5, running_window5))
        else:
            #Model thread has finished, so close the "running" pop-up window and display the solution.
            running_window5.destroy()
            solution_output5 = self.runforecast_thread5()
            solution_window5 = SolutionWindowForecast5(self, solution_output5)
            solution_window5.grab_set()

#Running Windows for Forecast

class RunningWindowForecast1(ctk.CTkToplevel): #Pop-up window that displays the statement that model is running.
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Currently Running")
        add_waiting_image = ctk.CTkImage(PIL.Image.open("icons/pop-up.jpg").resize((1000, 1000), PIL.Image.Resampling.LANCZOS))
        self.label = ctk.CTkLabel(self, text="The program is currently running. Please wait.", font=SMALL_FONT, image=add_waiting_image, compound="bottom")
        self.label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.geometry("300x300")

class RunningWindowForecast2(ctk.CTkToplevel): #Pop-up window that displays the statement that model is running.
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Currently Running")
        add_waiting_image = ctk.CTkImage(PIL.Image.open("icons/pop-up.jpg").resize((1000, 1000), PIL.Image.Resampling.LANCZOS))
        self.label = ctk.CTkLabel(self, text="The program is currently running. Please wait.", font=SMALL_FONT, image=add_waiting_image, compound="bottom")
        self.label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.geometry("300x300")

class RunningWindowForecast3(ctk.CTkToplevel): #Pop-up window that displays the statement that model is running.
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Currently Running")
        add_waiting_image = ctk.CTkImage(PIL.Image.open("icons/pop-up.jpg").resize((1000, 1000), PIL.Image.Resampling.LANCZOS))
        self.label = ctk.CTkLabel(self, text="The program is currently running. Please wait.", font=SMALL_FONT, image=add_waiting_image, compound="bottom")
        self.label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.geometry("300x300")

class RunningWindowForecast4(ctk.CTkToplevel): #Pop-up window that displays the statement that model is running.
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Currently Running")
        add_waiting_image = ctk.CTkImage(PIL.Image.open("icons/pop-up.jpg").resize((1000, 1000), PIL.Image.Resampling.LANCZOS))
        self.label = ctk.CTkLabel(self, text="The program is currently running. Please wait.", font=SMALL_FONT, image=add_waiting_image, compound="bottom")
        self.label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.geometry("300x300")

class RunningWindowForecast5(ctk.CTkToplevel): #Pop-up window that displays the statement that model is running.
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Currently Running")
        add_waiting_image = ctk.CTkImage(PIL.Image.open("icons/pop-up.jpg").resize((1000, 1000), PIL.Image.Resampling.LANCZOS))
        self.label = ctk.CTkLabel(self, text="The program is currently running. Please wait.", font=SMALL_FONT, image=add_waiting_image, compound="bottom")
        self.label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.geometry("300x300")

#Solution Windows For Forecast

class SolutionWindowForecast1(ctk.CTkToplevel): #Çalışması bittikten sonra sonuçları gösteren pencere.
    def __init__(self, parent, final1):
        super().__init__(parent)
        self.title("Outputs of Forecasting Methods")
        self.label = ctk.CTkLabel(self, text="The program has finished running.")
        self.label.grid(row=0, column=0, sticky="nsew")

        self.table = Table(self, dataframe=final1, showtoolbar=True, showstatusbar=True)
        self.table.grid(row=1, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.table.show(self)

class SolutionWindowForecast2(ctk.CTkToplevel):  # Çalışması bittikten sonra sonuçları gösteren pencere.
    def __init__(self, parent, final2):
        super().__init__(parent)
        self.title("Outputs of Forecasting Methods")
        self.label = ctk.CTkLabel(self, text="The program has finished running.")
        self.label.grid(row=0, column=0, sticky="nsew")

        self.table = Table(self, dataframe=final2, showtoolbar=True, showstatusbar=True)
        self.table.grid(row=1, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.table.show(self)

class SolutionWindowForecast3(ctk.CTkToplevel):  # Çalışması bittikten sonra sonuçları gösteren pencere.
    def __init__(self, parent, final3):
        super().__init__(parent)
        self.title("Outputs of Forecasting Methods")
        self.label = ctk.CTkLabel(self, text="The program has finished running.")
        self.label.grid(row=0, column=0, sticky="nsew")

        self.table = Table(self, dataframe=final3, showtoolbar=True, showstatusbar=True)
        self.table.grid(row=1, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.table.show(self)

class SolutionWindowForecast4(ctk.CTkToplevel):  # Çalışması bittikten sonra sonuçları gösteren pencere.
    def __init__(self, parent, final4):
        super().__init__(parent)
        self.title("Outputs of Forecasting Methods")
        self.label = ctk.CTkLabel(self, text="The program has finished running.")
        self.label.grid(row=0, column=0, sticky="nsew")

        self.table = Table(self, dataframe=final4, showtoolbar=True, showstatusbar=True)
        self.table.grid(row=1, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.table.show(self)

class SolutionWindowForecast5(ctk.CTkToplevel):  # Çalışması bittikten sonra sonuçları gösteren pencere.
    def __init__(self, parent, final5):
        super().__init__(parent)
        self.title("Outputs of Forecasting Methods")
        self.label = ctk.CTkLabel(self, text="The program has finished running.")
        self.label.grid(row=0, column=0, sticky="nsew")

        self.table = Table(self, dataframe=final5, showtoolbar=True, showstatusbar=True)
        self.table.grid(row=1, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.table.show(self)

#Bu window şu noktada disabled. Kullanılmak isteniyorsa cluster algoritması yerleştirilip user'a açık bir şekilde görüntülenebilir.

class Zones(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text="Update and Show Zones", font=LARGE_FONT, width=120,
                             height=25,
                             fg_color=("#004679", "gray75"),
                             corner_radius=2, text_color="white")
        label.pack(side=tk.TOP, fill=tk.BOTH, pady=10, expand=True)

        panedwindow1 = ttk.Panedwindow(self, orient=HORIZONTAL)
        panedwindow1.pack(fill=tk.BOTH, expand=TRUE)

        self.left1 = ttk.Frame(panedwindow1, width=100, height=300, relief=SUNKEN)
        self.right1 = ttk.Frame(panedwindow1, width=400, height=400, relief=SUNKEN)

        updatezones = ctk.CTkButton(self.left1, text="Update and Visualize Zones",
                                    command=lambda: self.run_script())
        updatezones.pack(side=tk.TOP, fill=tk.BOTH, pady=10, padx=10, expand=True)

        services = ctk.CTkButton(self.left1, text="Back to Provided Services",
                                 command=lambda: controller.show_frame(PageThree))
        services.pack(side=tk.TOP, fill=tk.BOTH, pady=10, padx=10, expand=True)

        panedwindow1.add(self.left1, weight=1)
        panedwindow1.add(self.right1, weight=4)

    def run_script(self):
        map = PIL.ImageTk.PhotoImage(PIL.Image.open("Graph/map.png"))
        label = ctk.CTkLabel(self.right1, image =map)
        label.pack()


#Bu noktada bu window disabled. İsteğe göre, belirlenen data insightlarını user'a sucacak şekilde düzenlenilebilir.
class Insights(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self,parent)
        label = ctk.CTkLabel(self, text= "Data Analysis Insights", font=LARGE_FONT,width=120,
                               height=25,
                               fg_color=("#004679", "gray75"),
                               corner_radius=2, text_color="white")
        label.pack(side=tk.TOP, fill=tk.BOTH, pady= 10 ,expand = True)

        uniquebutton = ctk.CTkButton(self, text="Show Number of Unique Products per Zone Chart",
                            command=lambda: self.sales_graph1())
        uniquebutton.pack(side=tk.TOP, pady=10, padx= 100, fill=tk.BOTH, expand=True)

        salesbutton = ctk.CTkButton(self, text="Number of Weeks Subject To Sales Product Counts per Zone Chart",
                                    command=lambda: self.sales_graph2())
        salesbutton.pack(side=tk.TOP, pady=10, padx=100, fill=tk.BOTH, expand=True)

        sfrbutton = ctk.CTkButton(self, text="Sales Frequency Ratio Product Counts per Zone Chart",
                                    command=lambda: self.sales_graph3())
        sfrbutton.pack(side=tk.TOP, pady=10, padx=100, fill=tk.BOTH, expand=True)

        homepage = ctk.CTkButton(self, text="Back to Provided Services",
                              command=lambda: controller.show_frame(PageThree))
        homepage.pack(side=tk.TOP, pady=10, padx=100, fill=tk.BOTH, expand=True)

    def sales_graph1(self):
        import graphcreate as gc
        graph1 = gc.number_unique()
        canvas = FigureCanvasTkAgg(graph1, self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def sales_graph2(self):
        import graphcreate as gc
        graph2 = gc.number_sales()
        canvas = FigureCanvasTkAgg(graph2, self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def sales_graph3(self):
        import graphcreate as gc
        graph3 = gc.number_sales()
        canvas = FigureCanvasTkAgg(graph3, self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


        #canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #Datayı forecast için hazırlayan R dosyasının çalışımı (isteğe göre enabled edilebilir).

        #def R_prepareforML():
            #subprocess.call(["Rscript", "22_Oplog.R"], shell= True)
            #popup = tk.Tk()
            #popup.wm_title("Data Preparation")
            #label = ttk.Label(popup, text="Data Preparation Completed.", font= NORM_FONT)
            #label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            #b1 = ttk.Button(popup, text="Okay", command = popup.destroy)
            #b1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #Datayı düzenleyen R dosyasının çalışımı, isteğe göre enabled edilebilir.
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



        #weekofsalesbutton = ttk.Button(self, text="Show Chart of Start Week of Sales",
                            #command=lambda: controller.show_frame(Start))
        #weekofsalesbutton.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #nowsoldbutton = ttk.Button(self, text="Show Chart of Number of Weeks Sold",
                            #command=lambda: controller.show_frame(NoWSold))
        #nowsoldbutton.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #productclass = ttk.Button(self, text="Show Product Classification Chart",
                            #command=lambda: controller.show_frame(ProdClass))
        #productclass.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #manipulatedata = ttk.Button(self, text="Adjust Address and Sales Excel Files",
                            #command=R_datamanipulation)
        #manipulatedata.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



#Bu pencere şu an disabled. Burada, sizden gelecek feedback'e göre, grafik olarak gösterilmesi istenen plotlar display edilebilir.
#Alttaki plot sadece örnek oluşturmak adına bir gösterim.
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

# Bu window dataları düzenlemek adına olan R dosyasını çalıştırıyor.
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

# Bu pencerede integer allocation model çalışıyor. Dosyanın okunması ve çıktılarının alınması evreleri forecast ile aynı şekilde design edilmiş durumdan.
class IAM(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self,parent)
        self.controller = controller
        label = ctk.CTkLabel(self, text= "Integer Allocation Model", font=LARGE_FONT,width=120,
                               height=25,
                               fg_color=("#004679", "gray75"),
                               corner_radius=2, text_color="white")
        label.pack(side=tk.TOP, fill=tk.BOTH, pady= 10 ,expand = True)

        panedwindow = ttk.Panedwindow(self, orient=HORIZONTAL)
        panedwindow.pack(fill=tk.BOTH, expand=TRUE)

        self.left = ttk.Frame(panedwindow, width=100, height=300, relief=SUNKEN)
        self.right = ttk.Frame(panedwindow, width =400, height=400, relief=SUNKEN)

        runmodel = ctk.CTkButton(self.left, text="Run Integer Allocation Model",font=SMALL_FONT, command=lambda:self.run_model())
        runmodel.pack(side=tk.TOP, fill=tk.BOTH, pady= 10,  padx= 10,expand=True)

        services = ctk.CTkButton(self.left, text="Back to Provided Services", font=SMALL_FONT,
                              command=lambda: controller.show_frame(PageThree))
        services.pack(side=tk.TOP, fill=tk.BOTH, pady = 10,padx=10 ,expand=True)

        panedwindow.add(self.left, weight=1)
        panedwindow.add(self.right, weight=4)


    def run_model(self):
        model_thread = threading.Thread(target=self.runmodel_thread)
        running_window = RunningWindowIAM(self, model_thread)
        running_window.grab_set()

        model_thread.start()

        self.check_model_thread(model_thread, running_window)

    def show_solution_window(self,result):
        self.table = Table(self.right, dataframe=result, showtoolbar=True, showstatusbar=True)
        self.table.show()

    #Burada gurobi için path tanımlanmış durumda.
    def runmodel_thread(self):
        import ModelLatest as iam
        path_to_gurobipy = "C:/Users/PC/PycharmProjects/pythonProject23/venv/Lib/site-packages/gurobipy"
        os.environ["PYTHONPATH"] = path_to_gurobipy
        import Parameter as pm
        file_freq = "IAM_Preperation/for_ML_v4.rds"
        file_inter = "IAM_Preperation/for_croston.rds"
        file_ma = "IAM_Preperation/for_ma.rds"
        file_direct = "IAM_Preperation/direct_assignment.rds"
        sales = "IAM_Preperation/new_sales_validation.rds"
        final = pm.parameter(file_freq, file_inter, file_ma, file_direct, sales)
        demand = final[['Zone_1','Zone_2','Zone_3','Zone_4','Zone_5']]
        supply = final['Sales']
        result = iam.AllocationModel(demand, supply)
        self.show_solution_window(result)

    #def check_model_thread(self,model_thread, running_window, right, show_solution_window):
    def check_model_thread(self, model_thread, running_window):
        if model_thread.is_alive():
            self.after(100, lambda: self.check_model_thread(model_thread, running_window)) #checking if the model is ended or still running every 100ms.
        else:
            running_window.destroy()

class RunningWindowIAM(ctk.CTkToplevel): #Pop-up window that displays the statement that model is running.
    def __init__(self,parent, model_thread):
        self.model_thread = model_thread
        super().__init__(parent)
        self.title("Currently Running")
        self.model_thread = model_thread
        add_waiting_image = ctk.CTkImage(PIL.Image.open("icons/pop-up.jpg").resize((1000, 1000), PIL.Image.Resampling.LANCZOS))
        self.label = ctk.CTkLabel(self, text="The program is currently running. Please wait.", font=SMALL_FONT, image=add_waiting_image, compound="bottom")
        self.label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.stop_button = ctk.CTkButton(self, text = "Cancel", command= self.cancel_model_thread)
        self.stop_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.geometry("300x300")
        self.stop_model = False

    def cancel_model_thread(self):
        self.stop_model = True
        self.destroy()
        # join() method waits until the thread finishes execution.
        # If join() method is not called, the thread will continue running even after the GUI is closed.
        #self.model_thread.join()




app = AllocationApp()
app.geometry("500x450")
app.mainloop()
