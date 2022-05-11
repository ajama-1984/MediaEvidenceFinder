from tkinter import *
import self
from Case import Case

if __name__ == '__main__':
    gui = Tk(className='Media Evidence Finder')
    # set window size
    gui.geometry("1280x720")
    menubar = Menu(gui)
    gui.config(menu=menubar)
    fileMenu = Menu(menubar,tearoff=0)
    menubar.add_cascade(label="File",menu=fileMenu)

    openMenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Open",menu=openMenu)
    openMenu.add_command(label="Open Existing Case", command= lambda: Case.openCase(self))

    gui.mainloop()


