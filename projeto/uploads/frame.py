from Tkinter import *

raiz = Tk()
cont = Frame(raiz)
cont.pack()

ct = Text(cont, width="10", height="2")
ct.pack()

botaoA = Button(cont)
botaoA["text"]="+"
botaoA.pack()

botaoS = Button(cont)
botaoS["text"]="-"
botaoS.pack()

botaoM = Button(cont)
botaoM["text"]="X"
botaoM.pack()

botaoD = Button(cont)
botaoD["text"]="/"
botaoD.pack()

raiz.mainloop()