import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
from shutter_controller_master import ShutterController


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW")
        self.resizable(width=False, height=False)
        self.title("Shutter Controller")

        ConnectScreen(self)

        self.mainloop()

class ConnectScreen(ttk.Frame):
    def __init__(self, master):
        assert isinstance(master, App)
        self.master: App = master
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.port_lable = ttk.Label(self, text="port:", font=("", 15))
        self.port_lable.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)

        ports = serial.tools.list_ports.comports()
        self.port = tk.StringVar()
        self.com_input = ttk.Combobox(self, textvariable=self.port, state="readonly", width=20, font=("", 15))
        self.com_input["values"] = ports
        self.com_input.grid(row=0, column=1, sticky="nsew", pady=5, padx=5)

        self.baudrate_lable = ttk.Label(self, text="baudrate:", font=("", 15))
        self.baudrate_lable.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)

        self.baudrate = tk.StringVar()
        self.baudrate.set("9600")
        self.baudrate_input = ttk.Combobox(self, textvariable=self.baudrate, state="readonly", width=20, font=("", 15))
        self.baudrate_input["values"] = (9600, 115200)
        self.baudrate_input.grid(row=1, column=1, sticky="nsew", pady=5, padx=5)

        self.connect_button = ttk.Button(self, text="connect", command=self.connect_button)
        self.connect_button.grid(row=2, column=0, columnspan = 2, sticky = tk.W+tk.E, pady=5, padx=5)


        self.pack(expand=True)

    def connect_button(self):
        port, junk = self.port.get().split(" ", 1)
        baudrate = self.baudrate.get()
        shutter_controller = ShutterController(port, int(baudrate))

        self.pack_forget()
        MainWindow(self.master, shutter_controller)

class MainWindow(tk.Frame):
    def __init__(self, master, shutter_controller):
        assert isinstance(master, App)
        self.master: App = master
        super().__init__(master)

        self.shutter_controller = shutter_controller
        self.shutter_status = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.open_shutter_button = ttk.Button(self, text='Open shutter', command=self.shutter_controller.open_shutter)
        self.open_shutter_button.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=5, padx=5)
        self.close_shutter_button = ttk.Button(self, text='Close shutter', command=self.shutter_controller.close_shutter)
        self.close_shutter_button.grid(row=0, column=2, columnspan=3, sticky="nsew", pady=5, padx=5)

        self.lable_timed_exposure = ttk.Label(self, text="timed exposure:", font=("", 15))
        self.lable_timed_exposure.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)
        self.timed_exposure = tk.StringVar()
        self.timed_exposure_entry = ttk.Entry(self, textvariable=self.timed_exposure)
        self.timed_exposure_entry.grid(row=1, column=1, sticky="nsew", pady=5, padx=5)
        self.timed_exposure_time_unit = tk.StringVar()
        self.timed_exposure_time_unit.set("s")
        self.timed_exposure_time_unit_combox = ttk.Combobox(self, textvariable=self.timed_exposure_time_unit, state="readonly")
        self.timed_exposure_time_unit_combox['values'] = ('ms', 's', 'min', 'h')
        self.timed_exposure_time_unit_combox.grid(row=1, column=2, sticky="nsew", pady=5, padx=5)
        self.timed_exposure_expose_button = ttk.Button(self, text="Expose", command=self.expose_button)
        self.timed_exposure_expose_button.grid(row=1, column=3, sticky="nsew", pady=5, padx=5)
        self.timed_exposure_abort_button = ttk.Button(self, text="Abort", command=self.shutter_controller.abort_timed_exposure)
        self.timed_exposure_abort_button.grid(row=1, column=4, sticky="nsew", pady=5, padx=5)


        self.get_shutter_status()
        self.pack()

    def get_shutter_status(self):
        self.shutter_status = self.shutter_controller.get_status()
        if self.shutter_status:
            self.open_shutter_button.state(["disabled"])
            self.close_shutter_button.state(["!disabled"])
        elif not self.shutter_status:
            self.open_shutter_button.state(["!disabled"])
            self.close_shutter_button.state(["disabled"])
        self.after(500, self.get_shutter_status)

    def expose_button(self):
        exposure_time = float(self.timed_exposure.get())
        time_unit = self.timed_exposure_time_unit.get()

        self.shutter_controller.timed_exposure(exposure_time, time_unit)


App()