"""
CaptiveFi - A simple script dreaming of automation of captive portal logins
Website: https://github.com/Inviro/CaptiveFi
Open source under GNU General Public License v3.0

This is a side project of mine, and it was inspired by the needles amount of time spent just logging into captive portals.
I hope that it makes things run a bit more smoothly for anyone using this program.
"""


from tkinter import Tk, Label, Entry, Button, Menu, Toplevel  # Used for GUI
from os import system  # Used for logging into wifi networks via command line


class CaptiveFi:
    def __init__(self, parent):
        # Initializes variables
        self.label_names = "Wifi Name", "Wifi Password", "Username", "Above Field", \
                           "Password", "Above Field", "Login Page"  # Name of each label
        self.parent = parent
        parent.winfo_toplevel().title("captiveFi")  # Sets title
        self.my_input = []
        self.row = 10  # Current Row

        # Makes menu and entry grid
        self.make_grid()  # Makes the label and entry pairs from label_names
        self.make_menu()

    def make_menu(self):
        menu = Menu(self.parent)
        self.parent.config(menu=menu)

        # Creating file submenu and menu items
        file = Menu(menu)
        file.add_command(label="Connect to Wifi", command=lambda: self.wifi_connect())
        file.add_command(label="Connect to Captive Portal", command=lambda: self.captive_connect())
        file.add_command(label="Connect to Both", command=lambda: self.both_connect())
        file.add_command(label="Disconnect from Wifi", command=lambda: self.wifi_disconnect())
        file.add_command(label="Clear Fields", command=self.clear)
        file.add_command(label="Save", command=lambda: self.both_connect())  # replace with save
        file.add_command(label="Load", command=lambda: self.both_connect())  # replace with load
        file.add_command(label="Export", command=lambda: self.both_connect())  # replace with export
        file.add_command(label="Exit Program", command=self.parent.quit)

        # Creating tools submenu and menu items
        tools = Menu(menu)
        tools.add_command(label="Set Auto Load", command=lambda: self.both_connect())  # replace with auto_load
        tools.add_command(label="Set Auto Run", command=lambda: self.both_connect())  # replace with auto_run

        # Creating help submenu and menu items
        help_menu = Menu(menu)
        help_menu.add_command(label="About", command=lambda: self.credits())  # replace with credits

        # Adding in the submenus
        menu.add_cascade(label="File", menu=file)
        menu.add_cascade(label="Tools", menu=tools)
        menu.add_cascade(label="Options", menu=help_menu)

    def make_grid(self):
        row_origin = 15  # Row number to begin making the grid
        hide_entry = False
        for name in self.label_names:
            temp_label = Label(width=10, text=name+":", anchor="c")
            if hide_entry:
                temp_entry = Entry(show="*", width=10)
            else:
                temp_entry = Entry(width=10)
            hide_entry = not hide_entry

            self.my_input.append(temp_entry)
            temp_label.grid(row=row_origin, column=1, padx="15", pady="5")
            temp_entry.grid(row=row_origin, column=2, padx="15", pady="5")
            row_origin += 1

    # Connects to wifi using data inputted into the GUI
    def wifi_connect(self):
        if self.my_input[0].get():  # Wifi Name exists
            print("Wifi Name:", self.my_input[0].get())
            if self.my_input[1].get():  # Wifi is password protected
                print("Wifi password", self.my_input[1].get())
            else:  # Wifi is not password protected
                system("netsh wlan connect " + self.my_input[0].get())  # Connects to wifi through cmd
        else:  # Wifi Name does not exist
            print("Error: Please input wifi name.")

    # Connects to captive portal using data inputted into the GUI
    def captive_connect(self):
        if self.my_input[2].get() and self.my_input[3].get():  # Login credentials exist
            print("Login username:", self.my_input[2].get(), "and password:", self.my_input[3].get())
        else:
            print("No Login username and password")

    # Connects to wifi and to captive portal
    def both_connect(self):
        self.wifi_connect()
        self.captive_connect()

    # Disconnects from the wifi that is in wifi name
    def wifi_disconnect(self):
        if self.my_input[0].get():  # Wifi Name exists
            system("netsh wlan disconnect " + self.my_input[1].get())  # Connects to wifi through cmd
        else:  # Wifi Name does not exist
            print("Error: Please input wifi name.")

    def clear(self):
        for ele in self.my_input:
            ele.delete(0, 'end')

    # Makes a popup on the current window using title and message
    @staticmethod
    def popup_message(title, message, size):
        window = Toplevel()
        window.title(title)
        window.geometry(size)
        label = Label(window, width=100, text=message, anchor="c")
        label.pack()
        confirm_button = Button(window, text="ok", command=lambda: window.destroy())
        confirm_button.pack()
        window.focus_force()

    # Opens up credits: including the developers, dependencies, and copyright
    def credits(self):
        self.popup_message("Credits",  # Name of window
                           "CaptiveFi - A script dreaming of freedom from manual captive logins.\n"
                           "Website: https://github.com/Inviro/CaptiveFi\n"  # Website
                           "Open Source under the GNU General Public License v3.0\n",  # Open source license
                           "380x90")  # Size of window


root = Tk()  # New window
root.geometry("215x220")  # Size of window
gui = CaptiveFi(root)  # Instance of CaptiveFi using root
root.mainloop()  # Starts the program
