"""
CaptiveFi - A simple script dreaming of automation of captive portal logins
Website: https://github.com/Inviro/CaptiveFi
Open source under GNU General Public License v3.0

This is a side project of mine, and it was inspired by the needles amount of time spent just logging into captive portals.
I hope that it makes things run a bit more smoothly for anyone using this program.
"""


from tkinter import Tk, Label, Entry, Button, Menu, Toplevel  # Used for GUI
from os import system, environ  # Used for logging into wifi networks via command line

# Used for opening a website and putting in credentials
from selenium import webdriver  # Basic Web Driver
from selenium.webdriver.support.ui import WebDriverWait as WDWait  # Ensures that fields pop up
from selenium.webdriver.support import expected_conditions as ec  # Used for checking conditions of previous
from selenium.webdriver.support.expected_conditions import presence_of_element_located as p_ele_located
from selenium.webdriver.common.by import By
from time import sleep


class CaptiveFi:
    def __init__(self, parent):
        # Initializes variables
        # Label Names
        self._label_names = "Wifi Name", "Wifi Password", "Username", "User field", \
                           "Password", "Pass field", "Login Page", "✓Box Field", \
                           "Submit Field"

        # Constants
        self._WN = 0
        self._WP = 1
        self._U = 2
        self._UF = 3
        self._P = 4
        self._PF = 5
        self._LP = 6
        self._CF = 7
        self._S = 8

        self.__parent = parent
        self.__parent.winfo_toplevel().title("captiveFi")  # Sets title
        self._my_input = []

        # Makes menu and entry grid
        self.__make_grid()  # Makes the label and entry pairs from _label_names
        self.__make_menu()

    def __make_menu(self):
        __menu = Menu(self.__parent)
        self.__parent.config(menu=__menu)

        # Creating __file submenu and menu items
        __file = Menu(__menu)
        __file.add_command(label="Connect to Wifi", command=lambda: self.__wifi_connect())
        __file.add_command(label="Connect to Captive Portal", command=lambda: self.__captive_connect())
        __file.add_command(label="Connect to Both", command=lambda: self.__both_connect())
        __file.add_command(label="Disconnect from Wifi", command=lambda: self.__wifi_disconnect())
        __file.add_command(label="Clear Fields", command=self.__clear)
        __file.add_command(label="Save", command=lambda: self.__both_connect())  # replace with save
        __file.add_command(label="Load", command=lambda: self.__both_connect())  # replace with load
        __file.add_command(label="Export", command=lambda: self.__both_connect())  # replace with export
        __file.add_command(label="Exit Program", command=self.__parent.quit)

        # Creating __tools submenu and menu items
        __tools = Menu(__menu)
        __tools.add_command(label="Set Auto Load", command=lambda: self.__both_connect())  # replace with auto_load
        __tools.add_command(label="Set Auto Run", command=lambda: self.__both_connect())  # replace with auto_run

        # Creating help submenu and menu items
        __help_menu = Menu(__menu)
        __help_menu.add_command(label="About", command=lambda: self.__credits())

        # Adding in the submenus
        __menu.add_cascade(label="File", menu=__file)
        __menu.add_cascade(label="Tools", menu=__tools)
        __menu.add_cascade(label="Options", menu=__help_menu)

    def __make_grid(self):
        row_origin = 15  # Row number to begin making the grid
        for name in self._label_names:
            __temp_label = Label(width=10, text=name+":", anchor="c")
            if "Password" in name:
                __temp_entry = Entry(show="*", width=10)
            else:
                __temp_entry = Entry(width=10)

            self._my_input.append(__temp_entry)
            __temp_label.grid(row=row_origin, column=1, padx="15", pady="5")
            __temp_entry.grid(row=row_origin, column=2, padx="15", pady="5")
            row_origin += 1

    # Connects to wifi using data inputted into the GUI
    def __wifi_connect(self):
        if self._my_input[self._WN].get():  # Wifi Name exists
            print("Wifi Name:", self._my_input[self._WN].get())
            if self._my_input[self._WP].get():  # Wifi is password protected
                print("Wifi password", self._my_input[self._WP].get())
            else:  # Wifi is not password protected
                system("netsh wlan connect " + self._my_input[self._WN].get())  # Connects to wifi through cmd
        else:  # Wifi Name does not exist
            print("Error: Please input wifi name.")

    # Connects to captive portal using data inputted into the GUI
    def __captive_connect(self):
        if self._my_input[self._U].get() and self._my_input[self._P].get():  # Login credentials exist
            print("Login username:", self._my_input[self._U].get(), "and password:", self._my_input[self._P].get())
            environ['MOZ_HEADLESS'] = '1'
            _browser = webdriver.Firefox()
            _browser.get(self._my_input[self._LP].get())
            __username = WDWait(_browser, 10).until(p_ele_located((By.NAME, self._my_input[self._UF].get())))
            __password = WDWait(_browser, 10).until(p_ele_located((By.NAME, self._my_input[self._PF].get())))
            __username.send_keys(self._my_input[self._U].get())
            __password.send_keys(self._my_input[self._P].get())
            _check_box = WDWait(_browser, 10).until(ec.element_to_be_clickable(By.NAME, self._my_input[self._UF].get()))
            _check_box.click()
            __submit_button = _browser.find_element_by_id("ID_form6ecb360b_weblogin_submit")
            __submit_button.submit()
            sleep(2)  # Makes sure that it logs in properly
            _browser.close()
        else:
            print("No Login username and password")

    # Connects to wifi and to captive portal
    def __both_connect(self):
        self.__wifi_connect()
        self.__captive_connect()

    # Disconnects from the wifi that is in wifi name
    def __wifi_disconnect(self):
        if self._my_input[self._WN].get():  # Wifi Name exists
            system("netsh wlan disconnect " + self._my_input[self._WP].get())  # Connects to wifi through cmd
        else:  # Wifi Name does not exist
            print("Error: Please input wifi name.")

    def __clear(self):
        for ele in self._my_input:
            ele.delete(0, 'end')

    # Makes a popup on the current window using title and message
    @staticmethod
    def _popup_message(title, message, size):
        __window = Toplevel()
        __window.title(title)
        __window.geometry(size)
        __label = Label(__window, width=100, text=message, anchor="c")
        __label.pack()
        __confirm_button = Button(__window, text="ok", command=lambda: __window.destroy())
        __confirm_button.pack()
        __window.focus_force()

    # Opens up credits: including the developers, dependencies, and copyright
    def __credits(self):
        self._popup_message("Credits",  # Name of window
                            "CaptiveFi - A script dreaming of freedom from manual captive logins.\n"
                            "Website: https://github.com/Inviro/CaptiveFi\n"  # Website
                            "Open Source under the GNU General Public License v3.0\n",  # Open source license
                            "380x100")  # Size of window


def main():
    root = Tk()  # New window
    root.geometry("215x280")  # Size of window
    root.resizable(False, False)  # Not resizeable
    CaptiveFi(root)  # Instance of CaptiveFi using root
    root.mainloop()  # Starts the program


main()
