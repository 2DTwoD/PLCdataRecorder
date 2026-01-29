import datetime
import threading
from tkinter import ttk, Text, BOTH, RIGHT, Y, END, LEFT


time_format_for_text_area = '%d.%m.%Y %H:%M:%S.%f'


class TextArea(ttk.Frame):
    def __init__(self, master, height=3):
        ttk.Frame.__init__(self, master)

        self.mutex = threading.Lock()
        self.textArea = Text(self, wrap="word", height=height, state="disabled")
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.textArea.yview)

        self.textArea.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)
        self.textArea["yscrollcommand"] = scroll.set

    def clearArea(self):
        with self.mutex:
            self.textArea.configure(state='normal')
            self.textArea.delete('1.0', END)
            self.textArea.configure(state='disabled')

    def insertText(self, text: str, date_flag=True, new_line_flag=False):
        with self.mutex:
            if not isinstance(text, str) or text.strip() == "":
                return

            self.textArea.configure(state='normal')

            date_txt = datetime.datetime.now().strftime(time_format_for_text_area)[:-3] + ' - ' if date_flag else ''
            new_line = "" if not new_line_flag or str(self.textArea.get(1.0, END)).isspace() else "\n"

            self.textArea.insert(END, f"{new_line}{date_txt}{text}")
            self.textArea.yview(END)

            self.textArea.configure(state='disabled')

    def insertNewLineText(self, text: str, date_flag=True):
        self.insertText(text, date_flag, new_line_flag=True)

    def clearAndInsertText(self, text: str, date_flag=True):
        self.clearArea()
        self.insertText(text, date_flag)
