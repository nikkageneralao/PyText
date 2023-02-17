import os.path
from tkinter import *
from tkinter import messagebox as message
from tkinter import filedialog as fd
from Stack import *
from tkinter.ttk import *
from tkinter import font
from tkinter import font,colorchooser
import tempfile
from datetime import datetime

#  Class Window is used for managing all the operations in TextEditor
class Window:
    def __init__(self):
        # Variables declarations at initial level
        self.isFileOpen = True
        self.File = ""
        self.isFileChange = False
        self.elecnt = 0
        self.mode = "normal"
        self.fileTypes = [('All Files', '*.*'),
                          ('Python Files', '*.py'),
                          ('Text Document', '*.txt')]

        # Initialisation Of window
        self.window = Tk()
        self.window.geometry("1200x700+20+20")
        self.window.wm_title("PyText")
        p1 = PhotoImage(file='logo.png')
        self.window.iconphoto(False, p1)

        ## Scrollbar
        self.scrollBar = Scrollbar(self.window)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        # Initialisation of Text Widget
        self.TextBox = Text(self.window, highlightthickness=0, font=("Arial", 12), yscrollcommand=self.scrollBar.set)
        self.scrollBar.config(command=self.TextBox.yview)

        ## Status Bar
        self.statusBar=Label(self.window, text='Status Bar')
        self.statusBar.pack(side=BOTTOM)
        self.TextBox.bind('<<Modified>>', self.status_Bar)

        # Initialisation of MenuBar
        self.menuBar = Menu(self.window, bg="#eeeeee", font=("Helvetica", 13), borderwidth=0)
        self.window.config(menu=self.menuBar)

        ## File Menu (added icons images)
        self.fileMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.newImage = PhotoImage(file="new.png")
        self.openImage = PhotoImage(file="open.png")
        self.saveImage = PhotoImage(file="save.png")
        self.saveasImage = PhotoImage(file="saveas.png")
        self.printImage = PhotoImage(file="print.png")
        self.exit = PhotoImage(file="exit.png")
        self.fileMenu.add_command(label=" New", accelerator="Ctrl+N", image=self.newImage, compound=LEFT, command=self.new_file)
        self.fileMenu.add_command(label=" Open", accelerator="Ctrl+O", image=self.openImage, compound=LEFT, command=self.open_file)
        self.fileMenu.add_command(label=" Save", accelerator="Ctrl+S", image=self.saveImage, compound=LEFT, command=self.retrieve_input)
        self.fileMenu.add_command(label=" Save As", accelerator="Ctrl+Alt+S", image=self.saveasImage, compound=LEFT, command=self.saveas_file)
        self.fileMenu.add_command(label=" Print", accelerator="Ctrl+P", image=self.printImage, compound=LEFT, command=self.printFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=" Exit", accelerator="Ctrl+D", image=self.exit, compound=LEFT, command=self._quit)
        self.menuBar.add_cascade(label="    File    ", menu=self.fileMenu)

        ## Edit Menu (added icons images and the select, clear, find and time/date features)
        self.editMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2,
                             font="Helvetica", )
        self.undoImage = PhotoImage(file="undo.png")
        self.redoImage = PhotoImage(file="redo.png")
        self.cutImage = PhotoImage(file="cut.png")
        self.copyImage = PhotoImage(file="copy.png")
        self.pasteImage = PhotoImage(file="paste.png")
        self.selectImage = PhotoImage(file="select.png")
        self.clearImage = PhotoImage(file="clear.png")
        self.findImage = PhotoImage(file="find.png")
        self.timedateImage = PhotoImage(file="timedate.png")
        self.editMenu.add_command(label=" Undo", accelerator="Ctrl+Z", image=self.undoImage, compound=LEFT,command=self.undo)
        self.editMenu.add_command(label=" Redo", accelerator="Ctrl+Shift+Z", image=self.redoImage, compound=LEFT, command=self.redo)
        self.editMenu.add_separator()
        self.editMenu.add_command(label=" Cut", accelerator="Ctrl+X", image=self.cutImage, compound=LEFT, command=self.cut)
        self.editMenu.add_command(label=" Copy", accelerator="Ctrl+C", image=self.copyImage, compound=LEFT, command=self.copy)
        self.editMenu.add_command(label=" Paste", accelerator="Ctrl+V", image=self.pasteImage, compound=LEFT, command=self.paste)
        self.editMenu.add_separator()
        self.editMenu.add_command(label=" Select All", accelerator="Ctrl+A", image=self.selectImage, compound=LEFT)
        self.editMenu.add_command(label=" Clear", accelerator="Ctrl+Alt+X", image=self.clearImage, compound=LEFT)
        self.editMenu.add_command(label=" Find", accelerator="Ctrl+F", image=self.findImage, compound=LEFT, command=self.findText)
        self.editMenu.add_command(label=" Time/Date", accelerator="Ctrl+D", image=self.timedateImage, compound=LEFT, command=self.timeDate)
        self.menuBar.add_cascade(label="    Edit    ", menu=self.editMenu)

        # View Menu
        self.showToolBar = BooleanVar()
        self.showStatusBar = BooleanVar()
        self.toolbarImage = PhotoImage(file="toolbar.png")
        self.statusbarImage = PhotoImage(file="statusbar.png")
        self.viewMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2,
                             font="Helvetica", )
        self.viewMenu.add_checkbutton(label=" Tool Bar ", variable=self.showToolBar, onvalue=True, offvalue=False, image=self.toolbarImage, compound=LEFT, command=self.ToolBarFunc)
        self.showToolBar.set(True)
        self.viewMenu.add_checkbutton(label=" Status Bar ", variable=self.showStatusBar, onvalue=True, offvalue=False, image=self.statusbarImage, compound=LEFT, command=self.StatusBarFunc)
        self.showStatusBar.set(True)
        self.menuBar.add_cascade(label="   View   ", menu=self.viewMenu)

        ## Themes Menu
        self.themesMenu = Menu(self.menuBar, tearoff=False)
        self.defaultImage = PhotoImage(file='white.png')
        self.darkImage = PhotoImage(file='dark.png')
        self.yellowImage = PhotoImage(file='yellow.png')
        self.dwhiteImage = PhotoImage(file='dwhite.png')
        self.pinkImage = PhotoImage(file='pink.png')
        self.greenImage = PhotoImage(file='green.png')
        self.blueImage = PhotoImage(file='blue.png')
        self.redImage = PhotoImage(file='red.png')
        self.themeChoice = StringVar()
        self.themesMenu.add_radiobutton(label='  Default/White', image=self.defaultImage, variable=self.themeChoice, compound=LEFT
                                        , command=lambda: self.changeColor('white', 'black'))
        self.themesMenu.add_radiobutton(label='  Dark', image=self.darkImage, variable=self.themeChoice, compound=LEFT
                                        , command=lambda: self.changeColor('black', 'white'))
        self.themesMenu.add_radiobutton(label='  Yellow', image=self.yellowImage, variable=self.themeChoice, compound=LEFT
                                        , command=lambda: self.changeColor('#FCF9BE', 'black'))
        self.themesMenu.add_radiobutton(label='  Dirty White', image=self.dwhiteImage, variable=self.themeChoice, compound=LEFT
                                        , command=lambda: self.changeColor('#F5EBE0', 'black'))
        self.themesMenu.add_radiobutton(label='  Pink', image=self.pinkImage, variable=self.themeChoice, compound=LEFT
                                        , command=lambda: self.changeColor('#FFC4E1', 'black'))
        self.themesMenu.add_radiobutton(label='  Green', image=self.greenImage, variable=self.themeChoice, compound=LEFT
                                        , command=lambda: self.changeColor('#E1F1DD', 'black'))
        self.themesMenu.add_radiobutton(label='  Blue', image=self.blueImage, variable=self.themeChoice, compound=LEFT
                                        , command=lambda: self.changeColor('#B2C8DF', 'black'))
        self.themesMenu.add_radiobutton(label='  Red', image=self.redImage, variable=self.themeChoice, compound=LEFT
                                        , command=lambda: self.changeColor('#FF9F9F', 'black'))
        self.menuBar.add_cascade(label='   Themes   ', menu=self.themesMenu)

        # Help Menu
        self.helpMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2,
                             font="Helvetica", )
        self.helpMenu.add_command(label="    About   ", command=self.about)
        self.menuBar.add_cascade(label="   Help   ", menu=self.helpMenu)

        ## Tool Bar
        ## Font Button
        self.toolBar = Label(self.window)
        self.toolBar.pack(side=TOP, fill=X)
        self.fontFamilies = font.families()
        self.fontFamily_variable = StringVar()
        self.fontFamily_combobox = Combobox(self.toolBar, width=30, values=self.fontFamilies, state='readonly', textvariable=self.fontFamily_variable)
        self.fontFamily_combobox.current(self.fontFamilies.index('Arial'))
        self.fontFamily_combobox.grid(row=0, column=0, padx=5)
        ## Font Functionality
        self.fontFamily_combobox.bind('<<ComboboxSelected>>', self.font_Style)
        ## Font Size
        self.fontSize_variable = IntVar()
        self.fontSize_combobox = Combobox(self.toolBar, width=14, textvariable=self.fontSize_variable, state='readonly', values=tuple(range(8,80)))
        self.fontSize_combobox.current(4)
        self.fontSize_combobox.grid(row=0, column=1, padx=5)
        ## Font Size Functionality
        self.fontSize_combobox.bind('<<ComboboxSelected>>', self.font_Size)
        ## Bold Button
        self.boldImage = PhotoImage(file='bold.png')
        self.boldButton = Button(self.toolBar, image=self.boldImage, command=self.boldText)
        self.boldButton.grid(row=0, column=2, padx=5)
        ## Italic Button
        self.italicImage = PhotoImage(file='italic.png')
        self.italicButton = Button(self.toolBar, image=self.italicImage, command=self.italicText)
        self.italicButton.grid(row=0, column=3, padx=5)
        ## Underline Button
        self.underlineImage = PhotoImage(file='underline.png')
        self.underlineButton = Button(self.toolBar, image=self.underlineImage, command=self.underlineText)
        self.underlineButton.grid(row=0, column=4, padx=5)
        ## Text Color
        self.colorImage = PhotoImage(file='color2.png')
        self.colorButton = Button(self.toolBar, image=self.colorImage, command=self.colorText)
        self.colorButton.grid(row=0, column=5, padx=5)
        ## Text Alignment
        self.leftAlignImage = PhotoImage(file='alignleft.png')
        self.rightAlignImage = PhotoImage(file='alignright.png')
        self.centerAlignImage = PhotoImage(file='aligncenter.png')
        self.leftAlignButton = Button(self.toolBar, image=self.leftAlignImage, command=self.leftAlignText)
        self.rightAlignButton = Button(self.toolBar, image=self.rightAlignImage, command=self.rightAlignText)
        self.centerAlignButton = Button(self.toolBar, image=self.centerAlignImage, command=self.centerText)
        self.leftAlignButton.grid(row=0, column=6, padx=5)
        self.rightAlignButton.grid(row=0, column=8, padx=5)
        self.centerAlignButton.grid(row=0, column=7, padx=5)
        ## Controls
        self.window.bind("<Control-f>", self.findText)
        self.window.bind("<Control-d>", self._quit)
        self.window.bind("<Control-Alt-s>", self.saveas_file)
        self.window.bind("<Control-p>", self.printFile)
        self.window.bind("<Control-d>", self.timeDate)

        # Initialisation Of Stack Objects By Original state i.e if the file contains data, it is the Original state of
        # that file
        self.UStack = Stack(self.TextBox.get("1.0", "end-1c"))
        self.RStack = Stack(self.TextBox.get("1.0", "end-1c"))

    #     Member Functions
    # 1. New File method which creates a new file
    def new_file(self):
        self.TextBox.config(state=NORMAL)
        if self.isFileOpen:
            if len(self.File) > 0:
                if self.isFileChange:
                    self.save_file(self.File)
                self.window.wm_title("Untitled")
                self.TextBox.delete('1.0', END)
                self.File = ''
            else:
                if self.isFileChange:
                    result = message.askquestion('Window Title', 'Do You Want to Save Changes')
                    self.save_new_file(result)
                self.window.wm_title("Untitled")
                self.TextBox.delete('1.0', END)
        else:
            self.isFileOpen = True
            self.window.wm_title("Untitled")

        self.isFileChange = False

        if self.UStack.size() > 0:
            self.UStack.clear_stack()
            self.UStack.add(self.TextBox.get("1.0", "end-1c"))

    # 2. Open a file which opens a file in editing mode
    def open_file(self):
        global filename
        self.TextBox.config(state=NORMAL)
        if self.isFileOpen and self.isFileChange:
            self.save_file(self.File)
        filename = fd.askopenfilename(filetypes=self.fileTypes, defaultextension=".txt")
        if len(filename) != 0:
            self.isFileChange = False
            outfile = open(filename, "r")
            text = outfile.read()
            self.TextBox.delete('1.0', END)
            self.TextBox.insert(END, text)
            self.window.wm_title(os.path.basename(filename))
            self.isFileOpen = True
            self.File = filename

        if self.UStack.size() > 0:
            self.UStack.clear_stack()
            self.UStack.add(self.TextBox.get("1.0", "end-1c"))

    # 3. Save file
    def save_file(self, file, event):
        result = message.askquestion('Window Title', 'Do You Want to Save Changes')
        if result == "yes":
            if len(file) == 0:
                saveFile = fd.asksaveasfile(filetypes=self.fileTypes, defaultextension=".txt")
                if saveFile is None:
                    pass
                else:
                    print(saveFile.name)
                    self.write_file(saveFile.name)
                    self.TextBox.delete('1.0', END)
            else:
                self.write_file(file)

    # 3.1 Save as file
    def saveas_file(self, event):
        saveFile = fd.asksaveasfile(filetypes=self.fileTypes, defaultextension=".txt")
        if saveFile is None:
            pass
        else:
            content = self.TextBox.get(0.0, END)
            saveFile.write(content)
            saveFile.close()
    # 4. Save new file -> this function is for saving the new file
    def save_new_file(self, result):
        self.isFileChange = False
        if result == "yes":
            saveFile = fd.asksaveasfile(filetypes=self.fileTypes, defaultextension=".txt")
            if saveFile is None:
                pass
            else:
                self.write_file(saveFile.name)
                self.File = saveFile.name
        else:
            self.TextBox.delete('1.0', END)

    # 5. Writing in file
    def write_file(self, file):
        inputValue = self.TextBox.get("1.0", "end-1c")
        outfile = open(file, "w")
        outfile.write(inputValue)

    # 6. Getting the data from file and showing in the text widget box
    def retrieve_input(self):
        if self.isFileOpen and len(self.File) != 0:
            self.write_file(self.File)
            self.isFileChange = False
        else:
            self.save_new_file("yes")
            self.window.wm_title(self.File)
            self.isFileOpen = True

    # 7. This function invokes whenever a key is pressed whether it is a special-key or a normal key
    def key_pressed(self, event):
        if event.char == "\x1a" and event.keysym == "Z":
            self.redo()
        elif event.char == "\x1a" and event.keysym == "z":
            self.undo()
        elif event.char == "\x13":
            self.retrieve_input()
        elif event.char == "\x0f":
            self.open_file()
        elif event.char == "\x0e":
            self.new_file()
        elif event.char == "\x04":
            self._quit()
        elif event.char == " " or event.char == ".":
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)
        elif event.keysym == 'Return':
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)
        elif event.keysym == 'BackSpace':
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)
        elif (event.keysym == 'Up' or event.keysym == 'Down') or (event.keysym == 'Left' or event.keysym == 'Right'):
            self.isFileChange = True
            self.elecnt = 0
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)
        else:
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            if self.elecnt >= 1:
                self.UStack.remove()
            self.UStack.add(inputValue)
            self.elecnt += 1

        if self.TextBox.get("1.0", "end-1c") == self.UStack.ele(0):
            self.isFileChange = False

    # 8. Undo the data by calling Stack class functions
    def undo(self):
        self.isFileChange = True
        if self.UStack.size() == 1:
            self.UStack.remove()
            self.UStack.add(self.TextBox.get("1.0", "end-1c"))
        else:
            self.RStack.add(self.UStack.remove())
            text = self.UStack.peek()
            self.TextBox.delete('1.0', END)
            self.TextBox.insert(END, text)

    # 9. Redo/Rewrite the task/data by calling Stack class functions
    def redo(self):
        if self.RStack.size() > 1:
            text = self.RStack.peek()
            self.TextBox.delete('1.0', END)
            self.TextBox.insert(END, text)
            self.UStack.add(text)
            self.RStack.remove()

    # 10. Close the window (called when the close button at the right-top is clicked)
    def on_closing(self):
        if self.isFileOpen and self.isFileChange:
            self.save_file(self.File)
        self.window.quit()
        self.window.destroy()

    # 11. Quit or Exit Function to exit from Text-Editor
    def _quit(self, event):
        if self.isFileOpen and self.isFileChange:
            self.save_file(self.File)
        self.window.quit()
        self.window.destroy()

    ## 12. Color Theme
    def changeColor(self, bg_color, fg_color):
        self.TextBox.config(bg=bg_color, fg=fg_color)

    # 13. About
    def about(self):
        outfile = open("About.txt", "r")
        text = outfile.read()
        self.TextBox.insert(END, text)
        self.TextBox.config(state=DISABLED)

    # 14. Copy
    def copy(self):
        self.TextBox.clipboard_clear()
        text = self.TextBox.get("sel.first", "sel.last")
        self.TextBox.clipboard_append(text)

    # 15. Cut
    def cut(self):
        self.copy()
        self.TextBox.delete("sel.first", "sel.last")
        self.UStack.add(self.TextBox.get("1.0", "end-1c"))

    # 16. Paste
    def paste(self):
        text = self.TextBox.selection_get(selection='CLIPBOARD')
        self.TextBox.insert('insert', text)
        self.UStack.add(self.TextBox.get("1.0", "end-1c"))

    ## 17. Font and Font Size Features
    fontSize = 12
    fontStyle = 'Arial'
    def font_Style(self, event):
        global fontStyle
        self.fontStyle = self.fontFamily_variable.get()
        self.TextBox.config(font=(self.fontStyle, self.fontSize))

    def font_Size(self, event):
        global fontSize
        self.fontSize = self.fontSize_variable.get()
        self.TextBox.config(font=(self.fontStyle, self.fontSize))

    ## 18. Bold Text Feature
    def boldText(self):
        self.textProperty = font.Font(font=self.TextBox['font']).actual()
        if self.textProperty['weight'] == 'normal':
            self.TextBox.config(font=(self.fontStyle, self.fontSize, 'bold'))

        if self.textProperty['weight'] == 'bold':
            self.TextBox.config(font=(self.fontStyle, self.fontSize, 'normal'))

    ## 19. Italic Text Feature
    def italicText(self):
        self.textProperty = font.Font(font=self.TextBox['font']).actual()
        if self.textProperty['slant'] == 'roman':
            self.TextBox.config(font=(self.fontStyle, self.fontSize, 'italic'))

        if self.textProperty['slant'] == 'italic':
            self.TextBox.config(font=(self.fontStyle, self.fontSize, 'roman'))

    ## 20. Underline Text Feature
    def underlineText(self):
        self.textProperty = font.Font(font=self.TextBox['font']).actual()
        if self.textProperty['underline'] == 0:
            self.TextBox.config(font=(self.fontStyle, self.fontSize, 'underline'))

        if self.textProperty['underline'] == 1:
            self.TextBox.config(font=(self.fontStyle, self.fontSize))

    ## 21. Text Color Feature
    def colorText(self):
        color = colorchooser.askcolor()
        self.TextBox.config(fg=color[1])

    ## 22. Left Align Text Feature
    def leftAlignText(self):
        data = self.TextBox.get(0.0, END)
        self.TextBox.tag_config('left', justify=LEFT)
        self.TextBox.delete(0.0, END)
        self.TextBox.insert(INSERT, data, 'left')

    ## 23. Right Align Text Feature
    def rightAlignText(self):
        data = self.TextBox.get(0.0, END)
        self.TextBox.tag_config('right', justify=RIGHT)
        self.TextBox.delete(0.0, END)
        self.TextBox.insert(INSERT, data, 'right')

    ## 24. Center Text Feature
    def centerText(self):
        data = self.TextBox.get(0.0, END)
        self.TextBox.tag_config('center', justify=CENTER)
        self.TextBox.delete(0.0, END)
        self.TextBox.insert(INSERT, data, 'center')

    ## 25. Status Bar Feature
    def status_Bar(self, event):
        if self.TextBox.edit_modified():
            words = len(self.TextBox.get(0.0, END).split())
            characters = len(self.TextBox.get(0.0, 'end-1c').replace(' ', ''))
            self.statusBar.config(text=f'Characters: {characters} Words: {words}')
        self.TextBox.edit_modified(False)

    ## 26. Find Feature
    def findText(self, event):

        def findWord():
            self.TextBox.tag_remove('match', 1.0, END)
            start_pos = '1.0'
            word = self.findEntryField.get()
            if word:
                while True:
                    start_pos = self.TextBox.search(word, start_pos, stopindex=END)
                    if not start_pos:
                        break
                    end_pos = f'{start_pos} + {len(word)}c'
                    self.TextBox.tag_add('match', start_pos, end_pos)

                    self.TextBox.tag_config('match', foreground='red', background='yellow')
                    start_pos = end_pos

        def replaceText():
            word = self.findEntryField.get()
            replaceword = self.replaceEntryField.get()
            content = self.TextBox.get(1.0, END)
            newContent = content.replace(word, replaceword)
            self.TextBox.delete(1.0, END)
            self.TextBox.insert(1.0, newContent)


        self.find1 = Toplevel()

        self.find1.title('Find')
        self.find1.geometry('450x250+500+200')
        self.find1.resizable(0,0)

        self.labelFrame = LabelFrame(self.find1, text='Find/Replace')
        self.labelFrame.pack(pady=50)

        self.findLabel = Label(self.labelFrame, text='Find')
        self.findLabel.grid(row=0, column=0, padx=5, pady=5)
        self.findEntryField = Entry(self.labelFrame)
        self.findEntryField.grid(row=0, column=1, padx=5, pady=5)

        self.replaceLabel = Label(self.labelFrame, text='Replace')
        self.replaceLabel.grid(row=1, column=0, padx=5, pady=5)
        self.replaceEntryField = Entry(self.labelFrame)
        self.replaceEntryField.grid(row=1, column=1, padx=5, pady=5)

        self.findButton = Button(self.labelFrame, text='FIND', command=findWord)
        self.findButton.grid(row=2, column=0, padx=5, pady=5)

        self.replaceButton = Button(self.labelFrame, text='REPLACE', command=replaceText)
        self.replaceButton.grid(row=2, column=1, padx=5, pady=5)

        def closeWindow():
            self.TextBox.tag_remove('match', 1.0, END)
            self.find1.destroy()

        self.find1.protocol('WM_DELETE_WINDOW', closeWindow)
        self.find1.mainloop()

    ## 27. View Menu
    def ToolBarFunc(self):
        if self.showToolBar.get()==False:
            self.toolBar.pack_forget()
        if self.showToolBar.get() == True:
            self.TextBox.pack_forget()
            self.toolBar.pack(fill=X)
            self.TextBox.pack(fill=BOTH, expand=1)

    def StatusBarFunc(self):
        if self.showStatusBar.get()==False:
            self.statusBar.pack_forget()
        else:
            self.statusBar.pack()

    ## 28. Print Feature
    def printFile(self, event=None):
        file = tempfile.mktemp('.doc')
        open(file, 'w').write(self.TextBox.get(1.0, END))
        os.startfile(file, 'print')

    ## 29. Date and Time Feature
    def timeDate(self, event=None):
        dateTime = datetime.now()
        formatDT = dateTime.strftime('%H:%M %p %B %d, %Y %A')
        self.TextBox.insert(1.0, formatDT)
