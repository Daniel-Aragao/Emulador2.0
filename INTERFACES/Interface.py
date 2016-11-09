from Tkinter import *
import tkMessageBox
import threading
from tkFileDialog import askopenfilename
from COMPUTADOR import Constantes as Consts


class Tela(threading.Thread):

    def __init__(self):
        super(Tela, self).__init__()

        self.root = Tk()
        self.root.title("Arquitetura e Org. de Computadores")
        self.root.resizable(width=False, height=False)
        # self.root.geometry("800x500")
        # self.root.configure(background="#2a2730")
        # self.quit_root = self.root.destroy
        # filename = askopenfilename()
        # tkMessageBox.showinfo("Erro", "Informe todos os campos")

        self.top = Frame(self.root)
        self.top.pack()

        self.northgroup = PanedWindow(self.root)  # relief flat, groove, raised, ridge, solid, or sunken

        # clock
        Label(self.northgroup, text="Clock").pack(side="left", padx=10)
        self.clock = DoubleVar()
        # clock.get()
        Scale(self.northgroup, variable=self.clock, from_=10**2, to=10**9, orient="horizontal").pack(side="left")

        # lbar
        Label(self.northgroup, text="Largura do barramento").pack(side="left", padx=10)
        self.lbar = DoubleVar()
        Scale(self.northgroup, variable=self.lbar, from_=2 ** 3, to=2 ** 7, orient="horizontal").pack(side="left")

        self.northgroup.pack()

    @staticmethod
    def center(toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def run(self):
        Tela.center(self.root)
        self.root.mainloop()
