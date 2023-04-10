import io
import tkinter
from tkinter import *
from tkinter.ttk import Combobox

import pygame
import serial
import serial.tools.list_ports
from serial import Serial


class Controller:
    def __init__(self):
        self.connection = None
        self.x = 2048
        self.y = 2048
        self.but1 = 0
        self.but2 = 0
        self.butj = 0
        self.stop = False

    def connect(self):
        dialog_root = Tk()
        dialog_root.title("Choose COM port:")
        dialog_root.geometry("500x100")

        available_comports = serial.tools.list_ports.comports()
        port_choices = [(port + ": " + desc) for port, desc, hwid in sorted(available_comports)]
        port_choice = StringVar()
        port_choice.set(port_choices[1])

        combo_box = Combobox(dialog_root, values=port_choices, textvariable=port_choice, state="readonly")
        combo_box.pack(padx=10, pady=10, fill=tkinter.X, expand=True)

        button = Button(dialog_root, text="OK", command=dialog_root.destroy)
        button.pack(padx=10, fill=tkinter.X, expand=True)

        dialog_root.mainloop()

        target_port = port_choice.get().split(":")[0]
        serial_connection = serial.Serial(port=target_port,
                                          baudrate=9600,
                                          timeout=1)
        if not serial_connection.isOpen():
            serial_connection.open()

        self.connection = serial_connection

    def disconnect(self):
        self.connection.close()

    def read_input(self):
        while True:
            if self.stop:
                return
            try:
                raw_data = self.connection.read_until(b"\r\n")
                raw_data_str = raw_data.decode("utf-8").replace("\n", "").replace("\r", "").strip()
                raw_data_split = raw_data_str.split(" ")

                raw_data_dict = {}
                for raw_data in raw_data_split:
                    name_value = raw_data.split(":")
                    raw_data_dict[name_value[0]] = name_value[1]

                self.x = int(raw_data_dict["x"])
                self.y = int(raw_data_dict["y"])
                self.but1 = int(raw_data_dict["but1"])
                self.but2 = int(raw_data_dict["but2"])
                self.butj = int(raw_data_dict["butj"])
            except:
                pass





