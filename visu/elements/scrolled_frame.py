from tkinter import ttk, Canvas, LEFT, BOTH, RIGHT, Y, NW


class ScrolledFrame(ttk.Frame):
    def __init__(self, parent, width=100, height=100):
        super().__init__(parent, width=width, height=height)
        self.pack()

        self.width = width

        self.canvas = Canvas(self, highlightthickness=0)
        scroll = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)

        self.canvas.pack(side=LEFT, fill=BOTH)
        scroll.pack(side=RIGHT, fill=Y)

        scroll.update()
        self.scroll_width = scroll.winfo_width()

        self.canvas.config(width=width - self.scroll_width, height=height)
        self.canvas.config(yscrollcommand=scroll.set)

    def setMainPanel(self, main_panel):
        self.canvas.create_window((0, 0), window=main_panel, anchor=NW, width=self.width - self.scroll_width)
        main_panel.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
