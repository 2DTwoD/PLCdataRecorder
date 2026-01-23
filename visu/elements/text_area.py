from tkinter import ttk, Text, BOTH, RIGHT, Y, END, LEFT


class TextArea(ttk.Frame):
    def __init__(self, master, height=3):
        ttk.Frame.__init__(self, master)

        self.textArea = Text(self, wrap="word", height=height, state="disabled")
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.textArea.yview)

        self.textArea.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)
        self.textArea["yscrollcommand"] = scroll.set

    def clearArea(self):
        self.textArea.configure(state='normal')
        self.textArea.delete('1.0', END)
        self.textArea.configure(state='disabled')

    def insertText(self, text: str):
        if not isinstance(text, str) or text.strip() == "":
            return
        self.textArea.configure(state='normal')
        self.textArea.insert(END, text)
        self.textArea.yview(END)
        self.textArea.configure(state='disabled')

    def insertNewLineText(self, text: str):
        newLine = "" if str(self.textArea.get(1.0, END)).isspace() else "\n"
        self.insertText(newLine + text)

    def clearAndInsertText(self, text: str):
        self.clearArea()
        self.insertText(text)
