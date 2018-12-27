from tkinter import Tk, Label, Entry, Button, Grid  # used for GUI


class CaptiveFi:
    def __init__(self, parent):
        self.parent = parent
        parent.winfo_toplevel().title("captiveFi")  # Sets title

        # self.label = Label(parent, text="Welcome to my Program!")
        self.wifi_name_entry = Entry(parent, width=10)
        # self.greet_button = Button(parent, text="Greet", command=self.print)
        self.run_button = Button(parent, text="Run", command=self.greet)
        self.close_button = Button(parent, text="Close", command=parent.quit)
        # self.entry = Entry(parent, width=10)

        to_pack = [self.wifi_name_entry]
        buttons = [self.run_button, self.close_button]
        row = 0
        for ele in to_pack:
            ele.grid(row=row, column=0)
            row += 1

        col = 0
        for button in buttons:
            button.grid(row=row, column=col)
            col += 1

    def greet(self):
        print(self.wifi_name_entry.get())

    def print(self):
        print(self.entry.get())


root = Tk()
gui = CaptiveFi(root)
root.geometry("215x100")  # Size of window
root.mainloop()  # Starts the program
