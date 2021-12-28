import tkinter

root = tkinter.Tk()
root.title("Calculadora")
root.iconbitmap("calculadora_icon.ico")
root.configure(bg="#E6E6E6")
root.resizable(False, False) 

style = ("Sergoe UI", 12)

mainFrame = tkinter.Frame(root)
mainFrame.grid(row=0, column=0, columnspan=4)

# ---------------------------- Images and Image Setup ---------------------------- #

pixel = tkinter.PhotoImage(width=1, height=1)
deleteButtonImage = tkinter.PhotoImage(file="delbutton.png")

# ---------------------------- Calculator Display ---------------------------- #

previewText = tkinter.StringVar()
entryText = tkinter.StringVar()

preview = tkinter.Label(mainFrame, 
                        textvariable=previewText,
                        width=59,
                        background="white",
                        borderwidth=0, 
                        anchor="e",
                        font=("Gadugi", 10))
preview.grid(row=0, column=0, columnspan=4, pady=(1, 0), sticky="e")
preview.grid_propagate(False)

entry = tkinter.Label(mainFrame,
                        textvariable=entryText,
                        width=22,
                        background="white", 
                        borderwidth=0, 
                        anchor="e",
                        font=("Sergoe Ui", 25))
entry.grid(row=1, column=0, columnspan=4, sticky="e")
entry.grid_propagate(False)

entryText.set("0")

# ---------------------------- Classes and Auxiliary Variables ---------------------------- #

mathClicked = False
result = False
mathSymbol = "null"

numberButtonArray =  []


class Auxiliary():

    def FormatEntry():
        
        if "Inf" in entryText.get():
            previewText.set("")

        if len(entryText.get()) > 16:  # Formata acima de 16 dígitos
            formatEntry = "{:.8e}".format(float(entryText.get()))
            entryText.set(formatEntry)

    def LimitEntry():
        if len(entryText.get()) > 16:
            entryText.set(entryText.get()[0:-1])

    def FormatPreview():
        if mathSymbol == "plus":
            previewText.set(previewText.get() + entryText.get() + " + ")
            
        elif mathSymbol == "sub":
            previewText.set(previewText.get() + entryText.get() + " - ")

        elif mathSymbol == "mult":
            previewText.set(previewText.get() + entryText.get() + " X ")

        elif mathSymbol == "div":
            previewText.set(previewText.get() + entryText.get() + " ÷ ")

    def AssignNumberButtons():
        
        for i in range(10):
            numberButton = tkinter.Button(root, 
                                        text=str(i), 
                                        width=100, 
                                        height=65, 
                                        borderwidth=0, 
                                        bg="white", 
                                        command=lambda i=i: Math.DigitButtons(i), 
                                        font=style, 
                                        activebackground="#a5a5a5", 
                                        image=pixel, 
                                        compound="center")

            numberButtonArray.append(numberButton)

            numberButtonArray[i].bind("<Enter>", lambda event, i=i: numberButtonArray[i].configure(bg="#b9b9b9"))
            numberButtonArray[i].bind("<Leave>", lambda event, i=i: numberButtonArray[i].configure(bg="white"))

class Math():

    def DigitButtons(number):

        global mathClicked
        global result

        if mathClicked:
            entryText.set("")
            mathClicked = False
        
        if result:
            previewText.set("")
            result = False

        if entryText.get() == "0":
            entryText.set("")

        entryText.set(entryText.get() + str(number))

        Auxiliary.LimitEntry()
        Auxiliary.FormatEntry()

    def Clear():
        previewText.set("")
        entryText.set("0")

    def Delete():

        if entryText.get() == "0":
            pass

        else:
            entryText.set(entryText.get()[0:-1])

            if len(entryText.get()) == 0:
                entryText.set("0")

    def Comma():

        global mathClicked

        if mathClicked:

            entryText.set("1")

        else:

            if "." not in entryText.get():
                entryText.set(entryText.get() + ".")

    def MathOperations(localSymbol):

        global result

        global mathClicked
        mathClicked = True

        global mathSymbol
        mathSymbol = localSymbol

        Auxiliary.FormatPreview()
        
        completeEquation = previewText.get()

        if "X" in completeEquation:
            completeEquation = completeEquation.replace("X", "*")

        if "÷" in completeEquation:
            completeEquation = completeEquation.replace("÷", "/")
        
        if "=" in completeEquation:
            completeEquation = completeEquation.strip("=")

        if result:
            previewText.set("")
            result = False

            Math.MathOperations(mathSymbol)


        else:

            if mathSymbol == "plus" and "Inf" not in entryText.get():
                completeEquation = completeEquation.rsplit("+", 1)[0]
                entryText.set(round(eval(completeEquation), 14))

            elif mathSymbol == "sub" and "Inf" not in entryText.get():
                completeEquation = completeEquation.rsplit("-", 1)[0]
                entryText.set(round(eval(completeEquation), 14))

            elif mathSymbol == "mult" and "Inf" not in entryText.get():
                completeEquation = completeEquation.rsplit("*", 1)[0]
                entryText.set(round(eval(completeEquation), 14))

            elif mathSymbol == "div" and "Inf" not in entryText.get():
                if float(entryText.get()) > 0: 
                    completeEquation = completeEquation.rsplit("/", 1)[0]
                    entryText.set(round(eval(completeEquation), 14))
                
                else:
                    previewText.set("")
                    entryText.set("0")
                    
            elif mathSymbol == "exp" and "Inf" not in entryText.get():
                try:
                    entryText.set(round(float(entryText.get()) ** 2, 14))

                except OverflowError:
                    previewText.set("")
                    entryText.set("Inf")

            elif mathSymbol == "perx" and "Inf" not in entryText.get():
                if float(entryText.get()) > 0:
                    entryText.set(round(1/float(entryText.get()), 14))

            elif mathSymbol == "sqrt" and "Inf" not in entryText.get():
                entryText.set(round(float(entryText.get()) ** (1/2), 14))

            elif mathSymbol == "percent" and "Inf" not in entryText.get():
                previewText.set(entryText.get() + "%")
                
                if "-" in previewText.get():
                    previewText.set(previewText.get().strip("-"))

        Auxiliary.FormatEntry()

    def Negate():

        if entryText.get()[0] == "0":
            pass

        else:
            if entryText.get()[0] != "-":
                entryText.set("-" + entryText.get())

            else:
                entryText.set(entryText.get()[1:])

    def Equals():

        global result
        result = True

        symbols = ["+", "-", "X", "÷"]

        if mathSymbol == "percent":
            entryText.set(round((float(entryText.get()) / 100) * float(previewText.get().strip("%")), 14))

        elif mathSymbol == "null":
            previewText.set("")

        else:

            for key in symbols:
                if key in previewText.get():

                    if mathSymbol == "plus" and "Inf" not in entryText.get():
                        if "=" in previewText.get():
                            completeEquation = previewText.get().strip("=")
                            previewText.set(completeEquation + "+ " + entryText.get() + " =")
                            entryText.set(round(eval(completeEquation) + float(entryText.get()), 14))
                            
                        else:
                            completeEquation = previewText.get().rsplit("+", 1)[0]
                            previewText.set(previewText.get() + entryText.get() + " =")
                            entryText.set(round(eval(completeEquation) + float(entryText.get()), 14))
                        
                    elif mathSymbol == "sub" and "Inf" not in entryText.get():
                        if "=" in previewText.get():
                            completeEquation = previewText.get().strip("=")
                            previewText.set(completeEquation + "- " + entryText.get() + " =")
                            entryText.set(round(eval(completeEquation) - float(entryText.get()), 14))
                        
                        else:
                            completeEquation = previewText.get().rsplit("-", 1)[0]
                            previewText.set(previewText.get() + entryText.get() + " =")
                            entryText.set(round(eval(completeEquation) - float(entryText.get()), 14))

                    elif mathSymbol == "mult" and "Inf" not in entryText.get():

                        if "=" in previewText.get():
                            completeEquation = previewText.get().strip("=")
                            previewText.set(completeEquation + "X " + entryText.get() + " =")
                            entryText.set(round(eval(completeEquation.replace("X", "*")) * float(entryText.get()), 14))

                        else:
                            completeEquation = previewText.get().rsplit("X", 1)[0]
                            previewText.set(previewText.get() + entryText.get() + " =")
                            entryText.set(round(eval(completeEquation.replace("X", "*")) * float(entryText.get()), 14))

                    elif mathSymbol == "div" and "Inf" not in entryText.get():
                        if float(entryText.get()) > 0: 
                            if "=" in previewText.get():
                                completeEquation = previewText.get().strip("=")
                                previewText.set(completeEquation + "÷ " + entryText.get() + " =")
                                entryText.set(round(eval(completeEquation.replace("÷", "/")) / float(entryText.get()), 14))

                            else:
                                completeEquation = previewText.get().rsplit("÷", 1)[0]
                                previewText.set(previewText.get() + entryText.get() + " =")
                                entryText.set(round(eval(completeEquation.replace("÷", "/")) / float(entryText.get()), 14))

                        else:
                                previewText.set("")
                                entryText.set("0")

                    break

        Auxiliary.FormatEntry()

#region Buttons

# ---------------------------- Create Buttons ---------------------------- #

Auxiliary.AssignNumberButtons()

buttonNegate = tkinter.Button(root, 
                            text="+/-", 
                            width=100, 
                            height=65, 
                            borderwidth=0, 
                            bg="white", 
                            font=style,
                            command=Math.Negate,
                            activebackground="#a5a5a5", 
                            image=pixel, 
                            compound="center")

buttonComma = tkinter.Button(root, 
                            text=",", 
                            width=100, 
                            height=65, 
                            borderwidth=0, 
                            bg="white", 
                            font=style, 
                            command=Math.Comma,
                            activebackground="#a5a5a5", 
                            image=pixel, 
                            compound="center")

buttonPercent = tkinter.Button(root, 
                            text="%", 
                            width=100, height=65, 
                            borderwidth=0, 
                            font=style, 
                            command=lambda: Math.MathOperations("percent"),
                            activebackground="#a5a5a5", 
                            image=pixel, 
                            compound="center")

buttonClear = tkinter.Button(root, 
                            text="Clear", 
                            width=206, 
                            height=65, 
                            borderwidth=0, 
                            font=style, 
                            command=Math.Clear,
                            activebackground="#a5a5a5", 
                            image=pixel, 
                            compound="center")

buttonDelete = tkinter.Button(root, 
                            image=deleteButtonImage, 
                            width=102, 
                            height=67, 
                            borderwidth=0, 
                            font=style, 
                            command=Math.Delete,
                            activebackground="#a5a5a5")

buttonPerx = tkinter.Button(root, 
                            text="1/x", 
                            width=100, 
                            height=65, 
                            borderwidth=0, 
                            font=style, 
                            command=lambda: Math.MathOperations("perx"),
                            activebackground="#a5a5a5", 
                            image=pixel, 
                            compound="center")

buttonExponential = tkinter.Button(root, 
                            text="x²", 
                            width=100, 
                            height=65, 
                            borderwidth=0, 
                            font=style, 
                            command=lambda: Math.MathOperations("exp"), 
                            activebackground="#a5a5a5", 
                            image=pixel, 
                            compound="center")

buttonSqrt = tkinter.Button(root, 
                            text="²√x", 
                            width=100, 
                            height=65, 
                            borderwidth=0, 
                            font=style, 
                            command=lambda: Math.MathOperations("sqrt"),
                            activebackground="#a5a5a5", 
                            image=pixel, 
                            compound="center")

buttonDivision = tkinter.Button(root, 
                            text="÷", 
                            width=100, 
                            height=65, 
                            borderwidth=0, 
                            font=style, 
                            command=lambda: Math.MathOperations("div"),
                            activebackground="#a5a5a5", 
                            image=pixel, 
                            compound="center")

buttonSubtraction = tkinter.Button(root, 
                            text="-", 
                            width=100, 
                            height=65, 
                            borderwidth=0, 
                            font=style, 
                            command=lambda: Math.MathOperations("sub"),
                            activebackground="#a5a5a5", 
                            image=pixel, 
                            compound="center")

buttonMultiplier = tkinter.Button(root, 
                            text="x", 
                            width=100, 
                            height=65, 
                            borderwidth=0, 
                            font=style, 
                            command=lambda: Math.MathOperations("mult"),
                            activebackground="#a5a5a5", 
                            image=pixel, 
                            compound="center")

buttonSum = tkinter.Button(root, 
                            text="+", 
                            width=100, 
                            height=65, 
                            borderwidth=0, 
                            font=style, 
                            command=lambda: Math.MathOperations("plus"),
                            activebackground="#a5a5a5", 
                            image=pixel, 
                            compound="center")

buttonEquals = tkinter.Button(root, 
                            text="=", 
                            width=100, 
                            height=65, 
                            borderwidth=0, 
                            font=style, 
                            bg="#779ebd", 
                            command=Math.Equals,
                            activebackground="#0063b1", 
                            image=pixel, 
                            compound="center")


# ---------------------------- Display Buttons (numbers) ---------------------------- #

numberButtonArray[1].grid(row=6, column=0, padx=(0,2), pady=(2,0))
numberButtonArray[2].grid(row=6, column=1, padx=(0,2), pady=(2,0))
numberButtonArray[3].grid(row=6, column=2, padx=(0,2), pady=(2,0))

numberButtonArray[4].grid(row=5, column=0, padx=(0,2), pady=(2,0))
numberButtonArray[5].grid(row=5, column=1, padx=(0,2), pady=(2,0))
numberButtonArray[6].grid(row=5, column=2, padx=(0,2), pady=(2,0))

numberButtonArray[7].grid(row=4, column=0, padx=(0,2), pady=(2,0))
numberButtonArray[8].grid(row=4, column=1, padx=(0,2), pady=(2,0))
numberButtonArray[9].grid(row=4, column=2, padx=(0,2), pady=(2,0))

numberButtonArray[0].grid(row=7, column=1, padx=(0,2), pady=(2,0))


# ---------------------------- Display Buttons (functions) ---------------------------- #

buttonNegate.grid(row=7, column=0, padx=(0,2), pady=(2,0))
buttonComma.grid(row=7, column=2, padx=(0,2), pady=(2,0))

buttonPercent.grid(row=2, column=0, padx=(0,2))
buttonClear.grid(row=2, column=1, columnspan=2, padx=(0,2))
buttonDelete.grid(row=2, column=3)

buttonPerx.grid(row=3, column=0, padx=(0,2), pady=(2,0))
buttonExponential.grid(row=3, column=1, padx=(0,2), pady=(2,0))
buttonSqrt.grid(row=3, column=2, padx=(0,2), pady=(2,0))
buttonDivision.grid(row=3, column=3, pady=(2,0))

buttonSubtraction.grid(row=5, column=3, pady=(2,0))
buttonMultiplier.grid(row=4, column=3, pady=(2,0))
buttonSum.grid(row=6, column=3, pady=(2,0))
buttonEquals.grid(row=7, column=3, pady=(2,0))


# ---------------------------- Change On Mouse Hover ---------------------------- #

buttonNegate.bind("<Enter>", lambda event: buttonNegate.configure(bg="#b9b9b9"))
buttonNegate.bind("<Leave>", lambda event: buttonNegate.configure(bg="white"))

buttonComma.bind("<Enter>", lambda event: buttonComma.configure(bg="#b9b9b9"))
buttonComma.bind("<Leave>", lambda event: buttonComma.configure(bg="white"))

buttonPercent.bind("<Enter>", lambda event: buttonPercent.configure(bg="#b9b9b9"))
buttonPercent.bind("<Leave>", lambda event: buttonPercent.configure(bg="#f0f0f0"))

buttonClear.bind("<Enter>", lambda event: buttonClear.configure(bg="#b9b9b9"))
buttonClear.bind("<Leave>", lambda event: buttonClear.configure(bg="#f0f0f0"))

buttonDelete.bind("<Enter>", lambda event: buttonDelete.configure(bg="#b9b9b9"))
buttonDelete.bind("<Leave>", lambda event: buttonDelete.configure(bg="#f0f0f0"))

buttonPerx.bind("<Enter>", lambda event: buttonPerx.configure(bg="#b9b9b9"))
buttonPerx.bind("<Leave>", lambda event: buttonPerx.configure(bg="#f0f0f0"))

buttonExponential.bind("<Enter>", lambda event: buttonExponential.configure(bg="#b9b9b9"))
buttonExponential.bind("<Leave>", lambda event: buttonExponential.configure(bg="#f0f0f0"))

buttonSqrt.bind("<Enter>", lambda event: buttonSqrt.configure(bg="#b9b9b9"))
buttonSqrt.bind("<Leave>", lambda event: buttonSqrt.configure(bg="#f0f0f0"))

buttonDivision.bind("<Enter>", lambda event: buttonDivision.configure(bg="#b9b9b9"))
buttonDivision.bind("<Leave>", lambda event: buttonDivision.configure(bg="#f0f0f0"))

buttonMultiplier.bind("<Enter>", lambda event: buttonMultiplier.configure(bg="#b9b9b9"))
buttonMultiplier.bind("<Leave>", lambda event: buttonMultiplier.configure(bg="#f0f0f0"))

buttonSubtraction.bind("<Enter>", lambda event: buttonSubtraction.configure(bg="#b9b9b9"))
buttonSubtraction.bind("<Leave>", lambda event: buttonSubtraction.configure(bg="#f0f0f0"))

buttonSum.bind("<Enter>", lambda event: buttonSum.configure(bg="#b9b9b9"))
buttonSum.bind("<Leave>", lambda event: buttonSum.configure(bg="#f0f0f0"))

buttonEquals.bind("<Enter>", lambda event: buttonEquals.configure(bg="#3a7fb5"))
buttonEquals.bind("<Leave>", lambda event: buttonEquals.configure(bg="#779ebd"))

#endregion

root.mainloop()