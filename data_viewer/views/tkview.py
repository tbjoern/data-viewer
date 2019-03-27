from data_viewer.interfaces import View

from tkinter import *
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

STICKY_ALL = (N,W,E,S)

class Window(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Data Viewer")
        self.pack(fill=BOTH, expand=True)

        self.setup_menu()

        self.setup_data_view()

        self.setup_archive_selector()

        self.setup_plot_view()

        self.configure_grid()

    def configure_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=0)

    def setup_plot_view(self):
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=STICKY_ALL, rowspan=2)

    def setup_archive_selector(self):
        self.archive_selector = ArchiveSelector(self)
        self.archive_selector.grid(column=0, row=1, sticky=STICKY_ALL)

    def setup_data_view(self):
        self.data_view = ScrollList(self)
        self.data_view.grid(column=0, row=0, sticky=STICKY_ALL)

    def setup_menu(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu, tearoff=0)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

    def client_exit(self):
        exit()

class ScrollList(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.listbox = Listbox(self)
        self.listbox.grid(column=0, row=0, sticky=STICKY_ALL)

        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(column=1, row=0, sticky=(N,S))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.items = []

    def add_item(self, item):
        self.items.append(item)
        self.listbox.insert('end', str(item))

    def clear(self):
        self.items = []
        self.listbox.delete(0, END)

class ArchiveSelector(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.label = Label(self, text='open archive: <none>')
        self.label.pack()
        self.button = Button(self, text='select archive')
        self.button.pack()

class TKView(View):
    def __init__(self, controller):
        self.controller = controller
        self.root = Tk()
        self.app = Window(self.root)

    def loop(self):
        self.root.mainloop()

    def display_list(self, items, handler):
        view = self.app.data_view
        view.clear()
        for item in items:
            view.add_item(item)

    def display_plot(self, plot):
        raise NotImplementedError()
