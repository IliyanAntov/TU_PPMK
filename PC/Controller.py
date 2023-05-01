import tkinter
from tkinter import *
from tkinter.ttk import Combobox

import serial
import serial.tools.list_ports


class Controller:
    def __init__(self):
        self.connection = Controller.connect()
        self.x = 2048
        self.y = 2048
        self.but1 = 0
        self.but2 = 0
        self.butj = 0
        self.stop = False

    @staticmethod
    def connect() -> serial.Serial:
        # Create the dialog box window
        dialog_root = Tk()
        dialog_root.title("Choose COM port:")
        dialog_root.geometry("500x100")

        # Get a list of available serial devices on all COM ports
        available_comports = serial.tools.list_ports.comports()
        # Format the COM port devices as "<name>: <description>"
        port_choices = [(port + ": " + desc) for port, desc, hwid in sorted(available_comports)]
        port_choice = StringVar()
        port_choice.set(port_choices[1])
        # Create a combo box widget from the list
        combo_box = Combobox(dialog_root, values=port_choices, textvariable=port_choice, state="readonly")
        combo_box.pack(padx=10, pady=10, fill=tkinter.X, expand=True)

        # Create a confirmation button
        button = Button(dialog_root, text="OK", command=dialog_root.destroy)
        button.pack(padx=10, fill=tkinter.X, expand=True)

        # Display the dialog and wait for confirmation
        dialog_root.mainloop()

        # Extract the chosen COM port name from the combo box
        target_port = port_choice.get().split(":")[0]

        # Establish a connection with the chosen device
        serial_connection = serial.Serial(port=target_port,
                                          baudrate=9600,
                                          timeout=1)
        if not serial_connection.isOpen():
            serial_connection.open()

        # Return the connection object
        return serial_connection

    def disconnect(self):
        self.connection.close()

    def read_input(self):
        # Read the incoming input indefinitely
        while True:
            # If the stop variable is set, exit the method
            if self.stop:
                return
            try:
                # Read one line of input and remove all carriage returns and new lines
                raw_data = self.connection.read_until(b"\r\n")
                raw_data_str = raw_data.decode("utf-8").replace("\n", "").replace("\r", "").strip()
                # Convert the input into a list
                raw_data_split = raw_data_str.split(" ")

                # Convert the input list into dictionary
                raw_data_dict = {}
                for raw_data in raw_data_split:
                    name_value = raw_data.split(":")
                    raw_data_dict[name_value[0]] = name_value[1]

                # Set the class properties according to the input
                self.x = int(raw_data_dict["x"])
                self.y = int(raw_data_dict["y"])
                self.but1 = int(raw_data_dict["but1"])
                self.but2 = int(raw_data_dict["but2"])
                self.butj = int(raw_data_dict["butj"])
            except:
                pass

    def write_score(self, score: int):
        # Write the game score to the controller
        self.connection.write(data=score)
