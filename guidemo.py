from tkinter import *
from tkinter import ttk

class GuiTab:
    def __init__(self):
        nvshr = Tk()
        nvshr.title('Notebook Demo')
        nvshr.geometry('500x500')

        rows = 0
        while rows < 50:
            nvshr.rowconfigure(rows, weight=1)
            nvshr.columnconfigure(rows, weight=1)
            rows += 1

        nb = ttk.Notebook(nvshr)
        nb.grid(row=1, column=0, columnspan=50, rowspan= 49, sticky='NESW')

        page1 = ttk.Frame(nb)
        nb.add(page1, text='Commands')

        self.help = [1, 2, 3, 4]
        self.delete_command_button = {}
        for x in range(0, 4):
            self.delete_command_button[x] = Button(page1, text="Remove Command", command= self.delete_command())
            self.delete_command_button[x].grid(row=x, column=250, padx=10, pady=10, columnspan=100)
        nvshr.mainloop()

    def print_l(self, i):
        
        self.help.pop(i)
        print("The length of commands is " + str(len(self.delete_command_button)))

    def delete_command(self):
            
            #Set up boolean to see if button was pressed, if so then create another function to use that will return the "i" value of the real coordinate of the element indice within the list
            
            return (lambda i=len(self.delete_command_button): [self.print_l(i), self.delete_command_button[i].destroy(), self.delete_command_button.pop(i)])#[self.delete_command_button[i].destroy(), self.delete_command_button.pop(i)])

if __name__ == "__main__":
    GuiTab()