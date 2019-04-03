from data_viewer.interfaces import View

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

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

        self.setup_algorithm_view()

        self.setup_archive_selector()

        self.setup_plot_view()

        self.setup_plot_button()

        self.configure_grid()

    def setup_algorithm_view(self):
        self.algorithm_view = ScrollList(self, select_multiple=True)
        self.algorithm_view.grid(column=0, row=1, sticky=STICKY_ALL)

    def setup_plot_button(self):
        self.plot_button = Button(self, text='Plot item', command=self.plot_button_pressed)
        self.plot_button.grid(row=2, column=1, sticky=STICKY_ALL)

    def configure_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=0)

    def setup_plot_view(self):
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky=STICKY_ALL, rowspan=2)

    def setup_archive_selector(self):
        self.archive_selector = ArchiveSelector(self, self.archive_selected)
        self.archive_selector.grid(column=0, row=2, sticky=STICKY_ALL)

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

    def archive_selected(self):
        pass

    def plot_button_pressed(self):
        pass

class ScrollList(ttk.Frame):
    def __init__(self, master=None, select_multiple=False):
        super().__init__(master)
        self.master = master

        selectmode = 'multiple' if select_multiple else 'single'

        self.listbox = Listbox(self, selectmode=selectmode)
        self.listbox.configure(exportselection=False)
        self.listbox.grid(column=0, row=0, sticky=STICKY_ALL)

        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(column=1, row=0, sticky=(N,S))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.items = []

    def add_item(self, name, item):
        self.items.append(item)
        self.listbox.insert('end', name)

    def clear(self):
        self.items = []
        self.listbox.delete(0, END)

    def get_selection(self):
        return [self.items[i] for i in self.listbox.curselection()]

class ArchiveSelector(Frame):
    def __init__(self, master=None, button_handler=None):
        super().__init__(master)
        self.master = master
        self.button_handler = button_handler

        self.label = Label(self, text='selected archive: <none>')
        self.label.pack()
        self.button = Button(self, text='select archive', command=self.on_button_press)
        self.button.pack()

    def on_button_press(self):
        dir = filedialog.askdirectory()
        self.label.config(text=f'selected archive: {dir}')
        if self.button_handler:
            self.button_handler(dir)

class TKView(View, Window):
    def __init__(self, controller):
        self.controller = controller
        self.master = Tk()
        Window.__init__(self, self.master)

    def loop(self):
        self.master.mainloop()

    def display_instances(self, instances, handler):
        view = self.data_view
        items = ((instance, instance) for instance in instances)
        self.display_list(view, items, handler)

    def display_algorithms(self, algorithms, handler):
        view = self.algorithm_view
        items = ((algorithm.name, algorithm) for algorithm in algorithms)
        self.display_list(view, items, handler)
    
    def display_list(self, view, items, handler):
        view.clear()
        for name, item in items:
            view.add_item(name, item)

    def display_plot(self, plot):
        self.canvas.figure = plot
        plot.canvas = self.canvas
        self.canvas.draw()
        self.configure()

    def archive_selected(self, path):
        self.controller.open_path(path)

    def get_selected_algorithms(self):
        algorithms = self.algorithm_view.get_selection()
        print(algorithms)
        return algorithms

    def plot_button_pressed(self):
        instance = self.data_view.get_selection()[0]
        print(instance)
        if instance:
            self.controller.handle_item_selected(instance)
