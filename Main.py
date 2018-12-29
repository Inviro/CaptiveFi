from tkinter import Tk, Label, Entry, Button, Menu, Toplevel  # used for GUI


class CaptiveFi:
    def __init__(self, parent):
        # Initializes variables
        self.label_names = "Wifi Name", "Username", "Password"  # Name of each label
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
        file.add_command(label="Run", command=self.run)
        file.add_command(label="Clear", command=self.clear)
        file.add_command(label="Save", command=self.run)  # replace with save
        file.add_command(label="Load", command=self.run)  # replace with load
        file.add_command(label="Exit", command=self.parent.quit)

        # Creating tools submenu and menu items
        tools = Menu(menu)
        tools.add_command(label="Set Autoload", command=self.run)  # replace with auto_load
        tools.add_command(label="Set AutoRun", command=self.run)  # replace with auto_run

        # Creating help submenu and menu items
        help_menu = Menu(menu)
        help_menu.add_command(label="About", command=lambda: self.credits())  # replace with credits

        # Adding in the submenus
        menu.add_cascade(label="File", menu=file)
        menu.add_cascade(label="Tools", menu=tools)
        menu.add_cascade(label="Options", menu=help_menu)

    def make_grid(self):
        row_origin = 15
        for name in self.label_names:
            temp_label = Label(width=10, text=name+":", anchor="c")
            temp_entry = Entry(width=10)
            self.my_input.append(temp_entry)
            temp_label.grid(row=row_origin, column=1, padx="15", pady="5")
            temp_entry.grid(row=row_origin, column=2, padx="15", pady="5")
            row_origin += 1

    def run(self):
        for ele in self.my_input:
            print(ele.get())

    def clear(self):
        for ele in self.my_input:
            ele.delete(0, 'end')

    def print(self):
        print(self.entry.get())

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
        self.popup_message("Credits",
                           "CaptiveFi - A script dreaming of freedom from manual captive logins.\n"
                           "Website: https://github.com/Inviro/CaptiveFi\n"
                           "Open Source under the GNU General Public License v3.0\n",
                           "380x90")


root = Tk()
gui = CaptiveFi(root)
root.geometry("215x100")  # Size of window
root.mainloop()  # Starts the program
