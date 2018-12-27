from tkinter import Tk, Label, Entry, Button  # used for GUI


class CaptiveFi:
    def __init__(self, parent):
        self.label_names = "Wifi Name", "Username", "Password"  # Name of each label

        self.parent = parent
        parent.winfo_toplevel().title("captiveFi")  # Sets title
        self.my_input = []
        self.row = 10  # Current Row

        # Makes and adds buttons
        self.run_button = Button(parent, text="Run", command=self.run)
        self.close_button = Button(parent, text="Close", command=parent.quit)
        self.my_buttons = [self.run_button, self.close_button]
        self.make_grid()
        self.add_buttons()

    def add_buttons(self):
        col = 0  # Column offset
        for button in self.my_buttons:  # For each button: adds button
            button.grid(row=20, column=col)
            col += 1

    def make_grid(self):
        row_displace = 15
        for name in self.label_names:
            temp_label = Label(width=10, text=name+":   ", anchor="w")
            temp_entry = Entry(width=10)
            self.my_input.append(temp_entry)
            temp_label.grid(row=row_displace, column=0)
            temp_entry.grid(row=row_displace, column=1)
            row_displace += 1

    def run(self):
        for ele in self.my_input:
            print(ele.get())

    def print(self):
        print(self.entry.get())


root = Tk()
gui = CaptiveFi(root)
root.geometry("215x100")  # Size of window
root.mainloop()  # Starts the program
