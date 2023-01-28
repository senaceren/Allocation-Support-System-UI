import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

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

class AllocationApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Inventory Allocation Decision Support System")

        container = tk.Frame(self)
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

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
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

app = AllocationApp()
app.geometry("1280x720")
app.mainloop()
