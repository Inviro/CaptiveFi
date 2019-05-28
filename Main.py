"""
CaptiveFi - A simple script dreaming of automation of captive portal logins
Website: https://github.com/Inviro/CaptiveFi
Open source under GNU General Public License v3.0

This is a side project of mine, and it was inspired by the needles amount of time spent just logging into captive portals.
I hope that it makes things run a bit more smoothly for anyone using this program.
"""


from tkinter import Tk, Label, Entry, Button, Menu, Toplevel, IntVar, Checkbutton  # Used for GUI
from os import system, environ  # Used for logging into wifi networks via command line

# Used for opening a website and putting in credentials
from selenium import webdriver  # Basic Web Driver
from selenium.webdriver.support.ui import WebDriverWait as WDWait  # Ensures that fields pop up
# from selenium.webdriver.support import expected_conditions as ec  # Used for checking conditions of previous
from selenium.webdriver.support.expected_conditions import presence_of_element_located as p_ele_located
from selenium.webdriver.common.by import By
# from time import sleep
from collections import defaultdict  # Used to create dictionaries with lists as keys
from selenium.common.exceptions import InvalidArgumentException


class CaptiveFi:
    def __init__(self, parent):
        # Initializes variables
        self.__row_number = 15

        # Label Names
        self._label_names = "Wifi Name", "Wifi Password", "Login Page"

        # Constants
        self._WN = 0
        self._WP = 1
        self._LP = 2
        self._RESIZE_CONSTANT = 32  # y dimension value by which the window is resized per element

        self.__parent = parent
        self.__parent.winfo_toplevel().title("captiveFi")  # Sets title
        self.__parent.resizable(False, False)  # Not resizeable
        self._x_dim = 500
        self._y_dim = 0
        self.__set_window_size()

        self._my_input = []         # Used to store entries in label / entry pairs
        self._my_input_ele = []     # Used to store the elements corresponding to the previous list inputs
        self._my_check_var = []     # Used to store checkboxes
        self._my_radios = []        # Used to store all of the radio buttons
        self._button_value = ''     # Used to store the name of the submit button field

        # Makes menu and entry grid
        self.__make_menu()
        self.__make_grid(self._label_names, '101')

    def __set_window_size(self):
        """
        Sets the window size using self._x_dim and self._y_dim
        :return: None.
        """
        self.__parent.geometry(f'{self._x_dim}x{self._y_dim}')

    def __add_items(self, num_items):
        """
        Resizes the window based on a parameter of extra elements
        :param num_items: Number of extra elements for which the window needs to dynamically resize
        :return: None.
        """
        self._y_dim += self._RESIZE_CONSTANT * num_items
        self.__set_window_size()

    def __make_menu(self):
        """
        Makes the basic GUI and assigns each menu and submenu an appropriate command.
        :return: None.
        """
        __menu = Menu(self.__parent)
        self.__parent.config(menu=__menu)

        # Creating __file submenu and menu items
        __file = Menu(__menu)
        __file.add_command(label="Connect to Wifi", command=lambda: self.__wifi_connect())
        __file.add_command(label="Connect to Captive Portal", command=lambda: self.__captive_connect())
        __file.add_command(label="Connect to Both", command=lambda: self.__both_connect())
        __file.add_command(label="Disconnect from Wifi", command=lambda: self.__wifi_disconnect())
        __file.add_command(label="Clear Fields", command=self.__clear)
        __file.add_command(label="Save", command=lambda: self.__both_connect())     # replace with save
        __file.add_command(label="Load", command=lambda: self.__both_connect())     # replace with load
        __file.add_command(label="Export", command=lambda: self.__both_connect())   # replace with export
        __file.add_command(label="Exit Program", command=self.__parent.quit)

        # Creating __tools submenu and menu items
        __tools = Menu(__menu)
        __tools.add_command(label="Set Auto Load", command=lambda: self.__both_connect())   # replace with auto_load
        __tools.add_command(label="Set Auto Run", command=lambda: self.__both_connect())    # replace with auto_run

        # Creating help submenu and menu items
        __help_menu = Menu(__menu)
        __help_menu.add_command(label="About", command=lambda: self.__credits())

        # Adding in the submenus
        __menu.add_cascade(label="File", menu=__file)
        __menu.add_cascade(label="Tools", menu=__tools)
        __menu.add_cascade(label="Options", menu=__help_menu)

    def __make_grid(self, label_names, show_hide):
        """
        Converts a list of strings into a simple GUI which contains a label and an entry box
        :param label_names: List of strings for which the GUI is going to make labels and entry boxes
        :param show_hide: Bitstring of boolean values corresponding to the hidden attribute of elements in label_names
        :return:
        """
        for idx, name in enumerate(label_names):
            __temp_label = Label(width=35, text=name+":", anchor="c")
            if show_hide[idx] == "0":
                __temp_entry = Entry(show="*", width=20)
            else:
                __temp_entry = Entry(width=20)
            self._my_input.append(__temp_entry)
            __temp_label.grid(row=self.__row_number, column=1, padx="15", pady="5")
            __temp_entry.grid(row=self.__row_number, column=2, padx="15", pady="5")
            self.__row_number += 1
        self.__add_items(len(label_names))

    def __make_check_box(self, checkbox_names, current_state):
        for idx, name in enumerate(checkbox_names):
            __temp_label = Label(width=35, text=name + ":", anchor="c")
            __temp_var = IntVar(value=int(current_state[idx]))
            __temp_checkbox = Checkbutton(variable=__temp_var)

            self._my_check_var.append(__temp_var)
            __temp_label.grid(row=self.__row_number, column=1, padx="15", pady="5")
            __temp_checkbox.grid(row=self.__row_number, column=2, padx="15", pady="5")
            self.__row_number += 1
        self.__add_items(len(checkbox_names))

    def __make_button(self, button_names, _browser):
        for name in button_names:
            __temp_button = Button(text=name, command=lambda: self.__button_click(_browser))

            self._my_button = __temp_button
            __temp_button.grid(row=self.__row_number, column=1, padx="15", pady="5")
            self.__row_number += 1
        self.__add_items(len(button_names))

    def __send_data(self, _browser):
        def set_field(element):  # Waits for the field, then clicks it
            element_name = element.get_attribute('name')  # Gets the name of the element
            xpath = f"//input[@name='{element_name}']"  # Creates an xpath based on an a given element name
            element = WDWait(_browser, 10).until(p_ele_located((By.XPATH, xpath)))  # Waits until element is present
            element.click()  # Clicks element
            return element

        def set_field_text(element, text):  # Sends keys to the field after calling set_field
            set_field(element).send_keys(text)

        # For each index and element per text input after a certain constant
        for idx, ele in enumerate(self._my_input[self._LP + 1:]):
            temp = ele.get()  # Sets temp to the text in the gui entry field
            if temp:  # If there is text in the entry field
                set_field_text(self._my_input_ele[idx], temp)  # Set the element in the browser to it

    def __button_click(self, _browser):
        """
        Sets the fields in the browser to the ones in the GUI, then sends the data
        :param _browser: The browser in which the elements are found
        :return: None.
        """
        self.__send_data(_browser)
        _browser.find_element_by_xpath(f"//input[@value='{self._button_value}']").submit()

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
        # environ['MOZ_HEADLESS'] = '1'

        __login_page = self._my_input[self._LP].get()
        if __login_page:  # There is a captive portal page present
            _browser = webdriver.Firefox(service_log_path='')
            try:
                _browser.get(__login_page)
            except InvalidArgumentException:
                pass
            __my_elements = _browser.find_elements_by_xpath('//input')  # Sets my_elements to all inputs
            __my_dict = defaultdict(list)  # Dictionary with list as value
            for __ele in __my_elements:  # For each element in the list, append it to the list at the value of the key
                # if __ele.is_displayed():  # Only for visible elements
                __my_dict[__ele.get_attribute('type')].append(__ele)  # Append element to value at key
            __temp = 0
            print(__my_dict)  # """Debug"""

            for key, value in __my_dict.items():  # For each key value pair
                print(key)  # """Debug"""
                temp = []
                temp_state = []

                # Switch case for types of input
                if key == 'text' or key == 'email':
                    for ele in value:
                        self._my_input_ele.append(ele)
                        temp.append(ele.get_attribute('name'))
                    self.__make_grid(temp, len(temp) * '1')
                elif key == 'checkbox':
                    for ele in value:
                        temp.append(ele.get_attribute('name'))
                        temp_state.append(ele.is_selected())
                    self.__make_check_box(temp, temp_state)
                elif key == 'radio':
                    for ele in value:
                        print(ele)
                elif key == 'password':
                    for ele in value:
                        self._my_input_ele.append(ele)
                        temp.append(ele.get_attribute('name'))
                    self.__make_grid(temp, len(temp) * '0')  # Makes hidden entry fields for the passwords
                elif key == 'submit':
                    for ele in value:
                        temp.append(ele.get_attribute('value'))
                        self._my_button = ele
                    self.__make_button(temp, _browser)
        else:
            print('Error: No captive portal page entered.')

    # Connects to wifi and to captive portal
    def __both_connect(self):
        self.__wifi_connect()
        self.__captive_connect()

    # Disconnects from the wifi that is in wifi name
    def __wifi_disconnect(self):
        if self._my_input[self._WN].get():  # Wifi Name exists
            system("netsh wlan disconnect")  # Connects to wifi through cmd
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
    CaptiveFi(root)  # Instance of CaptiveFi using root
    root.mainloop()  # Starts the program


main()
