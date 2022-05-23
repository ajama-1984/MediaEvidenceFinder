from tkinter import *
import self
from Case import Case
from evidence import Evidence


if __name__ == '__main__':
    gui = Tk(className='Media Evidence Finder')
    # set window size
    gui.geometry("1280x720")
    menubar = Menu(gui)
    gui.config(menu=menubar)
    fileMenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="New Case", command=lambda: Case.createCase(self))
    openMenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Open", menu=openMenu)
    openMenu.add_command(label="Open Existing Case", command=lambda: Case.openCase(self))

    gui.mainloop()




