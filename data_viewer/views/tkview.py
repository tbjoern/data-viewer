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

        self.setup_iteration_field()

        self.setup_export_button()

        self.configure_grid()

    def setup_iteration_field(self):
        self.iteration_field = Entry(self)
        self.iteration_field.grid(row=2, column=2, sticky=STICKY_ALL)

    def setup_algorithm_view(self):
        self.algorithm_view = AlgorithmView(self)
        self.algorithm_view.grid(column=0, row=1, sticky=STICKY_ALL)

    def setup_plot_button(self):
        self.plot_button = Button(self, text='Plot item', command=self.plot_button_pressed)
        self.plot_button.grid(row=2, column=1, sticky=STICKY_ALL)

    def setup_export_button(self):
        self.export_button = Button(self, text='Export', command=self.export_button_pressed)
        self.export_button.grid(row=2, column=3, sticky=STICKY_ALL)

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

        self.plot_view = Frame(self)
        self.plot_view.grid(row=0, column=1, sticky=STICKY_ALL, rowspan=2, columnspan=3)
        self.plot_view.columnconfigure(0, weight=1)
        self.plot_view.rowconfigure(0, weight=1)
        self.plot_view.rowconfigure(1, weight=0)

        self.axes_buttons = Frame(self.plot_view)
        self.axes_buttons.grid(row=1, column=0, sticky=STICKY_ALL, rowspan=1, columnspan=1)
        self.axes_buttons.columnconfigure(0, weight=1)
        self.xaxis_radio_buttons = ButtonArray(self.axes_buttons)
        self.yaxis_radio_buttons = ButtonArray(self.axes_buttons)
        self.xaxis_radio_buttons.grid(row=0, column=0, sticky=STICKY_ALL)
        self.yaxis_radio_buttons.grid(row=1, column=0, sticky=STICKY_ALL)

        self.canvas = FigureCanvasTkAgg(f, self.plot_view)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=STICKY_ALL, rowspan=1, columnspan=1)

    def setup_archive_selector(self):
        self.archive_selector = ArchiveSelector(self, self.archive_selected)
        self.archive_selector.grid(column=0, row=2, sticky=STICKY_ALL)

    def setup_data_view(self):
        self.data_view = ScrollList(self, onselect=self.data_selected)
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

    def export_button_pressed(self):
        pass

    def data_selected(self, event):
        pass

class ButtonArray(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.radio_buttons = []
        self.selection = IntVar()

    def clear(self):
        for button in self.radio_buttons:
            button.destroy()

    def set_choices(self, choices):
        self.clear()
        for choice_name, choice_value in choices:
            radio_button = Radiobutton(self, text=choice_name, variable=self.selection, value=choice_value, indicatoron=0)
            radio_button.pack(side=LEFT, fill=BOTH, expand=True)
            self.radio_buttons.append(radio_button)


class ScrollList(ttk.Frame):
    def __init__(self, master=None, select_multiple=False, onselect=None):
        super().__init__(master)
        self.master = master

        selectmode = 'multiple' if select_multiple else 'single'

        self.listbox = Listbox(self, selectmode=selectmode)
        self.listbox.configure(exportselection=False)
        self.listbox.grid(column=0, row=0, sticky=STICKY_ALL)

        if onselect is not None:
            self.listbox.bind('<<ListboxSelect>>', onselect)

        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(column=1, row=0, sticky=(N,S))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.items = {}

    def add_item(self, name, item):
        self.items[name] = item
        self.listbox.insert('end', name)

    def clear(self):
        self.items = {}
        self.listbox.delete(0, END)

    def filter(self, matcher, mode):
        if mode == 'add':
            for index, name in enumerate(self.listbox.get(0, 'end')):
                if matcher(name):
                    self.listbox.selection_set(index)
        elif mode == 'remove':
            selected_items = ((index, self.listbox.get(index)) for index in self.listbox.curselection())
            for index, name in selected_items:
                if matcher(name):
                    self.listbox.selection_clear(index)

    def get_selection(self):
        return [self.items[self.listbox.get(i)] for i in self.listbox.curselection()]

    def toggle_select_all(self):
        selected_items = self.listbox.curselection()
        all_items = self.listbox.get(0, 'end')
        if len(selected_items) == len(all_items):
            self.listbox.selection_clear(0, 'end')
        else:
            self.listbox.selection_set(0, 'end')

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

class AlgorithmView(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.algorithm_view = ScrollList(self, select_multiple=True)
        self.algorithm_view.grid(row=0, column=0, sticky=STICKY_ALL, rowspan=1, columnspan=3)
        self.filter_button = Button(self, text='Add', command=self.filter_add)
        self.filter_button.grid(row=1, column=0, sticky=STICKY_ALL, rowspan=1, columnspan=1)
        self.filter_button = Button(self, text='Remove', command=self.filter_remove)
        self.filter_button.grid(row=1, column=1, sticky=STICKY_ALL, rowspan=1, columnspan=1)
        self.filter_field = Entry(self)
        self.filter_field.grid(row=1, column=2, sticky=STICKY_ALL, rowspan=1, columnspan=1)
        self.select_all_button = Button(self, text='select all', command=self.select_all)
        self.select_all_button.grid(row=2, column=0, sticky=STICKY_ALL, rowspan=1, columnspan=3)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
    
    def clear(self):
        self.algorithm_view.clear()

    def add_item(self, name, item):
        self.algorithm_view.add_item(name, item)
    
    def get_selection(self):
        return self.algorithm_view.get_selection()

    def filter_add(self):
        self.on_filter_button_press(mode='add')

    def filter_remove(self):
        self.on_filter_button_press(mode='remove')

    def parse_filter_field(self):
        filter_text = self.filter_field.get()
        filter = filter_text.split(',')
        filter = [t.strip() for t in filter]
        if filter_text == '':
            filter = []
        return filter

    def on_filter_button_press(self, mode):
        filter = self.parse_filter_field()
        def matcher(item):
            for token in filter:
                if not token in item:
                    return False
            return True
        self.algorithm_view.filter(matcher, mode)

    def select_all(self):
        self.algorithm_view.toggle_select_all()

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
        self.display_list(view, algorithms, handler)
    
    def display_list(self, view, items, handler):
        view.clear()
        for name, item in items:
            view.add_item(name, item)

    def display_plot(self, plot):
        self.current_plot = plot
        self.canvas.figure = self.current_plot.figure
        self.current_plot.figure.canvas = self.canvas
        self.canvas.draw()
        self.configure()

    def archive_selected(self, path):
        self.controller.open_path(path)

    def get_selected_algorithms(self):
        algorithms = self.algorithm_view.get_selection()
        return algorithms

    def plot_button_pressed(self):
        instance = self.data_view.get_selection()[0]
        if instance:
            self.controller.handle_item_selected(instance)

    def get_iteration_limit(self):
        text = self.iteration_field.get()
        try:
            return int(text)
        except:
            return None

    def export_button_pressed(self):
        self.controller.save_plot(self.current_plot)
    
    def get_selected_axes(self):
        xaxis = self.xaxis_radio_buttons.selection.get()
        yaxis = self.yaxis_radio_buttons.selection.get()
        return (xaxis, yaxis)

    def data_selected(self, event):
        instance = self.data_view.get_selection()[0]
        metadata = self.controller.item_metadata(instance)
        axes_choices = []
        for i, field in enumerate(metadata['fieldnames']):
            axes_choices.append((field,i))
        self.xaxis_radio_buttons.set_choices(axes_choices)
        self.yaxis_radio_buttons.set_choices(axes_choices)
