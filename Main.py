from tkinter import Tk, Label, Entry, Button, Menu  # used for GUI


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
        file = Menu(menu)
        file.add_command(label="Run", command=self.run)
        file.add_command(label="Exit", command=self.parent.quit)
        menu.add_cascade(label="File", menu=file)

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

    def print(self):
        print(self.entry.get())


root = Tk()
gui = CaptiveFi(root)
root.geometry("215x100")  # Size of window
root.mainloop()  # Starts the program
